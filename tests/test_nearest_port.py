from src.nearest_port import find_nearest_port


def test_find_nearest_port():
    ports = [
        {
            "name": "Port A",
            "latitude": 62.50,
            "longitude": 6.00,
            "radius_nm": 0.5,
        },
        {
            "name": "Port B",
            "latitude": 62.60,
            "longitude": 6.20,
            "radius_nm": 0.5,
        },
    ]

    result = find_nearest_port(
        62.501,
        6.001,
        ports,
    )

    assert result["port_name"] == "Port A"
    assert result["distance_nm"] >= 0
    assert result["inside_port_radius"] is True


def test_find_nearest_port_empty_list():
    result = find_nearest_port(
        62.5,
        6.0,
        [],
    )

    assert result is None