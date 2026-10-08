#!/usr/bin/env python3
"""Fail closed unless a style 20 candidate passes pixel and review gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import render_prompt


EXPECTED_SCORE_DIMENSIONS = (
    "shape-language",
    "face-language",
    "line-material",
    "directional-black-hatching",
    "mustard-yellow-material",
    "negative-space",
    "single-action-storytelling",
    "originality-boundary",
)
MINIMUM_REVIEW_SCORE = 34
MINIMUM_WHITE_RATIO = 0.75
MAXIMUM_WHITE_RATIO = 0.98
MINIMUM_DARK_RATIO = 0.003
MAXIMUM_DARK_RATIO = 0.15
MINIMUM_MUSTARD_RATIO = 0.004
MAXIMUM_MUSTARD_RATIO = 0.12
MAXIMUM_CORAL_RED_RATIO = 0.02
MAXIMUM_DISALLOWED_COOL_RATIO = 0.005
MAXIMUM_NEON_YELLOW_RATIO = 0.01


def rgb_hsv(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    red, green, blue = (channel / 255 for channel in rgb)
    maximum = max(red, green, blue)
    minimum = min(red, green, blue)
    difference = maximum - minimum
    saturation = 0.0 if maximum == 0 else difference / maximum
    if difference == 0:
        hue_degrees = 0.0
    elif maximum == red:
        hue_degrees = 60 * (((green - blue) / difference) % 6)
    elif maximum == green:
        hue_degrees = 60 * (((blue - red) / difference) + 2)
    else:
        hue_degrees = 60 * (((red - green) / difference) + 4)
    return hue_degrees, saturation, maximum


def calculate_palette_metrics(image_path: Path) -> dict[str, float]:
    _, color_type, bytes_per_pixel, pixel_bytes = render_prompt.decode_png_pixel_bytes(image_path)
    if color_type not in {2, 6}:
        raise ValueError("画风 20 自动验收只支持 8-bit RGB 或 RGBA PNG")

    pixel_count = len(pixel_bytes) // bytes_per_pixel
    sample_stride = max(1, pixel_count // 150_000)
    sampled_pixels = 0
    white_pixels = 0
    dark_pixels = 0
    mustard_pixels = 0
    coral_red_pixels = 0
    disallowed_cool_pixels = 0
    neon_yellow_pixels = 0

    for pixel_index in range(0, pixel_count, sample_stride):
        byte_offset = pixel_index * bytes_per_pixel
        rgb = tuple(pixel_bytes[byte_offset : byte_offset + 3])
        hue_degrees, saturation, value = rgb_hsv(rgb)
        sampled_pixels += 1
        white_pixels += value > 0.82 and saturation < 0.18
        dark_pixels += value < 0.28
        is_mustard = 32 <= hue_degrees <= 68 and saturation > 0.18 and value > 0.45
        mustard_pixels += is_mustard
        coral_red_pixels += (
            (hue_degrees <= 25 or hue_degrees >= 345)
            and saturation > 0.12
            and value > 0.45
        )
        disallowed_cool_pixels += (
            150 <= hue_degrees <= 300 and saturation > 0.18 and value > 0.35
        )
        neon_yellow_pixels += is_mustard and saturation > 0.65 and value > 0.90

    return {
        "white_ratio": white_pixels / sampled_pixels,
        "dark_ratio": dark_pixels / sampled_pixels,
        "mustard_ratio": mustard_pixels / sampled_pixels,
        "coral_red_ratio": coral_red_pixels / sampled_pixels,
        "disallowed_cool_ratio": disallowed_cool_pixels / sampled_pixels,
        "neon_yellow_ratio": neon_yellow_pixels / sampled_pixels,
    }


def validate_palette_metrics(metrics: dict[str, float]) -> list[str]:
    failures: list[str] = []
    bounded_metrics = (
        ("white_ratio", MINIMUM_WHITE_RATIO, MAXIMUM_WHITE_RATIO),
        ("dark_ratio", MINIMUM_DARK_RATIO, MAXIMUM_DARK_RATIO),
        ("mustard_ratio", MINIMUM_MUSTARD_RATIO, MAXIMUM_MUSTARD_RATIO),
    )
    for metric_name, minimum, maximum in bounded_metrics:
        value = metrics[metric_name]
        if not minimum <= value <= maximum:
            failures.append(f"{metric_name}={value:.6f} outside [{minimum}, {maximum}]")
    maximum_metrics = (
        ("coral_red_ratio", MAXIMUM_CORAL_RED_RATIO),
        ("disallowed_cool_ratio", MAXIMUM_DISALLOWED_COOL_RATIO),
        ("neon_yellow_ratio", MAXIMUM_NEON_YELLOW_RATIO),
    )
    for metric_name, maximum in maximum_metrics:
        value = metrics[metric_name]
        if value > maximum:
            failures.append(f"{metric_name}={value:.6f} exceeds {maximum}")
    return failures


def load_review_scorecard(
    scorecard_path: Path,
    source_image_sha256: str,
    image_sha256: str,
) -> tuple[int, list[str]]:
    scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    if scorecard.get("style_contract") != "warm-yellow-ink-story-v3":
        failures.append("scorecard style_contract mismatch")
    if scorecard.get("image_sha256") != image_sha256:
        failures.append("scorecard image_sha256 mismatch")
    if scorecard.get("source_image_sha256") != source_image_sha256:
        failures.append("scorecard source_image_sha256 mismatch")
    content_lock = scorecard.get("content_lock")
    if not isinstance(content_lock, dict):
        failures.append("scorecard content_lock must be an object")
    else:
        expected_subjects = content_lock.get("expected_subjects")
        observed_subjects = content_lock.get("observed_subjects")
        if not isinstance(expected_subjects, dict) or not expected_subjects:
            failures.append("content_lock expected_subjects must be a non-empty object")
        if observed_subjects != expected_subjects:
            failures.append("content_lock observed_subjects mismatch")
        if content_lock.get("identity_preserved") is not True:
            failures.append("content_lock identity_preserved must be true")
        if content_lock.get("required_objects_preserved") is not True:
            failures.append("content_lock required_objects_preserved must be true")
    scores = scorecard.get("scores")
    if not isinstance(scores, dict) or set(scores) != set(EXPECTED_SCORE_DIMENSIONS):
        failures.append("scorecard must contain exactly the eight required dimensions")
        return 0, failures
    for dimension, score in scores.items():
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 5:
            failures.append(f"score {dimension} must be an integer from 0 to 5")
    hard_failures = scorecard.get("hard_failures")
    if not isinstance(hard_failures, list):
        failures.append("scorecard hard_failures must be a list")
    elif hard_failures:
        failures.extend(f"hard failure: {failure}" for failure in hard_failures)
    total_score = sum(score for score in scores.values() if isinstance(score, int))
    if total_score < MINIMUM_REVIEW_SCORE:
        failures.append(f"review score {total_score} is below {MINIMUM_REVIEW_SCORE}")
    return total_score, failures


def build_validation_report(
    image_path: Path,
    source_image_path: Path,
    scorecard_path: Path,
) -> dict[str, object]:
    image_sha256 = hashlib.sha256(image_path.read_bytes()).hexdigest()
    source_image_sha256 = hashlib.sha256(source_image_path.read_bytes()).hexdigest()
    palette_metrics = calculate_palette_metrics(image_path)
    palette_failures = validate_palette_metrics(palette_metrics)
    review_score, review_failures = load_review_scorecard(
        scorecard_path,
        source_image_sha256,
        image_sha256,
    )
    failures = palette_failures + review_failures
    return {
        "style_contract": "warm-yellow-ink-story-v3",
        "image": str(image_path.resolve()),
        "image_sha256": image_sha256,
        "source_image": str(source_image_path.resolve()),
        "source_image_sha256": source_image_sha256,
        "scorecard": str(scorecard_path.resolve()),
        "palette_metrics": palette_metrics,
        "review_score": review_score,
        "minimum_review_score": MINIMUM_REVIEW_SCORE,
        "failures": failures,
        "status": "pass" if not failures else "rejected",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="验收风格 20 最终候选并失败关闭")
    parser.add_argument("--image", required=True, type=Path, help="待验收 PNG")
    parser.add_argument("--source-image", required=True, type=Path, help="基础生成 PNG")
    parser.add_argument("--scorecard", required=True, type=Path, help="八维人工评分卡 JSON")
    parser.add_argument("--output", type=Path, help="可选的验收报告 JSON 路径")
    args = parser.parse_args()

    try:
        if not args.image.is_file():
            raise ValueError(f"待验收图片不可用: {args.image}")
        if not args.source_image.is_file():
            raise ValueError(f"基础生成图片不可用: {args.source_image}")
        if not args.scorecard.is_file():
            raise ValueError(f"评分卡不可用: {args.scorecard}")
        report = build_validation_report(args.image, args.source_image, args.scorecard)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"validate_style_20_asset: {error}", file=sys.stderr)
        return 2

    report_json = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(f"{report_json}\n", encoding="utf-8")
    print(report_json)
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
