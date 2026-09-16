"""Phase 14: SHA-256 hash manifest for reproducibility (section 81).

Hashes every file under data/raw, data/story_level, data/final,
data/processed, and the key outputs/ subdirectories, so a later run (or a
different machine) can verify the pipeline reproduced byte-identical
results, and so any silent data drift is detectable.
"""
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

HASH_DIRS = [
    "data/raw",
    "data/story_level",
    "data/final",
    "data/processed",
    "data/derived",
    "outputs/validation",
    "outputs/networks",
    "outputs/matrices",
    "outputs/statistics",
    "outputs/tables",
    "outputs/null_models",
    "outputs/figures",
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    rows = []
    for rel_dir in HASH_DIRS:
        d = ROOT / rel_dir
        if not d.exists():
            continue
        for path in sorted(d.rglob("*")):
            if path.is_file():
                rows.append({
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_of(path),
                })

    df = pd.DataFrame(rows)
    out_path = ROOT / "outputs" / "manifest_sha256.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {out_path} ({len(df)} files hashed)")


if __name__ == "__main__":
    main()
