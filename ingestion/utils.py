import re


def standardize_columns(columns):
    """
    Convert column names to snake_case.
    Example:
    Patient Number -> patient_number
    CPT Code -> cpt_code
    """
    cleaned = []

    for col in columns:
        col = str(col).strip().lower()
        col = re.sub(r"[()%/]", "", col)
        col = re.sub(r"[\s\-]+", "_", col)
        col = re.sub(r"_+", "_", col)

        cleaned.append(col)

    return cleaned