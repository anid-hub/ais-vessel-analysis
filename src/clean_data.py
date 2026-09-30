import pandas as pd


def clean_ais_data(df):
    """
    Clean AIS data by removing invalid or unusable observations.

    Parameters
    ----------
    df : pandas.DataFrame
        AIS dataset.

    Returns
    -------
    pandas.DataFrame
        Cleaned AIS dataset.
    """

    df = df.copy()

    # Remove rows without essential fields
    df = df.dropna(
        subset=[
            "date_time_utc",
            "latitude",
            "longitude",
        ]
    )

    # Keep only valid geographic coordinates
    df = df[
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    ]

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Sort chronologically
    sort_columns = ["date_time_utc"]

    if "vessel_id" in df.columns:
        sort_columns = ["vessel_id", "date_time_utc"]
    elif "mmsi" in df.columns:
        sort_columns = ["mmsi", "date_time_utc"]

    df = df.sort_values(sort_columns)

    return df.reset_index(drop=True)