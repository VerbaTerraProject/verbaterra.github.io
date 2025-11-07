# VerbaTerra Simulation Lab (vSION demo)

A lightweight, reproducible repo that **runs cultural–linguistic simulations** and **demonstrates the project’s capabilities with a UI** (Streamlit) + a small Python package.

## Quick Start

### Option A — Local (Python 3.10+)
```bash
pip install -e ".[dev,ui]"
streamlit run app/streamlit_app.py
```

### Option B — GitHub Codespaces
1. Open this repo in a new Codespace (default settings).
2. In the terminal, run:
   ```bash
   pip install -e ".[dev,ui]" && streamlit run app/streamlit_app.py --server.port 7860 --server.address 0.0.0.0
   ```
3. Forward the port that Streamlit prints and open in the browser.

### Option C — Just the library
```bash
python -m verbaterra.sim --help
```

## What’s inside

- `src/verbaterra/` — Python package with the simulation core and scoring (NLIS, CRM).
- `app/streamlit_app.py` — UI: sliders for cultural inputs, on-the-fly simulation, plots, and exports.
- `tests/` — Pytest suite for core logic.
- `docs/` + `mkdocs.yml` — Minimal docs, deployable to GitHub Pages.
- `.github/workflows/` — CI for tests + Docs build.
- `.devcontainer/` — Codespaces config.

## Notes
- This demo follows your ICLHF/CALR setup (Ritual, Trade, Symbolism, Hierarchy → NLIS/CRM). 
- No external services are required — everything runs locally or in Codespaces.
- You can extend the model, add datasets, or attach notebooks in `notebooks/`.


## React + FastAPI dashboard

### Run with Docker Compose
```bash
docker compose up --build
```
- **API (FastAPI)**: http://localhost:8000
- **Streamlit**: http://localhost:8501
- **React dashboard (Vite)**: http://localhost:5173 (uses `VITE_API_BASE` to call the API)

### Local (no Docker)
API:
```bash
cd api
python -m pip install -e .
uvicorn api_main:app --reload
```
Webapp:
```bash
cd webapp
npm install
npm run dev
```
Set `VITE_API_BASE=http://localhost:8000` when building or via `.env`.

### Deploying the dashboard to GitHub Pages
This repo already deploys **docs** to Pages. To publish the React app instead, run the manual workflow
**Webapp Deploy (Manual)** in Actions; it will push the SPA build to Pages. Remember only one Pages site can be active at a time.
