import pandas as pd


def preprocess_classes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.replace("Wydział Nauk Stosowanych", "Dąbrowa")
    df = df.replace("Platforma", "Zajęcia Online")
    df = df.replace("Żywiec Zajęcia Online", "Zajęcia Online")

    df["nazwaSali"] = df["nazwaSali"].astype(str).str.lower()

    df = df[
        ~df["nazwaSali"]
        .str.strip()
        .str.lower()
        .str.contains("odwołane|cancelled", na=False)
    ]

    df.loc[
        df["nazwaSali"].str.contains("teams", case=False, na=False),
        "nazwaSali"
    ] = "teams"

    df["dataOd"] = pd.to_datetime(df["dataOd"])
    df["dataDo"] = pd.to_datetime(df["dataDo"])

    df["Data"] = df["dataOd"].dt.strftime("%Y-%m-%d")
    df["godzinaOd"] = df["dataOd"].dt.strftime("%H:%M")
    df["godzinaDo"] = df["dataDo"].dt.strftime("%H:%M")

    df = df.drop(columns=["NazwaPL", "formaZajec", "dataOd", "dataDo"])

    return df
