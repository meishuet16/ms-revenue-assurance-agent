from __future__ import annotations

import importlib.util
import pathlib
import sys
import traceback


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    test_files = sorted((root / "tests").glob("test_*.py"))
    failures = 0
    total = 0

    for test_file in test_files:
        spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
        if spec is None or spec.loader is None:
            print(f"ERROR {test_file}: cannot import")
            failures += 1
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            print(f"ERROR {test_file}")
            traceback.print_exc()
            failures += 1
            continue

        for name in sorted(dir(module)):
            if not name.startswith("test_"):
                continue
            candidate = getattr(module, name)
            if not callable(candidate):
                continue
            total += 1
            try:
                candidate()
            except Exception:
                print(f"FAIL {test_file.name}::{name}")
                traceback.print_exc()
                failures += 1
            else:
                print(f"PASS {test_file.name}::{name}")

    print(f"{total - failures}/{total} tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
