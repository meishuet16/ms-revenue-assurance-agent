from __future__ import annotations

import pathlib
import sys
import importlib.util


def test_streamlit_entrypoint_imports_without_package_shadowing():
    root = pathlib.Path(__file__).resolve().parents[1]
    entrypoint = root / "app" / "app.py"
    spec = importlib.util.spec_from_file_location("app", entrypoint)

    assert spec is not None
    assert spec.loader is not None

    previous_app = sys.modules.pop("app", None)
    previous_path = list(sys.path)
    sys.path.insert(0, str(entrypoint.parent))
    module = importlib.util.module_from_spec(spec)
    sys.modules["app"] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = previous_path
        sys.modules.pop("app", None)
        if previous_app is not None:
            sys.modules["app"] = previous_app
