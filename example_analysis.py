import argparse
import pandas as pd

from src.anonymize import anonymize_ais_data
from src.clean_data import clean_ais_data
from src.trajectory import (
    get_vessel_track,
    summarize_track,
    add_time_gaps,
    add_distance_travelled,
)
from src.vessel_summary import summarize_all_vessels
from src.visualize import plot_vessel_track


def main():
    parser = argparse.ArgumentParser(
        description="Run an example AIS vessel analysis."
    )

    parser.add_argument(
        "file_path",
        help="Path to the AIS Parquet file."
    )

    parser.add_argument(
        "--vessel",
        default="vessel_059",
        help="Anonymized vessel ID to analyze."
    )

    args = parser.parse_args()

    # Load data
    df = pd.read_parquet(args.file_path)

    # Anonymize and clean
    df_anon = anonymize_ais_data(df)
    df_clean = clean_ais_data(df_anon)

    # Select vessel
    track = get_vessel_track(
        df_clean,
        args.vessel
    )

    if track.empty:
        raise ValueError(
            f"No data found for {args.vessel}"
        )

    # Summary
    summary = summarize_track(track)

    print(f"\nSummary for {args.vessel}")

    for key, value in summary.items():
        print(f"{key}: {value}")

    # Time gaps
    track_with_gaps = add_time_gaps(
        track,
        gap_minutes=10
    )

    print("\nLargest time gaps:")

    print(
        track_with_gaps[
            [
                "date_time_utc",
                "time_gap",
                "large_gap",
            ]
        ]
        .sort_values(
            "time_gap",
            ascending=False
        )
        .head(10)
    )

    # Distance
    distance_track = add_distance_travelled(track)

    total_distance = (
        distance_track["distance_nm"].sum()
    )

    print(
        "\nTotal distance travelled:",
        round(total_distance, 2),
        "nautical miles"
    )

    # Fleet summary
    fleet_summary = summarize_all_vessels(
        df_clean
    )

    print("\nTop vessels by distance:")

    print(
        fleet_summary[
            [
                "vessel_id",
                "messages",
                "mean_reported_sog",
                "total_distance_nm",
                "distance_avg_speed",
            ]
        ].head(10)
    )

    # Plot selected vessel
    plot_vessel_track(
        track,
        vessel_id=args.vessel
    )


if __name__ == "__main__":
    main()