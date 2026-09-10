import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const galleryRoot = path.resolve(here, "..");
const sourcePath = "D:\\GitHub Program\\guizang-ppt-skill";
const expectedIds = [
  "guizang-ink-classic",
  "guizang-indigo-porcelain",
  "guizang-forest-ink",
  "guizang-kraft-paper",
  "guizang-dune",
  "guizang-swiss-ikb",
  "guizang-swiss-lemon-yellow",
  "guizang-swiss-lemon-green",
  "guizang-swiss-safety-orange",
];

function readWebpDimensions(buffer) {
  assert.equal(buffer.subarray(0, 4).toString("ascii"), "RIFF");
  assert.equal(buffer.subarray(8, 12).toString("ascii"), "WEBP");
  const chunk = buffer.subarray(12, 16).toString("ascii");
  if (chunk === "VP8X") {
    return {
      width: buffer.readUIntLE(24, 3) + 1,
      height: buffer.readUIntLE(27, 3) + 1,
    };
  }
  assert.equal(chunk, "VP8 ");
  assert.equal(buffer.subarray(23, 26).toString("hex"), "9d012a");
  return {
    width: buffer.readUInt16LE(26) & 0x3fff,
    height: buffer.readUInt16LE(28) & 0x3fff,
  };
}

test("exposes every built-in Guizang theme as a named catalog item", async () => {
  // Given: the editable generator catalog source.
  const generators = JSON.parse(
    await readFile(path.join(galleryRoot, "data", "generators-source.json"), "utf8"),
  );

  // When: entries backed by the Guizang project are selected.
  const variants = generators.filter((item) => item.source === sourcePath);

  // Then: all nine themes remain independently named and previewable.
  assert.deepEqual(variants.map((item) => item.id), expectedIds);
  assert.equal(new Set(variants.map((item) => item.poster)).size, expectedIds.length);
  for (const variant of variants) {
    assert.match(variant.name, /^归藏 - .+风格$/u);
    const poster = await readFile(path.join(galleryRoot, variant.poster));
    assert.deepEqual(readWebpDimensions(poster), { width: 1600, height: 1200 });
  }
});
