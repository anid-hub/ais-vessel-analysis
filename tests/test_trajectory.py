import pandas as pd

from src.trajectory import (
    get_vessel_track,
    haversine_distance_nm,
    add_distance_travelled,
)


def test_get_vessel_track_filters_and_sorts():
    df = pd.DataFrame(
        {
            "vessel_id": [
                "vessel_001",
                "vessel_002",
                "vessel_001",
            ],
            "date_time_utc": pd.to_datetime(
                [
                    "2023-01-01 00:10:00",
                    "2023-01-01 00:05:00",
                    "2023-01-01 00:00:00",
                ]
            ),
            "latitude": [62.1, 62.2, 62.0],
            "longitude": [6.1, 6.2, 6.0],
        }
    )

    result = get_vessel_track(df, "vessel_001")

    assert len(result) == 2
    assert result.iloc[0]["date_time_utc"] < result.iloc[1]["date_time_utc"]


def test_haversine_zero_distance():
    distance = haversine_distance_nm(
        62.0,
        6.0,
        62.0,
        6.0,
    )

    assert distance == 0


def test_add_distance_travelled_starts_at_zero():
    track = pd.DataFrame(
        {
            "date_time_utc": pd.to_datetime(
                [
                    "2023-01-01 00:00:00",
                    "2023-01-01 00:10:00",
                ]
            ),
            "latitude": [62.0, 62.01],
            "longitude": [6.0, 6.01],
        }
    )

    result = add_distance_travelled(track)

    assert result.iloc[0]["distance_nm"] == 0
    assert result.iloc[1]["distance_nm"] > 0