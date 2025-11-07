from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

# --- Config dataclass ---------------------------------------------------------
@dataclass
class SimulationConfig:
    n: int = 200
    ritual_mu: float = 6.7
    trade_mu: float = 5.9
    symbol_mu: float = 6.3
    hier_mu: float = 6.1
    sigma: float = 1.8
    random_seed: int | None = 42

# --- Output models ------------------------------------------------------------
class NLIS_CRM(BaseModel):
    NLIS: float = Field(..., ge=0)
    CRM: float = Field(..., ge=0)

# --- Core logic ---------------------------------------------------------------
def _bounded_normal(mean: float, sigma: float, size: int, rng: np.random.Generator) -> np.ndarray:
    x = rng.normal(mean, sigma, size)
    return np.clip(x, 1.0, 10.0)

def simulate_block(cfg: SimulationConfig) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.random_seed)
    # Cultural inputs
    C_ritual = _bounded_normal(cfg.ritual_mu, cfg.sigma, cfg.n, rng)
    C_trade  = _bounded_normal(cfg.trade_mu,  cfg.sigma, cfg.n, rng)
    C_symbol = _bounded_normal(cfg.symbol_mu, cfg.sigma, cfg.n, rng)
    C_hier   = _bounded_normal(cfg.hier_mu,   cfg.sigma, cfg.n, rng)

    # Linguistic outcomes (heuristic transforms aligned with ICLHF)
    # Syntax recursion (L1) — ritual + hierarchy
    L_syntax = np.clip(0.55*C_ritual + 0.35*C_hier + rng.normal(0, 0.6, cfg.n), 1, 10)
    # Lexical diversity (L2) — trade
    L_lexdiv = np.clip(0.70*C_trade + 0.15*C_symbol + rng.normal(0, 0.6, cfg.n), 1, 10)
    # Semantic flexibility (L3) — symbolism
    L_semflex = np.clip(0.65*C_symbol + 0.20*C_trade + rng.normal(0, 0.6, cfg.n), 1, 10)
    # Borrowed lexicon (L4) — trade
    L_borrow = np.clip(0.60*C_trade + rng.normal(0, 0.6, cfg.n), 1, 10)

    df = pd.DataFrame({
        "C_ritual": C_ritual, "C_trade": C_trade, "C_symbol": C_symbol, "C_hier": C_hier,
        "L_syntax": L_syntax, "L_lexdiv": L_lexdiv, "L_semflex": L_semflex, "L_borrow": L_borrow,
    })
    return df

def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    # NLIS: integration of syntax, semantics, and lexical capacity
    nlis = 0.35*df["L_syntax"] + 0.30*df["L_semflex"] + 0.25*df["L_lexdiv"] + 0.10*df["L_borrow"]
    # CRM: resilience — trade openness, lexical diversity, and integration
    crm = 0.30*df["C_trade"] + 0.25*df["L_lexdiv"] + 0.25*nlis + 0.20*df["L_borrow"]
    out = df.copy()
    out["NLIS"] = nlis
    out["CRM"] = crm
    return out

# CLI for quick demo
def _cli():
    import argparse
    ap = argparse.ArgumentParser(description="Run VerbaTerra cultural–linguistic simulation")
    ap.add_argument("-n", type=int, default=200, help="Number of cases")
    ap.add_argument("--seed", type=int, default=42, help="Random seed")
    args = ap.parse_args()
    cfg = SimulationConfig(n=args.n, random_seed=args.seed)
    df = compute_scores(simulate_block(cfg))
    print(df.describe(numeric_only=True).round(2))

if __name__ == "__main__":
    _cli()
