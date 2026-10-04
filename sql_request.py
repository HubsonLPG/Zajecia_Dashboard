import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_SERVER = os.getenv("DB_SERVER")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")


QUERY = """
SELECT DISTINCT
    dataOd,
    dataDo,
    TRIM(nazwaSali) AS nazwaSali,
    TRIM(prowadzacy) AS prowadzacy,
    formaZajec,
    TRIM(budynekNazwa) AS budynekNazwa,
    TRIM(NazwaPL) AS NazwaPL
FROM [QS].[v_PlanZajec]
WHERE
    CAST(dataOd AS DATE) >= CAST(GETDATE() AS DATE)
    AND CAST(dataOd AS DATE) < CAST(DATEADD(day, 7, GETDATE()) AS DATE)
    AND (
        LOWER(TRIM(budynekNazwa)) LIKE '%wydział nauk stosowanych%'
        OR LOWER(TRIM(budynekNazwa)) LIKE '%będzin%'
        OR LOWER(TRIM(budynekNazwa)) LIKE '%platforma%'
        OR LOWER(TRIM(budynekNazwa)) LIKE '%clickmeeting%'
    )
"""


def get_connection_string() -> str:
    return (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={PASSWORD};"
        "TrustServerCertificate=yes;"
    )


def fetch_classes_from_sql() -> pd.DataFrame:
    connection_string = get_connection_string()

    with pyodbc.connect(connection_string) as conn:
        df = pd.read_sql(QUERY, conn)

    return df
