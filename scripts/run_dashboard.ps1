$ErrorActionPreference = "Stop"

python -m streamlit run app/app.py `
    --server.port=8501 `
    --server.headless=true `
    --server.fileWatcherType=none `
    --browser.gatherUsageStats=false

