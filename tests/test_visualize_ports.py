import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.visualize_ports import plot_ports_and_track


def test_plot_ports_and_track_without_stationary_periods(
    monkeypatch,
):
    track = pd.DataFrame(
        {
            "longitude": [
                6.05,
                6.06,
                6.07,
            ],
            "latitude": [
                62.50,
                62.51,
                62.52,
            ],
        }
    )

    ports = [
        {
            "name": "Port A",
            "latitude": 62.50,
            "longitude": 6.08,
            "radius_nm": 0.5,
        }
    ]

    monkeypatch.setattr(
        plt,
        "show",
        lambda: None,
    )

    plot_ports_and_track(
        track,
        ports,
        vessel_id="vessel_test",
        stationary_periods=None,
        zoom_to_track=True,
        basemap=False,
    )

    assert len(plt.get_fignums()) > 0

    plt.close("all")


def test_plot_ports_and_track_with_stationary_period(
    monkeypatch,
):
    track = pd.DataFrame(
        {
            "longitude": [
                6.05,
                6.051,
                6.052,
            ],
            "latitude": [
                62.50,
                62.501,
                62.502,
            ],
        }
    )

    ports = [
        {
            "name": "Port A",
            "latitude": 62.503,
            "longitude": 6.053,
            "radius_nm": 0.5,
        },
        {
            "name": "Port B",
            "latitude": 62.60,
            "longitude": 6.20,
            "radius_nm": 0.5,
        },
    ]

    stationary_periods = pd.DataFrame(
        {
            "mean_latitude": [
                62.502,
            ],
            "mean_longitude": [
                6.052,
            ],
        }
    )

    monkeypatch.setattr(
        plt,
        "show",
        lambda: None,
    )

    plot_ports_and_track(
        track,
        ports,
        vessel_id="vessel_test",
        stationary_periods=stationary_periods,
        zoom_to_track=True,
        basemap=False,
    )

    assert len(plt.get_fignums()) > 0

    plt.close("all")