from fastapi import FastAPI
from sql_request import fetch_classes_from_sql
from preprocessing import preprocess_classes

app = FastAPI()

df = None


@app.get("/")
async def root():
    return {"message": "API działa"}


@app.get("/classes")
async def get_classes():
    global df

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
