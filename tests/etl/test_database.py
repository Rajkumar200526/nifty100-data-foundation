from pathlib import Path


def test_database_exists():
    assert Path("db/nifty100.db").exists()