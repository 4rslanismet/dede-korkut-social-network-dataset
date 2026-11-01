# AI Assistance Disclosure

## Overview

This repository uses **Claude Code** (Anthropic) as an AI-assisted software and
research-engineering tool. This document transparently discloses the nature, scope,
and limitations of that assistance.

## What Claude Code Was Used For

Claude Code served as a development and research-engineering assistant for:

- **Repository auditing**: structural inspection, schema validation, consistency checks
- **Python implementation**: pipeline scripts, analysis modules, data-processing code
- **Validation tooling**: automated tests, hash manifests, release-consistency checks
- **Reproducibility infrastructure**: pipeline orchestration, deterministic seed management
- **Network-analysis implementation**: graph construction, metric computation, statistical tests
- **Website generation**: GitHub Pages site build from pipeline outputs
- **Documentation consistency checking**: cross-referencing claims against computed outputs
- **Test generation**: pytest suite for schema integrity, metric correctness, etc.
- **Code review**: identifying bugs, verifying weight semantics, checking edge cases
- **Artifact generation**: figures, tables, CSV/JSON exports

## What Claude Code Is NOT

- **Claude is not a human author.** It must not be listed as a human researcher or
  co-author on any publication, thesis, or citation record derived from this work.
- **Claude is not a domain expert.** It does not have specialist knowledge of Turkic
  epic literature, the Book of Dede Korkut, or the specific source editions used.
- **Claude is not a substitute for peer review.** All scientific claims require
  independent human validation.

## Responsibility and Oversight

- **Final scientific responsibility** belongs to the human researcher(s) who own
  this repository and any publications derived from it.
- **Dataset interpretation** — including which entities are distinct characters,
  how relations map to social-network concepts, and what the narrative structure
  implies — requires human domain expertise and judgment.
- **Source-edition decisions** — which edition of the Book of Dede Korkut was coded,
  how transcription choices affect the dataset — are exclusively human decisions.
- **Entity-resolution judgments** — whether composite node labels represent one actor
  or multiple, whether aliases refer to the same person — require human review.
- **Publication claims** — what the data support, what they do not, how findings
  should be framed — are the responsibility of the human author(s).

## Validation Requirements

All AI-generated code and results are validated through:

1. **Deterministic scripts**: every analysis step is a reproducible Python script
   reading parameters from `config/analysis.yaml`.
2. **Automated tests**: a pytest suite checks schema integrity, metric correctness,
   weight semantics, and cross-artifact consistency.
3. **Hash manifests**: SHA-256 hashes of source data and generated outputs.
4. **Pipeline reproducibility**: `python run_pipeline.py --all` regenerates every
   output from source data.

## What Must Not Be Invented by AI

- Literary facts not present in the coded dataset
- Source-edition metadata not documented in the repository
- Author names, affiliations, ORCIDs, or DOIs
- Inter-annotator agreement statistics (requires actual second-human annotations)
- Bibliographic references (must be verified by a human researcher)

## Acknowledgment Format

Claude Code may be acknowledged in publications as:

> AI-assisted development tool (Claude Code, Anthropic)

It should appear in an acknowledgments section or a methods note about tooling —
never in an author list.
