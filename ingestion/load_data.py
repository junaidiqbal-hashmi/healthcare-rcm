from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from ingestion.config import (
    get_database_config,
    get_files_config,
    get_paths_config,
    get_schemas_config,
)


def main():

    # Load configurations
    database = get_database_config()
    files = get_files_config()["files"]
    paths = get_paths_config()
    schemas = get_schemas_config()

    # Create database connection URL
    connection_url = (
        f"postgresql+psycopg://"
        f"{database['user']}:{database['password']}"
        f"@{database['host']}:{database['port']}/"
        f"{database['database']}"
    )

    engine = create_engine(connection_url)

    raw_dir = Path(paths["raw"])

    # Create Bronze schema
    with engine.begin() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS bronze")
        )

    # Load each dataset
    for dataset in files:

        dataset_name = dataset["name"]
        output_file = dataset["output_file"]

        csv_file = raw_dir / output_file

        print(f"\nLoading: {dataset_name}")

        # Get schema configuration for this dataset
        schema = schemas[dataset_name]

        dtype = schema.get("dtype", {})
        parse_dates = schema.get("parse_dates", [])

        # Read CSV with explicit data types
        df = pd.read_csv(
            csv_file,
            dtype=dtype,
            parse_dates=parse_dates,
        )

        table_name = dataset_name

        df.to_sql(
            name=table_name,
            con=engine,
            schema="bronze",
            if_exists="replace",
            index=False,
            chunksize=1000,
        )

        print(
            f"Loaded {len(df):,} rows "
            f"into bronze.{table_name}"
        )

    engine.dispose()

    print("\nAll datasets loaded successfully.")


if __name__ == "__main__":
    main()