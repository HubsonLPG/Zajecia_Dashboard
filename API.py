from fastapi import FastAPI

from preprocessing import preprocess_classes
from sql_request import fetch_classes_from_sql

app = FastAPI()

raw_df = fetch_classes_from_sql()
df = preprocess_classes(raw_df)


@app.get("/")
async def root():
    return {"message": "API działa"}


@app.get("/classes")
async def get_classes():
    global df  # noqa: PLW0602

    if df is None:
        return {
            "message": "Brak danych. Najpierw wejdź na classes/refresh"
        }

    return df.to_dict(orient="records")


@app.get("/classes/refresh")
async def refresh():
    global df

    raw_df = fetch_classes_from_sql()
    df = preprocess_classes(raw_df)

    return {
        "message": "Dane odświeżone",
        "rows": len(df)
    }
