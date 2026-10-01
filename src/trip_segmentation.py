def assign_trip_ids(track, gap_minutes=30):
    """
    Assign trip IDs based on time gaps between AIS observations.
    """

    track = track.copy()
    track = track.sort_values("date_time_utc").reset_index(drop=True)

    time_gap = (
        track["date_time_utc"]
        .diff()
        .dt.total_seconds()
        / 60
    )

    new_trip = time_gap > gap_minutes

    track["trip_id"] = new_trip.cumsum() + 1
    track["time_gap_minutes"] = time_gap

    return track


def summarize_trips(track_with_trips):
    """
    Create one summary row per trip.
    """

    summary = (
        track_with_trips
        .groupby("trip_id")
        .agg(
            messages=("trip_id", "size"),
            start_time=("date_time_utc", "min"),
            end_time=("date_time_utc", "max"),
            min_latitude=("latitude", "min"),
            max_latitude=("latitude", "max"),
            min_longitude=("longitude", "min"),
            max_longitude=("longitude", "max"),
        )
        .reset_index()
    )

    summary["duration_hours"] = (
        summary["end_time"] - summary["start_time"]
    ).dt.total_seconds() / 3600

    return summary