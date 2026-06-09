# Dede Korkut Social Network Dataset

A reproducible social network dataset derived from the narratives of the Book of Dede Korkut.

## Overview

This repository contains a curated and standardized social network dataset generated from the narratives of the Book of Dede Korkut. The dataset was developed through a multi-stage process including manual coding, entity normalization, alias resolution, contextual standardization, and network construction.

The resulting dataset can be directly used for:

- Social Network Analysis (SNA)
- Complex Network Research
- Digital Humanities Studies
- Literary Network Analysis
- Narrative Structure Analysis

## Dataset Statistics

| Metric | Value |
|----------|----------|
| Stories | 14 |
| Nodes | 333 |
| Edges | 628 |
| Narrative Events | 85 |

## Repository Structure

```text
data/
├── final/
│   ├── dede_korkut_dugumler_temiz.csv
│   ├── dede_korkut_kenarlar_temiz.csv
│   ├── dede_korkut_olaylar_temiz.csv
│   ├── dede_korkut_alias_sozlugu.csv
│   ├── dede_korkut_degisim_logu.csv
│   └── 00_boy_dataset_indeksi_temiz.csv

docs/
├── README_v2.md
└── README_v3.md
```

## Dataset Versions

### Version 1 (Raw Coding Dataset)

Initial manually coded character and relationship data extracted from individual narratives.

### Version 2 (Standardized Dataset)

Entity normalization and contextual disambiguation were applied.

### Version 3 (Final Research Dataset)

Additional semantic standardization, alias resolution, event extraction, and quality control procedures were completed.

## Files

### Node List

`dede_korkut_dugumler_temiz.csv`

Contains all identified narrative actors and their attributes.

### Edge List

`dede_korkut_kenarlar_temiz.csv`

Contains relationships between actors.

### Event List

`dede_korkut_olaylar_temiz.csv`

Contains narrative events that could not be represented as network edges.

## Potential Research Applications

- Degree Centrality Analysis
- Betweenness Centrality Analysis
- Community Detection
- Narrative Network Comparison
- Character Importance Ranking
- Comparative Literary Network Analysis

## Citation

If you use this dataset in academic work, please cite the repository and associated publications.

## License

CC BY 4.0
