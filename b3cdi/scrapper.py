from typing import Tuple
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def parse_html(html_content: str) -> Tuple[bool, pd.DataFrame]:

    soup = BeautifulSoup(html_content, "html5lib")
    table = soup.find("table", attrs={"id": "tb_principal1"})

    if table is None:
        return (False, None)

    dtypes = np.dtype(
        [
            ("duration", int),
            ("base252", float),
            ("base360", float),
        ]
    )
    data = np.empty(0, dtype=dtypes)
    df = pd.DataFrame(data)

    for i, tr in enumerate(table.find_all("tr")[2:]):
        row = []
        for td in tr.find_all("td"):
            content = td.text
            if "," in content:
                row.append(float(content.replace(".", "").replace(",", ".")))
            else:
                row.append(int(content))
        df.loc[i] = row

    df_full = pd.DataFrame(
        {
            "duration": pd.Series(
                np.array(list(range(1, int(df["duration"].iloc[-1]) + 1)))
            ).astype(int)
        }
    )

    df_full = df_full.merge(df, on="duration", how="left")
    df_full.interpolate(method="polynomial", order=3, inplace=True)

    return (True, df_full)
