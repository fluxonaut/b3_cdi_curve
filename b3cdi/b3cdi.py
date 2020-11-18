from datetime import date
from rich.console import Console
from rich.progress import Progress

import numpy as np
import pandas as pd
import requests
from .database import get_db_connection, get_latest_date, insert_data
from .files_utils import check_create_output_folder, get_local_dataframe, save_dataframe
from .scrapper import parse_html
from pandas.tseries.offsets import BDay

console = Console(log_path=False)


def create_time_series(duration: int, output_dir="output/"):

    console.log(f"Creating time series for ({duration})...")

    check_create_output_folder(output_dir)

    db_conn = get_db_connection(output_dir)
    db_cursor = db_conn.cursor()

    query = f"SELECT date, base252, base360 FROM cdi WHERE duration={duration};"
    db_cursor.execute(query)
    result = db_cursor.fetchall()

    db_cursor.close()
    db_conn.close()

    df = pd.DataFrame(result, columns=["date", "base252", "base360"]).astype(
        {"date": np.datetime64, "base252": float, "base360": float}
    )

    filename = output_dir + f"cdi_duration{duration}.csv"

    df.to_csv(filename, index=False)
    console.log(f"Series saved to {filename}")


def sync_db(save_all_files: bool = False, verbose: bool = False, output_dir="output/"):
    initial_date = date(year=2020, month=8, day=8)
    latest_date = date.today() - BDay(1)

    check_create_output_folder(output_dir)

    db_conn = get_db_connection(output_dir)

    db_has_entries, last_db_date = get_latest_date(db_conn)

    start_date = last_db_date + BDay(1) if db_has_entries else initial_date

    working_days = pd.bdate_range(start=start_date, end=latest_date)
    if len(working_days):
        if db_has_entries:
            console.log("Updating existing database...")
        else:
            console.log("Creating new database...")

        with Progress() as progress:
            task = progress.add_task("Starting job", total=len(working_days))
            for day in working_days:
                process_day(day, output_dir, db_conn, save_all_files)
                progress.update(task, description=day.strftime("%d/%m/%Y"), advance=1)

    db_conn.close()


def process_day(day, output_dir, db_conn, save_all_files=False):
    filename = f"CDI_Curve_{day}.gzip"
    has_local_file, local_df = get_local_dataframe(filename, output_dir)

    if has_local_file:
        insert_data(day, local_df, db_conn)
        return

    url = (
        "http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-taxas-referenciais-bmf-ptBR.asp?Data="
        f"{day.strftime('%d/%m/%Y')}"
        "&slcTaxa=PRE"
    )

    html_content = requests.post(url).text

    if "Não há dados para a data" in html_content:
        return

    success_parsing, df = parse_html(html_content)

    if not success_parsing:
        return

    insert_data(day, df, db_conn)

    if save_all_files:
        save_dataframe(df, filename, output_dir)
