import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.roster import generate_se_roster, ROSTER_SIZE, POD_NAMES


def test_roster_size_and_roles():
    rng = random.Random(42)
    roster = generate_se_roster(rng)
    assert len(roster) == ROSTER_SIZE
    roles = [r["role"] for r in roster]
    assert roles.count("Director") == 1
    assert roles.count("SE Manager") == 2
    assert roles.count("SE") == ROSTER_SIZE - 3


def test_roster_pods_and_manager_links():
    rng = random.Random(42)
    roster = generate_se_roster(rng)
    by_id = {r["se_id"]: r for r in roster}
    director = [r for r in roster if r["role"] == "Director"][0]
    assert director["manager_id"] is None
    for r in roster:
        assert r["pod"] in POD_NAMES
        if r["role"] != "Director":
            assert r["manager_id"] in by_id


def test_roster_is_deterministic():
    roster_a = generate_se_roster(random.Random(42))
    roster_b = generate_se_roster(random.Random(42))
    assert roster_a == roster_b
