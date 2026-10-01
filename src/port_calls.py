from src.trajectory import haversine_distance_nm


def detect_port_calls(
    stationary_periods,
    ports,
):
    """
    Match stationary periods to nearby ports.

    Parameters
    ----------
    stationary_periods : pandas.DataFrame
        Output from detect_stationary_periods().
        Must contain mean_latitude and mean_longitude.

    ports : list of dict
        Each dictionary must contain:
        - name
        - latitude
        - longitude
        - radius_nm

    Returns
    -------
    pandas.DataFrame
        Stationary periods that fall within a port radius.
    """

    port_calls = []

    for _, period in stationary_periods.iterrows():

        for port in ports:

            distance = haversine_distance_nm(
                period["mean_latitude"],
                period["mean_longitude"],
                port["latitude"],
                port["longitude"],
            )

            if distance <= port["radius_nm"]:

                call = period.to_dict()

                call["port_name"] = port["name"]
                call["distance_to_port_nm"] = distance

                port_calls.append(call)

                break

    import pandas as pd

    return pd.DataFrame(port_calls)