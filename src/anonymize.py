import pandas as pd


def anonymize_ais_data(df):
    """
    Anonymize sensitive vessel identifiers in an AIS DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        AIS dataset containing vessel identifiers.

    Returns
    -------
    pandas.DataFrame
        A copy of the dataset with anonymized vessel IDs.
    """

    df = df.copy()

    unique_mmsi = df["mmsi"].dropna().unique()

    mmsi_map = {
        mmsi: f"vessel_{i:03d}"
        for i, mmsi in enumerate(unique_mmsi, start=1)
    }

    df["vessel_id"] = df["mmsi"].map(mmsi_map)

    columns_to_remove = [
        "mmsi",
        "imo",
        "callsign",
        "ship_name",
    ]

    df = df.drop(
        columns=columns_to_remove,
        errors="ignore",
    )

    return df