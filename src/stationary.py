def detect_stationary_periods(
    track,
    speed_threshold=0.5,
    min_duration_minutes=10,
    max_gap_minutes=30,
):
    """
    Detect stationary periods based on low speed over time.

    A new stationary period starts when:
    - the vessel changes between moving and stationary, or
    - the time gap between observations exceeds max_gap_minutes.
    """

    track = track.copy()
    track = track.sort_values("date_time_utc").reset_index(drop=True)

    track["time_gap_minutes"] = (
        track["date_time_utc"]
        .diff()
        .dt.total_seconds()
        / 60
    )

    track["is_stationary"] = (
        track["speed_over_ground"] <= speed_threshold
    )

    state_change = (
        track["is_stationary"]
        != track["is_stationary"].shift()
    )

    large_gap = (
        track["time_gap_minutes"] > max_gap_minutes
    )

    track["stationary_group"] = (
        state_change | large_gap
    ).cumsum()

    stationary = track[
        track["is_stationary"]
    ].copy()

    summary = (
        stationary
        .groupby("stationary_group")
        .agg(
            start_time=("date_time_utc", "min"),
            end_time=("date_time_utc", "max"),
            messages=("date_time_utc", "size"),
            mean_latitude=("latitude", "mean"),
            mean_longitude=("longitude", "mean"),
            mean_speed=("speed_over_ground", "mean"),
            max_speed=("speed_over_ground", "max"),
        )
        .reset_index(drop=True)
    )

    summary["duration_minutes"] = (
        summary["end_time"]
        - summary["start_time"]
    ).dt.total_seconds() / 60

    summary = summary[
        summary["duration_minutes"]
        >= min_duration_minutes
    ]

    return summary.reset_index(drop=True)
