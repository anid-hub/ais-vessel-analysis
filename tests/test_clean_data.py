import pandas as pd

from src.clean_data import clean_ais_data


def test_clean_data_removes_invalid_rows_and_duplicates():
    df = pd.DataFrame(
        {
            "date_time_utc": pd.to_datetime(
                [
                    "2023-01-01 00:00:00",
                    "2023-01-01 00:00:00",
                    None,
                    "2023-01-01 00:05:00",
                ]
            ),
            "vessel_id": [
                "vessel_001",
                "vessel_001",
                "vessel_002",
                "vessel_003",
            ],
            "latitude": [
                62.5,
                62.5,
                62.4,
                95.0,
            ],
            "longitude": [
                6.1,
                6.1,
                6.2,
                6.3,
            ],
        }
    )

    result = clean_ais_data(df)

    assert len(result) == 1
    assert result.iloc[0]["vessel_id"] == "vessel_001"