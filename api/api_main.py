from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np

app = FastAPI(title="VerbaTerra API", version="0.1.0")

class SimIn(BaseModel):
    n: int = Field(ge=1, le=5000, default=300)
    ritual_mu: float = 6.7
    trade_mu: float = 5.9
    symbol_mu: float = 6.3
    hier_mu: float = 6.1
    sigma: float = 1.8
    seed: int = 42

class SimOut(BaseModel):
    nlis_mean: float
    crm_mean: float

def _bounded_normal(mean: float, sigma: float, size: int, rng: np.random.Generator):
    x = rng.normal(mean, sigma, size)
    return np.clip(x, 1.0, 10.0)

@app.get("/healthz")
def health():
    return {"ok": True}

@app.post("/simulate", response_model=SimOut)
def simulate(inp: SimIn):
    rng = np.random.default_rng(inp.seed)
    C_ritual = _bounded_normal(inp.ritual_mu, inp.sigma, inp.n, rng)
    C_trade  = _bounded_normal(inp.trade_mu,  inp.sigma, inp.n, rng)
    C_symbol = _bounded_normal(inp.symbol_mu, inp.sigma, inp.n, rng)
    C_hier   = _bounded_normal(inp.hier_mu,   inp.sigma, inp.n, rng)

    L_syntax  = np.clip(0.55*C_ritual + 0.35*C_hier + rng.normal(0, 0.6, inp.n), 1, 10)
    L_lexdiv  = np.clip(0.70*C_trade + 0.15*C_symbol + rng.normal(0, 0.6, inp.n), 1, 10)
    L_semflex = np.clip(0.65*C_symbol + 0.20*C_trade + rng.normal(0, 0.6, inp.n), 1, 10)
    L_borrow  = np.clip(0.60*C_trade + rng.normal(0, 0.6, inp.n), 1, 10)

    nlis = 0.35*L_syntax + 0.30*L_semflex + 0.25*L_lexdiv + 0.10*L_borrow
    crm  = 0.30*C_trade + 0.25*L_lexdiv + 0.25*nlis + 0.20*L_borrow

    return {"nlis_mean": float(nlis.mean()), "crm_mean": float(crm.mean())}
