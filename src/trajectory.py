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