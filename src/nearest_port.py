from src.trajectory import haversine_distance_nm


def find_nearest_port(latitude, longitude, ports):
    """
    Find the nearest configured port to a position.
    """
    if not ports:
        return None

    nearest = None
    nearest_distance = float("inf")

    for port in ports:
        distance = haversine_distance_nm(
            latitude,
            longitude,
            port["latitude"],
            port["longitude"],
        )

        if distance < nearest_distance:
            nearest_distance = distance
            nearest = {
                "port_name": port["name"],
                "distance_nm": distance,
                "radius_nm": port["radius_nm"],
                "inside_port_radius": distance <= port["radius_nm"],
            }

    return nearest