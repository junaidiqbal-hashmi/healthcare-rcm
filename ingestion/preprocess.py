from pathlib import Path

import pandas as pd

from ingestion.config import get_files_config, get_paths_config
from ingestion.utils import standardize_columns


def main():

    files = get_files_config()["files"]
    paths = get_paths_config()

    source_dir = Path(paths["source"])
    raw_dir = Path(paths["raw"])

    raw_dir.mkdir(parents=True, exist_ok=True)

    for dataset in files:

        logger.info(f"Processing: {dataset['name']}")

        input_file = source_dir / dataset["input_file"]

        # Detect file type automatically
        if input_file.suffix.lower() in [".xlsx", ".xls"]:

            excel_file = pd.ExcelFile(input_file)

            # Match sheet names even if they contain extra spaces
            sheet_name = next(
                (
                    sheet
                    for sheet in excel_file.sheet_names
                    if sheet.strip() == dataset["sheet_name"].strip()
                ),
                None,
            )

            if sheet_name is None:
                raise ValueError(
                    f"Sheet '{dataset['sheet_name']}' not found in '{input_file.name}'.\n"
                    f"Available sheets: {excel_file.sheet_names}"
                )

            df = pd.read_excel(input_file, sheet_name=sheet_name)

        elif input_file.suffix.lower() == ".csv":

            df = pd.read_csv(input_file)

        else:
            raise ValueError(f"Unsupported file type: {input_file.suffix}")

        # Standardize column names
        df.columns = standardize_columns(df.columns)

        # Save CSV
        output_file = raw_dir / dataset["output_file"]
        df.to_csv(output_file, index=False)

        print(f"Rows: {len(df):,}")
        print(f"Saved -> {output_file}")

    print("\n✅ All files processed successfully.")


if __name__ == "__main__":
    main()