import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


@pytest.fixture(scope="session")
def processed_dir():
    return ROOT / "data" / "processed"


@pytest.fixture(scope="session")
def nodes(processed_dir):
    return pd.read_csv(processed_dir / "nodes.csv", encoding="utf-8-sig")


@pytest.fixture(scope="session")
def relations_event_level(processed_dir):
    return pd.read_csv(processed_dir / "relations_event_level.csv", encoding="utf-8-sig")


@pytest.fixture(scope="session")
def relations_aggregated(processed_dir):
    return pd.read_csv(processed_dir / "relations_aggregated.csv", encoding="utf-8-sig")


@pytest.fixture(scope="session")
def stories(processed_dir):
    return pd.read_csv(processed_dir / "stories.csv", encoding="utf-8-sig")
