import pandas as pd

from src.port_calls import detect_port_calls


def test_detect_port_call_within_radius():
    stationary_periods = pd.DataFrame(
        {
            "start_time": pd.to_datetime(
                ["2023-01-01 00:00:00"]
            ),
            "end_time": pd.to_datetime(
                ["2023-01-01 01:00:00"]
            ),
            "messages": [10],
            "mean_latitude": [62.5025],
            "mean_longitude": [6.0655],
            "mean_speed": [0.1],
            "max_speed": [0.2],
            "duration_minutes": [60.0],
        }
    )

    ports = [
        {
            "name": "Test Port",
            "latitude": 62.5025,
            "longitude": 6.0655,
            "radius_nm": 0.5,
        }
    ]

    result = detect_port_calls(
        stationary_periods,
        ports,
    )

    assert len(result) == 1
    assert result.iloc[0]["port_name"] == "Test Port"
    assert result.iloc[0]["distance_to_port_nm"] == 0


def test_stationary_period_outside_port_is_not_returned():
    stationary_periods = pd.DataFrame(
        {
            "start_time": pd.to_datetime(
                ["2023-01-01 00:00:00"]
            ),
            "end_time": pd.to_datetime(
                ["2023-01-01 01:00:00"]
            ),
            "messages": [10],
            "mean_latitude": [62.8],
            "mean_longitude": [6.8],
            "mean_speed": [0.1],
            "max_speed": [0.2],
            "duration_minutes": [60.0],
        }
    )

    ports = [
        {
            "name": "Test Port",
            "latitude": 62.5025,
            "longitude": 6.0655,
            "radius_nm": 0.5,
        }
    ]

    result = detect_port_calls(
        stationary_periods,
        ports,
    )

    assert result.empty