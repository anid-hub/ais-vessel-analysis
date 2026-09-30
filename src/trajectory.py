def get_vessel_track(df, vessel_id):
    """
    Extract and sort the trajectory for one anonymized vessel.

    Parameters
    ----------
    df : pandas.DataFrame
        AIS dataset containing vessel_id and date_time_utc.

    vessel_id : str
        Anonymous vessel identifier.

    Returns
    -------
    pandas.DataFrame
        Chronologically sorted AIS records for the selected vessel.
    """

    vessel = df[df["vessel_id"] == vessel_id].copy()

    vessel = vessel.sort_values("date_time_utc")

    return vessel.reset_index(drop=True)
def summarize_track(track):
  
    """
    Return basic statistics for a vessel trajectory.
    """

    return {
        "messages": len(track),
        "start_time": track["date_time_utc"].min(),
        "end_time": track["date_time_utc"].max(),
        "avg_speed": track["speed_over_ground"].mean(),
        "max_speed": track["speed_over_ground"].max(),
        "min_latitude": track["latitude"].min(),
        "max_latitude": track["latitude"].max(),
        "min_longitude": track["longitude"].min(),
        "max_longitude": track["longitude"].max(),
    }
def add_time_gaps(track, gap_minutes=10):
    """
    Add the time difference between consecutive AIS messages
    and flag large gaps.
    """

    track = track.copy()

    track["time_gap"] = (
        track["date_time_utc"]
        .diff()
        .dt.total_seconds()
        / 60
    )

    track["large_gap"] = track["time_gap"] > gap_minutes

    return track
import math

def haversine_distance_nm(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographic points
    in nautical miles using the Haversine formula.
    """

    earth_radius_nm = 3440.065

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.asin(math.sqrt(a))

    return earth_radius_nm * c
def add_distance_travelled(track):
    """
    Calculate distance between consecutive AIS positions
    in nautical miles.
    """

    track = prepare_track_for_distance(track)

    distances = [0.0]

    for i in range(1, len(track)):
        distance = haversine_distance_nm(
            track.loc[i - 1, "latitude"],
            track.loc[i - 1, "longitude"],
            track.loc[i, "latitude"],
            track.loc[i, "longitude"],
        )

        distances.append(distance)

    track["distance_nm"] = distances

    return track
def prepare_track_for_distance(track):
    """
    Create one position per timestamp for distance calculations.

    Simultaneous observations from multiple data sources are
    represented by their mean latitude and longitude.
    """

    track = (
        track
        .groupby("date_time_utc", as_index=False)
        .agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
        )
        .sort_values("date_time_utc")
        .reset_index(drop=True)
    )

    return track