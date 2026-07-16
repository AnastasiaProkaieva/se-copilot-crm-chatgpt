import csv
import random
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from crm_data.csv_writer import write_csv


def test_write_csv_roundtrip(tmp_path):
    rows = [
        {"id": "A-01", "name": "Alpha"},
        {"id": "A-02", "name": "Beta"},
    ]
    out_path = tmp_path / "test.csv"
    write_csv(rows, str(out_path))

    with open(out_path, newline="") as f:
        reader = csv.DictReader(f)
        read_rows = list(reader)

    assert read_rows == rows


def test_full_script_run_produces_all_csvs_with_expected_row_counts(tmp_path):
    output_dir = tmp_path / "output"
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "generate_crm_data.py"), "--output-dir", str(output_dir)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    expected_counts = {
        "accounts.csv": 200,
        "contacts.csv": 600,
        "opportunities.csv": 350,
        "opportunity_team_members.csv": 400,
        "pocs.csv": 120,
        "se_activities.csv": 900,
        "competitor_mentions.csv": 150,
        "rfp_responses.csv": 70,
    }
    for filename, expected_count in expected_counts.items():
        path = output_dir / filename
        assert path.exists(), f"{filename} was not created"
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == expected_count, f"{filename} had {len(rows)} rows, expected {expected_count}"


def test_full_script_run_is_deterministic(tmp_path):
    output_dir_a = tmp_path / "run_a"
    output_dir_b = tmp_path / "run_b"
    for output_dir in (output_dir_a, output_dir_b):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_crm_data.py"), "--output-dir", str(output_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    for filename in ("accounts.csv", "opportunities.csv", "se_activities.csv"):
        content_a = (output_dir_a / filename).read_text()
        content_b = (output_dir_b / filename).read_text()
        assert content_a == content_b


def test_foreign_keys_are_referentially_consistent_across_all_files(tmp_path):
    output_dir = tmp_path / "output"
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "generate_crm_data.py"), "--output-dir", str(output_dir)],
        capture_output=True,
        text=True,
        check=True,
    )

    def read_ids(filename, id_field):
        with open(output_dir / filename, newline="") as f:
            return {row[id_field] for row in csv.DictReader(f)}

    account_ids = read_ids("accounts.csv", "account_id")
    opportunity_ids = read_ids("opportunities.csv", "opportunity_id")

    with open(output_dir / "contacts.csv", newline="") as f:
        for row in csv.DictReader(f):
            assert row["account_id"] in account_ids

    with open(output_dir / "opportunities.csv", newline="") as f:
        for row in csv.DictReader(f):
            assert row["account_id"] in account_ids

    with open(output_dir / "pocs.csv", newline="") as f:
        for row in csv.DictReader(f):
            assert row["opportunity_id"] in opportunity_ids

    with open(output_dir / "competitor_mentions.csv", newline="") as f:
        for row in csv.DictReader(f):
            assert row["opportunity_id"] in opportunity_ids

    with open(output_dir / "rfp_responses.csv", newline="") as f:
        for row in csv.DictReader(f):
            assert row["opportunity_id"] == "" or row["opportunity_id"] in opportunity_ids
