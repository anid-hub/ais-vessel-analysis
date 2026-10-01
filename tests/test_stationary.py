import pandas as pd

from src.stationary import detect_stationary_periods


def test_detect_stationary_period():
    track = pd.DataFrame(
        {
            "date_time_utc": pd.to_datetime(
                [
                    "2023-01-01 00:00:00",
                    "2023-01-01 00:05:00",
                    "2023-01-01 00:15:00",
                    "2023-01-01 00:20:00",
                ]
            ),
            "speed_over_ground": [
                0.1,
                0.2,
                0.1,
                5.0,
            ],
            "latitude": [62.0, 62.0, 62.0, 62.1],
            "longitude": [6.0, 6.0, 6.0, 6.1],
        }
    )

    result = detect_stationary_periods(
        track,
        speed_threshold=0.5,
        min_duration_minutes=10,
    )

    assert len(result) == 1
    assert result.iloc[0]["duration_minutes"] == 15


def test_large_gap_splits_stationary_periods():
    track = pd.DataFrame(
        {
            "date_time_utc": pd.to_datetime(
                [
                    "2023-01-01 00:00:00",
                    "2023-01-01 00:10:00",
                    "2023-01-01 01:00:00",
                    "2023-01-01 01:10:00",
                ]
            ),
            "speed_over_ground": [
                0.1,
                0.1,
                0.1,
                0.1,
            ],
            "latitude": [62.0, 62.0, 62.0, 62.0],
            "longitude": [6.0, 6.0, 6.0, 6.0],
        }
    )

    result = detect_stationary_periods(
        track,
        speed_threshold=0.5,
        min_duration_minutes=5,
        max_gap_minutes=30,
    )

    assert len(result) == 2