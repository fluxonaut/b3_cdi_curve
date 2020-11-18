import os
import pandas as pd
from typing import Tuple


def check_create_output_folder(output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)


def save_dataframe(df: pd.DataFrame, df_name: str, output_dir):
    df_path = output_dir + df_name
    df.to_csv(df_path, index=False, compression="gzip")


def get_local_dataframe(df_name: str, output_dir) -> Tuple[bool, pd.DataFrame]:

    filepath = output_dir + df_name
    if os.path.isfile(filepath):
        return (
            True,
            pd.read_csv(filepath, compression="gzip").astype(
                {"duration": int, "base252": float, "base360": float}
            ),
        )
    return (False, None)
