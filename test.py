import requests as re
import pandas as pd

r = re.request(method="GET", url="http://127.0.0.1:8000/header")


data = r.json()
df = pd.DataFrame(data)

print(df.head())
