#!/usr/bin/env bash
# 画风 21 手写独白彩铅:本机 Codex CLI 直接出图,默认 3:4、1086×1448。
# 用法:
#   bash scripts/generate_monologue_card_with_codex.sh --text '中文文案' --out out/card.png [--subject '…'] [--aspect 3:4]
#   --privacy-script PATH 可指定 sweety-image-privacy/scripts/main.ts。
# 依赖:已登录且支持生图的 Codex CLI、Python 3.10+、bun、sweety-image-privacy;默认尺寸还需要 macOS sips。
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MONOLOGUE_TEXT="" SUBJECT_DESCRIPTION="" OUTPUT_PATH="" REASONING_EFFORT="low" ASPECT_RATIO=""
PRIVACY_SCRIPT="${SWEETY_IMAGE_PRIVACY_SCRIPT:-}"
while [ $# -gt 0 ]; do
  case "$1" in
    --aspect|--text|--subject|--out|--reasoning|--privacy-script)
      [ $# -ge 2 ] || { echo "参数 $1 缺少值" >&2; exit 2; }
      case "$1" in
        --aspect) ASPECT_RATIO="$2" ;;
        --text) MONOLOGUE_TEXT="$2" ;;
        --subject) SUBJECT_DESCRIPTION="$2" ;;
        --out) OUTPUT_PATH="$2" ;;
        --reasoning) REASONING_EFFORT="$2" ;;
        --privacy-script) PRIVACY_SCRIPT="$2" ;;
      esac
      shift 2 ;;
    --keep-metadata) echo "--keep-metadata 不再受支持;生成图片必须通过隐私清理与审计" >&2; exit 2 ;;
    -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done
[ -n "$MONOLOGUE_TEXT" ] || { echo "必须提供 --text(要写进画里的中文文案)" >&2; exit 2; }
[ -n "$OUTPUT_PATH" ] || { echo "必须提供 --out(输出 PNG 路径)" >&2; exit 2; }
case "$OUTPUT_PATH" in *.png|*.PNG) ;; *) echo "--out 必须使用 PNG 文件路径" >&2; exit 2 ;; esac

RENDER_ARGS=(--style 21 --text "$MONOLOGUE_TEXT")
[ -n "$ASPECT_RATIO" ] && RENDER_ARGS+=(--aspect "$ASPECT_RATIO")
[ -n "$SUBJECT_DESCRIPTION" ] && RENDER_ARGS+=(--subject "$SUBJECT_DESCRIPTION")
IMAGE_PROMPT="$(python3 -B "$SCRIPT_ROOT/scripts/render_prompt.py" "${RENDER_ARGS[@]}")"

if [ -z "$PRIVACY_SCRIPT" ]; then
  for PRIVACY_CANDIDATE in \
    "$SCRIPT_ROOT/../sweety-image-privacy/scripts/main.ts" \
    "$HOME/.codex/skills/sweety-image-privacy/scripts/main.ts" \
    "$HOME/.agents/skills/sweety-image-privacy/scripts/main.ts" \
    "$HOME/.claude/skills/sweety-image-privacy/scripts/main.ts"; do
    if [ -f "$PRIVACY_CANDIDATE" ]; then PRIVACY_SCRIPT="$PRIVACY_CANDIDATE"; break; fi
  done
fi
[ -f "$PRIVACY_SCRIPT" ] || { echo "sweety-image-privacy 不可用;请安装该技能或用 --privacy-script 指定脚本" >&2; exit 3; }
command -v bun >/dev/null || { echo "缺少 bun;无法执行 sweety-image-privacy" >&2; exit 3; }
NEEDS_RESIZE=0
if [ -z "$ASPECT_RATIO" ] || [ "$ASPECT_RATIO" = "3:4" ]; then
  NEEDS_RESIZE=1
  command -v sips >/dev/null || { echo "缺少 sips;无法归一到默认尺寸,可用 --aspect 指定其他比例" >&2; exit 3; }
fi
command -v codex >/dev/null || { echo "缺少 Codex CLI" >&2; exit 3; }
FEATURES="$(codex features list 2>/dev/null || true)"
printf '%s\n' "$FEATURES" | grep -qE '^image_generation[[:space:]]+[^[:space:]]+[[:space:]]+true' || { echo "codex 的 image_generation 功能不可用" >&2; exit 3; }

TEMP_WORKSPACE="$(mktemp -d "${TMPDIR:-/tmp}/style21.XXXXXX")"
trap 'rm -rf "$TEMP_WORKSPACE"' EXIT
# Run outside the recipe repository; this entrypoint explicitly requests an image.
if ! codex exec -C "$TEMP_WORKSPACE" -s workspace-write --skip-git-repo-check \
  -c model_reasoning_effort="$REASONING_EFFORT" \
  "这是用户明确要求的本机直接出图任务。用你内置的 image_generation 工具(不要用任何 API/脚本/SVG/Canvas 替代)生成一张图,画幅按下面第一段所写,要求如下,逐字执行,尤其是 TEXT 段里的中文必须逐字准确:

$IMAGE_PROMPT

把生成的 PNG 保存为 $TEMP_WORKSPACE/out.png。完成后只回:done。" </dev/null >"$TEMP_WORKSPACE/codex.log" 2>&1; then
  echo "Codex 图像生成失败,未写入交付路径" >&2
  exit 4
fi

[ -f "$TEMP_WORKSPACE/out.png" ] || { echo "Codex 未产出图片,未写入交付路径" >&2; exit 4; }
if [ "$NEEDS_RESIZE" -eq 1 ]; then sips -z 1448 1086 "$TEMP_WORKSPACE/out.png" >/dev/null; fi
bun "$PRIVACY_SCRIPT" "$TEMP_WORKSPACE/out.png" --json >"$TEMP_WORKSPACE/privacy.json"
python3 -B - "$TEMP_WORKSPACE/privacy.json" <<'PY'
import json
import sys

audits = json.load(open(sys.argv[1], encoding="utf-8"))
if not isinstance(audits, list) or len(audits) != 1:
    raise SystemExit("隐私工具未返回单张图片审计结果")
privacy = audits[0].get("privacy", {})
if privacy.get("gpsPresent") is not False or privacy.get("sourceExifPresent") is not False or privacy.get("requiredMacSourceXattrsPresent") != []:
    raise SystemExit("图片隐私审计未通过,未写入交付路径")
remaining = privacy.get("macSourceXattrsPresent", [])
if remaining:
    print("隐私审计记录仍有 macOS 扩展属性: " + ", ".join(remaining), file=sys.stderr)
PY

mkdir -p "$(dirname "$OUTPUT_PATH")"
cp "$TEMP_WORKSPACE/out.png" "$OUTPUT_PATH"
cp "$TEMP_WORKSPACE/privacy.json" "$OUTPUT_PATH.privacy.json"
echo "$OUTPUT_PATH"
