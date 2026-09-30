import matplotlib.pyplot as plt


def plot_vessel_track(track, vessel_id=None):
    """
    Plot the trajectory of one vessel.

    Parameters
    ----------
    track : pandas.DataFrame
        Vessel trajectory containing longitude and latitude.

    vessel_id : str, optional
        Anonymous vessel identifier used in the plot title.
    """

    if track.empty:
        raise ValueError("The vessel track is empty.")

    plt.figure(figsize=(10, 8))

    plt.plot(
        track["longitude"],
        track["latitude"],
        linewidth=1,
    )

    plt.scatter(
        track["longitude"].iloc[0],
        track["latitude"].iloc[0],
        label="Start",
    )

    plt.scatter(
        track["longitude"].iloc[-1],
        track["latitude"].iloc[-1],
        label="End",
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    if vessel_id is None:
        plt.title("Vessel trajectory")
    else:
        plt.title(f"Trajectory - {vessel_id}")

    plt.legend()
    plt.grid()

    plt.show()