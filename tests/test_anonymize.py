import pandas as pd

from src.anonymize import anonymize_ais_data


def test_anonymize_removes_private_identifiers():
    df = pd.DataFrame(
        {
            "mmsi": [111111111, 222222222],
            "imo": [1234567, 7654321],
            "callsign": ["AAA", "BBB"],
            "ship_name": ["Ship A", "Ship B"],
            "latitude": [62.1, 62.2],
            "longitude": [6.1, 6.2],
        }
    )

    result = anonymize_ais_data(df)

    assert "mmsi" not in result.columns
    assert "imo" not in result.columns
    assert "callsign" not in result.columns
    assert "ship_name" not in result.columns
    assert "vessel_id" in result.columns

    assert result["vessel_id"].nunique() == 2