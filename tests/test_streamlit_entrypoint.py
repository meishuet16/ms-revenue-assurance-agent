from __future__ import annotations

import ast
import pathlib


def test_streamlit_entrypoint_removes_local_app_directory_before_importing_package():
    root = pathlib.Path(__file__).resolve().parents[1]
    entrypoint = root / "app" / "app.py"
    source = entrypoint.read_text(encoding="utf-8")

    tree = ast.parse(source)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

    assert "APP_DIR = pathlib.Path(__file__).resolve().parent" in source
    assert "pathlib.Path(path or \".\").resolve() != APP_DIR" in source
    assert "sys.path.insert(0, str(ROOT))" in source
    assert any(
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "pop"
        and call.args
        and isinstance(call.args[0], ast.Constant)
        and call.args[0].value == "app"
        for call in calls
    )


def test_streamlit_entrypoint_wires_expected_dashboard_tabs():
    root = pathlib.Path(__file__).resolve().parents[1]
    entrypoint = root / "app" / "app.py"
    source = entrypoint.read_text(encoding="utf-8")

    assert 'st.tabs(["Summary", "Case Queue", "Evidence Trail", "Flow Map"])' in source
