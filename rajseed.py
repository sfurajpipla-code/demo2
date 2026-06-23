import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import marimo as mo

    return (pl,)


@app.cell
def _(pl):
    df = pl.read_csv("Nursery1806.csv", infer_schema_length=10000)
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df, pl):
    item_schema = pl.List(
        pl.Struct([
            pl.Field("name", pl.String),
            pl.Field("nursery", pl.String),
            pl.Field("quantity", pl.Int64),
            pl.Field("price", pl.Float64),
            pl.Field("cpts", pl.List(
                pl.Struct([
                    pl.Field("no", pl.String), # can change to pl.Int64 if CPT numbers are strictly integers
                    pl.Field("qty", pl.Int64)
                ])
            ))
        ])
    )

    df_parsed = df.with_columns([
        pl.col("Items").str.json_decode(dtype=item_schema)
    ])
    return (df_parsed,)


@app.cell
def _(df_parsed):
    df_exploded = df_parsed.explode("Items").unnest("Items")
    return (df_exploded,)


@app.cell
def _(df_exploded):
    df_exploded
    return


@app.cell
def _(df_exploded):
    df_cpt_granular = df_exploded.explode("cpts").unnest("cpts")
    return (df_cpt_granular,)


@app.cell
def _(df_cpt_granular):
    df_cpt_granular
    return


@app.cell
def _(df_cpt_granular, pl):
    kk= df_cpt_granular.group_by("nursery").agg(pl.col("qty").sum())
    return (kk,)


@app.cell
def _(kk):
    kk
    return


if __name__ == "__main__":
    app.run()
