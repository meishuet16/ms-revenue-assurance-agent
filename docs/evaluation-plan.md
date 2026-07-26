# Evaluation Plan

The project evaluates twelve synthetic cases across:

- 2 valid pricing updates
- 2 valid concessions
- 2 expired or conditional exceptions
- 2 conflicting usage-data cases
- 2 effective-date boundary cases
- 2 fully normal billing cases

Metrics:

- variance detection recall;
- classification accuracy;
- false-positive rate;
- evidence citation completeness;
- unsafe action rate;
- monetary calculation accuracy.

Run:

```bash
python scripts/run_evaluation.py
```

