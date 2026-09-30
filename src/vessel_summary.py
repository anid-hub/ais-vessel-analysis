import pandas as pd

from src.trajectory import (
    get_vessel_track,
    add_distance_travelled,
)


def summarize_all_vessels(df):
    """
    Build a summary table for all anonymized vessels.
    """

    rows = []

    for vessel_id in df["vessel_id"].dropna().unique():

        track = get_vessel_track(df, vessel_id)

        distance_track = add_distance_travelled(track)

        start_time = track["date_time_utc"].min()
        end_time = track["date_time_utc"].max()

        duration_hours = (
            end_time - start_time
        ).total_seconds() / 3600

        total_distance_nm = (
            distance_track["distance_nm"].sum()
        )

        distance_avg_speed = (
            total_distance_nm / duration_hours
            if duration_hours > 0
            else 0
        )

        row = {
            "vessel_id": vessel_id,
            "messages": len(track),
            "start_time": start_time,
            "end_time": end_time,
            "duration_hours": duration_hours,
            "mean_reported_sog": (
                track["speed_over_ground"].mean()
            ),
            "max_speed": (
                track["speed_over_ground"].max()
            ),
            "total_distance_nm": total_distance_nm,
            "distance_avg_speed": distance_avg_speed,
            "min_latitude": track["latitude"].min(),
            "max_latitude": track["latitude"].max(),
            "min_longitude": track["longitude"].min(),
            "max_longitude": track["longitude"].max(),
        }

        rows.append(row)

    summary = pd.DataFrame(rows)

    return (
        summary
        .sort_values(
            "total_distance_nm",
            ascending=False
        )
        .reset_index(drop=True)
    )