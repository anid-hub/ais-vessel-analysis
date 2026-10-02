import pandas as pd
import pytest

from src.ports import load_ports


def test_load_ports_reads_valid_csv(tmp_path):
    file_path = tmp_path / "ports.csv"

    pd.DataFrame(
        {
            "name": ["Port A"],
            "latitude": [62.5],
            "longitude": [6.0],
            "radius_nm": [0.5],
        }
    ).to_csv(file_path, index=False)

    ports = load_ports(file_path)

    assert len(ports) == 1
    assert ports[0]["name"] == "Port A"
    assert ports[0]["latitude"] == 62.5
    assert ports[0]["longitude"] == 6.0
    assert ports[0]["radius_nm"] == 0.5


def test_load_ports_rejects_missing_columns(tmp_path):
    file_path = tmp_path / "ports.csv"

    pd.DataFrame(
        {
            "name": ["Port A"],
            "latitude": [62.5],
        }
    ).to_csv(file_path, index=False)

    with pytest.raises(ValueError):
        load_ports(file_path)