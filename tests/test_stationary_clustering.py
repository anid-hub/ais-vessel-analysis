import pandas as pd

from src.stationary_clustering import (
    filter_stationary_near_ports,
    cluster_stationary_points,
)


def test_filter_stationary_near_ports():
    stationary_periods = pd.DataFrame(
        {
            "mean_latitude": [
                62.5000,
                62.7000,
            ],
            "mean_longitude": [
                6.0000,
                6.5000,
            ],
        }
    )

    ports = [
        {
            "name": "Port A",
            "latitude": 62.5005,
            "longitude": 6.0005,
            "radius_nm": 0.5,
        }
    ]

    result = filter_stationary_near_ports(
        stationary_periods,
        ports,
        near_port_nm=2.0,
    )

    assert len(result) == 1
    assert result.iloc[0]["nearest_port"] == "Port A"
    assert result.iloc[0]["distance_to_port_nm"] <= 2.0


def test_cluster_stationary_points():
    stationary_periods = pd.DataFrame(
        {
            "mean_latitude": [
                62.5000,
                62.5005,
                62.5010,
                62.6000,
            ],
            "mean_longitude": [
                6.0000,
                6.0005,
                6.0010,
                6.2000,
            ],
        }
    )

    result = cluster_stationary_points(
        stationary_periods,
        eps_nm=0.5,
        min_samples=3,
    )

    assert "cluster_id" in result.columns

    clustered = result.iloc[:3]["cluster_id"]

    assert clustered.nunique() == 1
    assert clustered.iloc[0] != -1

    assert result.iloc[3]["cluster_id"] == -1