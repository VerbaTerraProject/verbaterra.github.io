from verbaterra.sim import SimulationConfig, simulate_block, compute_scores

def test_sim_shapes():
    cfg = SimulationConfig(n=100, random_seed=0)
    df = simulate_block(cfg)
    assert len(df) == 100
    for col in ["C_ritual","C_trade","C_symbol","C_hier","L_syntax","L_lexdiv","L_semflex","L_borrow"]:
        assert col in df.columns

def test_scores():
    cfg = SimulationConfig(n=50, random_seed=1)
    df = compute_scores(simulate_block(cfg))
    assert "NLIS" in df.columns and "CRM" in df.columns
    assert (df["NLIS"] >= 0).all()
    assert (df["CRM"] >= 0).all()
