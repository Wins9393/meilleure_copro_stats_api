def calcul_stats(df):
    if "condominium_expenses" not in df.columns:
        raise ValueError("La colonne 'condominium_expenses' est introuvable")
    
    series = df["condominium_expenses"].dropna().astype(float)
    if series.empty:
        return {"average": None, "quantile_10": None, "quantile_90": None}

    return {
        "average":     round(series.mean(), 2),
        "quantile_10": round(series.quantile(0.10), 2),
        "quantile_90": round(series.quantile(0.90), 2)
    }