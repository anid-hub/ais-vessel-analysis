import pandas as pd


def load_ports(file_path):
    """
    Load port definitions from a CSV file.

    Expected columns:
    - name
    - latitude
    - longitude
    - radius_nm
    """

    ports = pd.read_csv(file_path)

    required_columns = {
        "name",
        "latitude",
        "longitude",
        "radius_nm",
    }

    missing = required_columns - set(ports.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    return ports.to_dict(orient="records")