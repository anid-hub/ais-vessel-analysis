import pandas as pd

from src.vessel_summary import summarize_all_vessels


def test_summarize_all_vessels_returns_one_row_per_vessel():
    df = pd.DataFrame(
        {
            "vessel_id": [
                "vessel_001",
                "vessel_001",
                "vessel_002",
                "vessel_002",
            ],
            "date_time_utc": pd.to_datetime(
                [
                    "2023-01-01 00:00:00",
                    "2023-01-01 01:00:00",
                    "2023-01-01 00:00:00",
                    "2023-01-01 02:00:00",
                ]
            ),
            "latitude": [
                62.0,
                62.01,
                62.1,
                62.12,
            ],
            "longitude": [
                6.0,
                6.01,
                6.1,
                6.12,
            ],
            "speed_over_ground": [
                5.0,
                6.0,
                7.0,
                8.0,
            ],
        }
    )

    result = summarize_all_vessels(df)

    assert len(result) == 2
    assert set(result["vessel_id"]) == {
        "vessel_001",
        "vessel_002",
    }

    assert "total_distance_nm" in result.columns
    assert "distance_avg_speed" in result.columns
    assert "mean_reported_sog" in result.columns

    assert (result["total_distance_nm"] > 0).all()