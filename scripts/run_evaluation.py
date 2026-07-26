from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.local_engine import load_evaluation_cases, score_evaluation_cases


def main() -> int:
    report = score_evaluation_cases(load_evaluation_cases())
    print("Evaluation report")
    for key, value in report.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
