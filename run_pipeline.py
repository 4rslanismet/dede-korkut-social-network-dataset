#!/usr/bin/env python
"""Master pipeline orchestrator (section 75, 119).

Usage:
    python run_pipeline.py --all
    python run_pipeline.py --stage audit
    python run_pipeline.py --stage null_models --fast
    python run_pipeline.py --all --fast          # fast null-model mode for development
    python run_pipeline.py --all --validate-only # stop after the validation gate (CI use)

Each stage is a standalone script under src/ (also independently runnable).
This orchestrator just runs them in the documented order and stops on the
first failure, printing a clear PASS/WARNING/FAIL summary at the end
(section 80).
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
LOGS = ROOT / "logs"

# Order matches section 75's 16-step description, mapped onto the scripts
# actually implemented in this repository.
STAGES = [
    ("audit", "audit.py", []),
    ("validate", "validate.py", []),
    ("entity_resolution", "entity_resolution.py", []),
    ("build_canonical", "build_canonical.py", []),
    ("build_networks", "build_networks.py", []),
    ("story_networks", "story_networks.py", []),
    ("metrics", "metrics.py", []),
    ("communities", "communities.py", []),
    ("signed_and_directed", "signed_and_directed.py", []),
    ("multilayer", "multilayer.py", []),
    ("narrative_order", "narrative_order.py", []),
    ("null_models", "null_models.py", ["--fast"]),  # arg only appended when --fast passed to this orchestrator
    ("null_models_fdr", "null_models_fdr.py", []),
    ("sensitivity", "sensitivity.py", []),
    ("robustness", "robustness.py", []),
    ("visualization", "visualization.py", []),
    ("export_tables", "export_tables.py", []),
    ("build_inter_annotator_sample", "build_inter_annotator_sample.py", []),
    ("inter_annotator_stats", "inter_annotator_stats.py", []),
    ("hash_manifest", "build_hash_manifest.py", []),
]

STAGE_NAMES = [s[0] for s in STAGES]


def run_stage(name: str, script: str, fast_args: list[str], fast: bool, log_dir: Path) -> tuple[bool, str]:
    script_path = SRC / script
    args = [sys.executable, str(script_path)]
    if fast and name == "null_models":
        args.extend(fast_args)

    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_path = log_dir / f"{timestamp}_{name}.log"

    print(f"\n{'='*70}\nSTAGE: {name}  ({script})\n{'='*70}")
    with open(log_path, "w", encoding="utf-8") as logf:
        proc = subprocess.run(args, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        logf.write(proc.stdout or "")
    print(proc.stdout[-3000:] if proc.stdout else "(no output)")

    ok = proc.returncode == 0
    if not ok:
        print(f"STAGE FAILED: {name} (exit code {proc.returncode}) - see {log_path}")
    return ok, str(log_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--all", action="store_true", help="run every stage in order")
    parser.add_argument("--stage", choices=STAGE_NAMES, help="run a single named stage")
    parser.add_argument("--fast", action="store_true", help="use fast mode for null_models (n_random=100 instead of config's 1000)")
    parser.add_argument("--validate-only", action="store_true", help="stop after the validate stage (for CI)")
    args = parser.parse_args()

    if not args.all and not args.stage:
        parser.error("specify --all or --stage <name>")

    stages_to_run = STAGES
    if args.stage:
        stages_to_run = [s for s in STAGES if s[0] == args.stage]
    if args.validate_only:
        idx = STAGE_NAMES.index("validate")
        stages_to_run = STAGES[: idx + 1]

    results = []
    for name, script, fast_args in stages_to_run:
        ok, log_path = run_stage(name, script, fast_args, args.fast, LOGS)
        results.append((name, ok, log_path))
        if not ok:
            break

    print(f"\n{'='*70}\nPIPELINE SUMMARY\n{'='*70}")
    all_ok = all(ok for _, ok, _ in results)
    for name, ok, log_path in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  (log: {log_path})")

    n_ran = len(results)
    n_total = len(stages_to_run)
    if n_ran < n_total:
        print(f"\nSTOPPED EARLY: {n_ran}/{n_total} stages ran before a failure.")

    print(f"\nVALIDATION STATUS: {'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
