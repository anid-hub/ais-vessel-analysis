import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from src.trajectory import haversine_distance_nm


def filter_stationary_near_ports(
    stationary_periods,
    ports,
    near_port_nm=2.0,
):
    """
    Keep stationary-period mean positions that are within
    near_port_nm of at least one configured port.
    """

    rows = []

    for _, period in stationary_periods.iterrows():
        latitude = period["mean_latitude"]
        longitude = period["mean_longitude"]

        nearest_port = None
        nearest_distance = None

        for port in ports:
            distance_nm = haversine_distance_nm(
                latitude,
                longitude,
                port["latitude"],
                port["longitude"],
            )

            if (
                nearest_distance is None
                or distance_nm < nearest_distance
            ):
                nearest_distance = distance_nm
                nearest_port = port["name"]

        if (
            nearest_distance is not None
            and nearest_distance <= near_port_nm
        ):
            row = period.to_dict()
            row["nearest_port"] = nearest_port
            row["distance_to_port_nm"] = nearest_distance
            rows.append(row)

    return pd.DataFrame(rows)


def cluster_stationary_points(
    stationary_periods,
    eps_nm=0.5,
    min_samples=3,
):
    """
    Cluster stationary-period mean positions using DBSCAN
    with haversine distance.

    Cluster label -1 means DBSCAN classified the point
    as noise.
    """

    result = stationary_periods.copy()

    if result.empty:
        result["cluster_id"] = pd.Series(dtype=int)
        return result

    coords = result[
        ["mean_latitude", "mean_longitude"]
    ].to_numpy()

    coords_rad = np.radians(coords)

    earth_radius_nm = 3440.065
    eps_rad = eps_nm / earth_radius_nm

    model = DBSCAN(
        eps=eps_rad,
        min_samples=min_samples,
        metric="haversine",
        algorithm="ball_tree",
    )

    result["cluster_id"] = model.fit_predict(coords_rad)

    return result