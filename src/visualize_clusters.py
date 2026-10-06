import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point


def plot_stationary_clusters(
    clustered_stationary,
    ports,
    basemap=True,
):
    """
    Plot DBSCAN stationary-location clusters near ports.

    cluster_id == -1 represents DBSCAN noise.
    Only ports referenced by the selected stationary points
    are shown.
    """

    if clustered_stationary.empty:
        print("No clustered stationary points to plot.")
        return None, None

    # =====================================================
    # Stationary points
    # =====================================================

    points_gdf = gpd.GeoDataFrame(
        clustered_stationary.copy(),
        geometry=[
            Point(lon, lat)
            for lon, lat in zip(
                clustered_stationary["mean_longitude"],
                clustered_stationary["mean_latitude"],
            )
        ],
        crs="EPSG:4326",
    ).to_crs("EPSG:3857")

    # =====================================================
    # Keep only ports referenced by stationary points
    # =====================================================

    used_port_names = set(
        clustered_stationary["nearest_port"]
        .dropna()
        .unique()
    )

    used_ports = [
        port
        for port in ports
        if port["name"] in used_port_names
    ]

    ports_gdf = gpd.GeoDataFrame(
        used_ports,
        geometry=[
            Point(
                port["longitude"],
                port["latitude"],
            )
            for port in used_ports
        ],
        crs="EPSG:4326",
    ).to_crs("EPSG:3857")

    # =====================================================
    # Plot
    # =====================================================

    fig, ax = plt.subplots(
        figsize=(12, 10),
    )

    cluster_ids = sorted(
        points_gdf["cluster_id"].unique()
    )

    for cluster_id in cluster_ids:

        cluster = points_gdf[
            points_gdf["cluster_id"] == cluster_id
        ]

        if cluster_id == -1:
            cluster.plot(
                ax=ax,
                marker="x",
                markersize=55,
                label="Noise",
            )

        else:
            cluster.plot(
                ax=ax,
                marker="o",
                markersize=55,
                alpha=0.8,
                label=f"Cluster {cluster_id}",
            )

    # =====================================================
    # Configured ports
    # =====================================================

    if not ports_gdf.empty:

        ports_gdf.plot(
            ax=ax,
            marker="^",
            markersize=75,
            label="Associated ports",
        )

        #for _, port in ports_gdf.iterrows():

           # ax.annotate(
           #     port["name"],
            #    (
             #       port.geometry.x,
             #       port.geometry.y,
              #  ),
              #  xytext=(4, 4),
               # textcoords="offset points",
               # fontsize=7,
           # )

    # =====================================================
    # Cluster centroids
    # =====================================================

    valid_clusters = points_gdf[
        points_gdf["cluster_id"] != -1
    ]

    for cluster_id, cluster in valid_clusters.groupby(
        "cluster_id"
    ):

        centroid_x = cluster.geometry.x.mean()
        centroid_y = cluster.geometry.y.mean()

        n_points = len(cluster)

        ax.scatter(
            centroid_x,
            centroid_y,
            marker="*",
            s=180,
            edgecolor="black",
            linewidth=0.8,
            zorder=6,
        )

        ax.annotate(
            f"Cluster {cluster_id}\n(n={n_points})",
            (
                centroid_x,
                centroid_y,
            ),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=8,
            fontweight="bold",
        )

    # =====================================================
    # Basemap
    # =====================================================

    if basemap:
        ctx.add_basemap(
            ax,
            source=ctx.providers.Esri.WorldTopoMap,
        )

    # =====================================================
    # Labels
    # =====================================================

    ax.set_title(
        "DBSCAN clusters of stationary AIS positions near ports"
    )

    ax.set_xlabel("Web Mercator X")
    ax.set_ylabel("Web Mercator Y")

    ax.legend(
        title="Stationary clusters",
        loc="best",
    )

    plt.tight_layout()
    plt.show()

    return fig, ax