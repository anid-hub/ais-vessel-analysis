import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx

from shapely.geometry import Point
from src.nearest_port import find_nearest_port


def plot_ports_and_track(
    track,
    ports,
    vessel_id=None,
    stationary_periods=None,
    zoom_to_track=False,
    basemap=True,
):
    """
    Plot AIS vessel track and configured ports
    on an optional basemap.
    """

    # -----------------------
    # Convert AIS track
    # -----------------------

    track_gdf = gpd.GeoDataFrame(
        track.copy(),
        geometry=[
            Point(lon, lat)
            for lon, lat in zip(
                track["longitude"],
                track["latitude"],
            )
        ],
        crs="EPSG:4326",
    )

    # -----------------------
    # Convert ports
    # -----------------------

    ports_gdf = gpd.GeoDataFrame(
        ports,
        geometry=[
            Point(
                port["longitude"],
                port["latitude"],
            )
            for port in ports
        ],
        crs="EPSG:4326",
    )

    # -----------------------
    # Convert to Web Mercator
    # -----------------------

    track_gdf = track_gdf.to_crs(
        epsg=3857
    )

    ports_gdf = ports_gdf.to_crs(
        epsg=3857
    )

    # -----------------------
    # Create plot
    # -----------------------

    fig, ax = plt.subplots(
        figsize=(11, 9)
    )

    # AIS track
    ax.plot(
        track_gdf.geometry.x,
        track_gdf.geometry.y,
        linewidth=1.5,
        label="AIS track",
    )

    # Configured ports
    ax.scatter(
        ports_gdf.geometry.x,
        ports_gdf.geometry.y,
        marker="x",
        s=55,
        label="Configured ports",
    )

    # Initialize nearest-port variables
    nearest = None
    nearest_x = None
    nearest_y = None

    # -----------------------
    # Stationary position
    # -----------------------

    if (
        stationary_periods is not None
        and not stationary_periods.empty
    ):

        stationary = stationary_periods.iloc[0]

        stationary_gdf = gpd.GeoDataFrame(
            geometry=[
                Point(
                    stationary["mean_longitude"],
                    stationary["mean_latitude"],
                )
            ],
            crs="EPSG:4326",
        ).to_crs(
            epsg=3857
        )

        stationary_x = (
            stationary_gdf.geometry.x.iloc[0]
        )

        stationary_y = (
            stationary_gdf.geometry.y.iloc[0]
        )

        ax.scatter(
            stationary_x,
            stationary_y,
            marker="o",
            s=90,
            label="Stationary position",
        )

        # -----------------------
        # Nearest port
        # -----------------------

        nearest = find_nearest_port(
            stationary["mean_latitude"],
            stationary["mean_longitude"],
            ports,
        )

        if nearest is not None:

            nearest_match = ports_gdf[
                ports_gdf["name"]
                == nearest["port_name"]
            ]

            if not nearest_match.empty:

                nearest_row = (
                    nearest_match.iloc[0]
                )

                nearest_x = (
                    nearest_row.geometry.x
                )

                nearest_y = (
                    nearest_row.geometry.y
                )

                ax.scatter(
                    nearest_x,
                    nearest_y,
                    marker="s",
                    s=100,
                    label="Nearest port",
                )

                ax.plot(
                    [
                        stationary_x,
                        nearest_x,
                    ],
                    [
                        stationary_y,
                        nearest_y,
                    ],
                    linestyle="--",
                    linewidth=1,
                )

                ax.annotate(
                    (
                        f'{nearest["port_name"]}\n'
                        f'{nearest["distance_nm"]:.2f} NM'
                    ),
                    (
                        nearest_x,
                        nearest_y,
                    ),
                    xytext=(8, 8),
                    textcoords="offset points",
                    fontsize=9,
                )

    # -----------------------
    # Zoom
    # -----------------------

    if zoom_to_track:

        x_values = list(
            track_gdf.geometry.x
        )

        y_values = list(
            track_gdf.geometry.y
        )

        if (
            nearest is not None
            and nearest_x is not None
            and nearest_y is not None
        ):
            x_values.append(
                nearest_x
            )

            y_values.append(
                nearest_y
            )

        xmin = min(x_values)
        xmax = max(x_values)

        ymin = min(y_values)
        ymax = max(y_values)

        x_range = xmax - xmin
        y_range = ymax - ymin

        x_margin = max(
            x_range * 0.15,
            1000,
        )

        y_margin = max(
            y_range * 0.15,
            1000,
        )

        ax.set_xlim(
            xmin - x_margin,
            xmax + x_margin,
        )

        ax.set_ylim(
            ymin - y_margin,
            ymax + y_margin,
        )

    # -----------------------
    # Basemap
    # -----------------------

    if basemap:

        ctx.add_basemap(
            ax,
            source=ctx.providers.Esri.WorldTopoMap,
        )

    # -----------------------
    # Formatting
    # -----------------------

    title = (
        "AIS track and configured port locations"
    )

    if vessel_id is not None:
        title += f" — {vessel_id}"

    ax.set_title(title)

    ax.set_xlabel(
        "Web Mercator X"
    )

    ax.set_ylabel(
        "Web Mercator Y"
    )

    ax.legend()

    plt.tight_layout()
    plt.show()