#!/usr/bin/env python3
"""Generates Fluxora's synthetic CRM dataset ("soma-moma") as 8 CSV files.

Usage:
    python3 generate_crm_data.py [--output-dir DIR] [--seed N]
"""

import argparse
import random
from pathlib import Path

from crm_data.roster import generate_se_roster
from crm_data.accounts import generate_accounts
from crm_data.contacts import generate_contacts
from crm_data.opportunities import generate_opportunities
from crm_data.opportunity_team_members import generate_opportunity_team_members
from crm_data.pocs import generate_pocs
from crm_data.se_activities import generate_se_activities
from crm_data.competitor_mentions import generate_competitor_mentions
from crm_data.rfp_responses import generate_rfp_responses
from crm_data.csv_writer import write_csv

DEFAULT_SEED = 42

ROW_COUNTS = {
    "accounts": 200,
    "contacts": 600,
    "opportunities": 350,
    "opportunity_team_members": 400,
    "pocs": 120,
    "se_activities": 900,
    "competitor_mentions": 150,
    "rfp_responses": 70,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent.parent / "output"),
        help="Directory to write CSV files into (default: ../output relative to this script)",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)

    roster = generate_se_roster(rng)
    accounts = generate_accounts(rng, count=ROW_COUNTS["accounts"])
    contacts = generate_contacts(rng, accounts, count=ROW_COUNTS["contacts"])
    opportunities = generate_opportunities(rng, accounts, count=ROW_COUNTS["opportunities"])
    team_members = generate_opportunity_team_members(
        rng, opportunities, roster, count=ROW_COUNTS["opportunity_team_members"]
    )
    pocs = generate_pocs(rng, opportunities, count=ROW_COUNTS["pocs"])
    activities = generate_se_activities(
        rng, opportunities, roster, count=ROW_COUNTS["se_activities"]
    )
    mentions = generate_competitor_mentions(
        rng, opportunities, count=ROW_COUNTS["competitor_mentions"]
    )
    rfp_responses = generate_rfp_responses(
        rng, opportunities, count=ROW_COUNTS["rfp_responses"]
    )

    files = [
        ("accounts.csv", accounts),
        ("contacts.csv", contacts),
        ("opportunities.csv", opportunities),
        ("opportunity_team_members.csv", team_members),
        ("pocs.csv", pocs),
        ("se_activities.csv", activities),
        ("competitor_mentions.csv", mentions),
        ("rfp_responses.csv", rfp_responses),
    ]

    for filename, rows in files:
        write_csv(rows, str(output_dir / filename))
        print(f"{filename}: {len(rows)} rows")


if __name__ == "__main__":
    main()
