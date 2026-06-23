from pathlib import Path


def test_db_exists():
    assert Path("db/nifty100.db").exists()