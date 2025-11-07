# Usage

## Streamlit UI
```bash
pip install -e ".[ui]"
streamlit run app/streamlit_app.py
```

## Library
```python
from verbaterra.sim import SimulationConfig, simulate_block, compute_scores
cfg = SimulationConfig(n=400, random_seed=42)
df = compute_scores(simulate_block(cfg))
print(df.head())
```
