import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.visualize_clusters import plot_stationary_clusters


def test_plot_stationary_clusters_without_basemap(
    monkeypatch,
):
    clustered_stationary = pd.DataFrame(
        {
            "mean_latitude": [
                62.5000,
                62.5005,
                62.5100,
                62.5200,
            ],
            "mean_longitude": [
                6.0000,
                6.0005,
                6.0200,
                6.0400,
            ],
            "nearest_port": [
                "Port A",
                "Port A",
                "Port B",
                "Port B",
            ],
            "cluster_id": [
                0,
                0,
                1,
                -1,
            ],
        }
    )

    ports = [
        {
            "name": "Port A",
            "latitude": 62.5000,
            "longitude": 6.0000,
            "radius_nm": 0.5,
        },
        {
            "name": "Port B",
            "latitude": 62.5100,
            "longitude": 6.0200,
            "radius_nm": 0.5,
        },
        {
            "name": "Unused Port",
            "latitude": 62.6000,
            "longitude": 6.2000,
            "radius_nm": 0.5,
        },
    ]

    monkeypatch.setattr(
        plt,
        "show",
        lambda: None,
    )

    fig, ax = plot_stationary_clusters(
        clustered_stationary,
        ports,
        basemap=False,
    )

    assert fig is not None
    assert ax is not None

    plt.close("all")


def test_plot_stationary_clusters_empty_data():
    clustered_stationary = pd.DataFrame()

    fig, ax = plot_stationary_clusters(
        clustered_stationary,
        [],
        basemap=False,
    )

    assert fig is None
    assert ax is None