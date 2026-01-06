def safe_row(df, key):
    if key in df.index:
        values = df.loc[key].iloc[0:2].tolist()
        return {
            "latest": values[0] if len(values) > 0 else None,
            "previous": values[1] if len(values) > 1 else None
        }
    return {"latest": None, "previous": None}
