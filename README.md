# Preferred-Axis Geometry Constraint Screen

This repository contains the frozen publication inputs needed to verify the
numerical comparisons reported in:

**Testing a Proposed Rotational Pole Against Earth's Preferred-Axis Geometry**

## Contents

- `paper/Buchanan_preferred_axis_geometry.pdf` - public paper
- `paper/figures/` - publication figures
- `data/` - compact result tables used in the paper
- `validation/` - public validation summaries
- `code/verify_reported_results.py` - standalone verification script

## Verify

```bash
python -m pip install -r requirements.txt
python code/verify_reported_results.py
```

A successful run exits with status 0 and reports no failed checks.

## Reproducibility scope

This package verifies the reported comparisons from frozen machine readable
publication outputs. It does not reconstruct the calculations from raw
three dimensional tomography volumes.

Working notebooks, raw model volumes, cleaned intermediate datasets, helper
functions, internal development records, local file locations, and upstream
preprocessing pipelines are intentionally excluded.

## Main result

The family-balanced lowermost selected-axis center is near 1.02 degrees S,
17.24 degrees E in the candidate-facing representation. The proposed coordinate
lies 18.81 degrees away, outside the empirical 99% family-bootstrap radius of
3.04 degrees. The containment classification is `unsupported`.

The primary static-gravity maximum and one UNICA25 lowermost tensor are closer
secondary geometric comparisons. They do not replace the pooled containment
classification.

## Citation

Buchanan, Stephanie. 2026. *Testing a Proposed Rotational Pole Against Earth’s
Preferred-Axis Geometry*  Independent geophysical modeling case study.

## Author

Stephanie Buchanan, M.S.
_Independent Researcher in Geophysical Modeling_
