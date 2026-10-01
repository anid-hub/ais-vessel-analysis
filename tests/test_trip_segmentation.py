import pandas as pd

from src.trip_segmentation import (
    assign_trip_ids,
    summarize_trips,
)


def test_assign_trip_ids_splits_on_large_gap():
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
            "latitude": [62.0, 62.01, 62.1, 62.11],
            "longitude": [6.0, 6.01, 6.1, 6.11],
        }
    )

    result = assign_trip_ids(
        track,
        gap_minutes=30,
    )

    assert result["trip_id"].nunique() == 2
    assert list(result["trip_id"]) == [1, 1, 2, 2]


def test_summarize_trips_returns_one_row_per_trip():
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
            "latitude": [62.0, 62.01, 62.1, 62.11],
            "longitude": [6.0, 6.01, 6.1, 6.11],
        }
    )

    segmented = assign_trip_ids(
        track,
        gap_minutes=30,
    )

    summary = summarize_trips(segmented)

    assert len(summary) == 2
    assert list(summary["trip_id"]) == [1, 2]