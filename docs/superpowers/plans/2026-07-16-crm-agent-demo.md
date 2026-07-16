# Fluxora SE Copilot Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python script that generates a realistic, referentially-consistent synthetic CRM dataset (8 CSVs) for the fictional "Fluxora" company, plus a guideline document explaining how to configure the corresponding ChatGPT Enterprise Agent/Skills/Connector.

**Architecture:** A single script, `scripts/generate_crm_data.py`, organized as one generator function per CRM object, run in dependency order (roster → Account → Contact → Opportunity → OpportunityTeamMember → POC__c → SE_Activity__c → Competitor_Mention__c → RFP_Response__c). Each generator returns a list of dicts and appends to a shared ID-registry so downstream generators can pick valid foreign keys. A final step writes each list to its own CSV under `output/`. A separate Markdown guideline doc is hand-written (no script) covering ChatGPT Enterprise setup.

**Tech Stack:** Python 3, `faker` (already installed locally, version 40.23.0), stdlib `csv` and `random`. No other dependencies.

## Global Constraints

- Fixed random seed (`42`) so re-running the script produces byte-identical output — spec section 8.
- Output: 8 CSV files in `output/`, one per object, using prefixed IDs (`ACC-0001`, `CON-0001`, `OPP-0001`, `OTM-0001`, `POC-0001`, `ACT-0001`, `CMP-0001`, `RFP-0001`) — spec section 5.
- Every foreign key column must reference a row that exists in its parent CSV — spec section 5 and 8.
- SE roster (42 SEs, 3 pods: Enterprise/Strategic/Mid-Market, 2 SE managers, 1 Director) generated first and reused consistently across Opportunity/OpportunityTeamMember/POC/SE_Activity — spec section 5.
- Fluxora vocabulary: product lines (Lakehouse Core, PipelineOps, ModelServe, Governance Suite), deal stages (Discovery → Technical Validation → POC → Business Case → Negotiation → Closed Won/Closed Lost), competitors (Databricks, Snowflake, Confluent) — spec section 4.
- Approximate row targets: accounts ~200, contacts ~600, opportunities ~350, opportunity_team_members ~400, pocs ~120, se_activities ~900, competitor_mentions ~150, rfp_responses ~70 — spec section 5.
- No live CRM/system integration — data + docs only — spec section 1 and 7.

---

## Task 1: Project scaffolding and shared roster generator

**Files:**
- Create: `scripts/generate_crm_data.py`
- Create: `scripts/crm_data/__init__.py`
- Create: `scripts/crm_data/roster.py`
- Test: `scripts/tests/test_roster.py`

**Interfaces:**
- Produces: `crm_data.roster.generate_se_roster(rng: random.Random) -> list[dict]`, where each dict has keys `se_id` (str, e.g. `"SE-001"`), `name` (str), `pod` (one of `"Enterprise"`, `"Strategic"`, `"Mid-Market"`), `role` (one of `"SE"`, `"SE Manager"`, `"Director"`), `manager_id` (str or `None` for the Director).
- Produces: `crm_data.roster.ROSTER_SIZE = 42`, `crm_data.roster.POD_NAMES = ["Enterprise", "Strategic", "Mid-Market"]`.

- [ ] **Step 1: Write the failing test for roster generation**

Create `scripts/tests/test_roster.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts/tests && python3 -m pytest test_roster.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'crm_data'`

- [ ] **Step 3: Write the roster generator**

Create `scripts/crm_data/__init__.py` (empty file).

Create `scripts/crm_data/roster.py`:

```python
"""Generates Fluxora's fixed 42-person Sales Engineering roster."""

import random

from faker import Faker

ROSTER_SIZE = 42
POD_NAMES = ["Enterprise", "Strategic", "Mid-Market"]


def generate_se_roster(rng: random.Random) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    roster = []

    director_id = "SE-001"
    roster.append(
        {
            "se_id": director_id,
            "name": fake.name(),
            "pod": rng.choice(POD_NAMES),
            "role": "Director",
            "manager_id": None,
        }
    )

    manager_ids = []
    for i in range(2, 4):
        se_id = f"SE-{i:03d}"
        manager_ids.append(se_id)
        roster.append(
            {
                "se_id": se_id,
                "name": fake.name(),
                "pod": POD_NAMES[(i - 2) % len(POD_NAMES)],
                "role": "SE Manager",
                "manager_id": director_id,
            }
        )

    for i in range(4, ROSTER_SIZE + 1):
        se_id = f"SE-{i:03d}"
        pod = rng.choice(POD_NAMES)
        pod_managers = [
            m
            for m in roster
            if m["role"] == "SE Manager" and m["pod"] == pod
        ]
        manager_id = (
            rng.choice(pod_managers)["se_id"]
            if pod_managers
            else rng.choice(manager_ids)
        )
        roster.append(
            {
                "se_id": se_id,
                "name": fake.name(),
                "pod": pod,
                "role": "SE",
                "manager_id": manager_id,
            }
        )

    return roster
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd scripts/tests && python3 -m pytest test_roster.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add scripts/crm_data/__init__.py scripts/crm_data/roster.py scripts/tests/test_roster.py
git commit -m "$(cat <<'EOF'
Add SE roster generator for CRM synthetic data
EOF
)"
```

---

## Task 2: Account and Contact generators

**Files:**
- Create: `scripts/crm_data/accounts.py`
- Create: `scripts/crm_data/contacts.py`
- Test: `scripts/tests/test_accounts.py`
- Test: `scripts/tests/test_contacts.py`

**Interfaces:**
- Consumes: nothing from Task 1 directly (Account has no FK to roster).
- Produces: `crm_data.accounts.generate_accounts(rng: random.Random, count: int = 200) -> list[dict]`, each dict has keys `account_id` (str, `"ACC-0001"`), `name` (str), `industry` (str), `employee_count` (int), `region` (str), `tech_stack_tags` (str, comma-separated).
- Produces: `crm_data.accounts.INDUSTRIES` (list[str]), `crm_data.accounts.REGIONS` (list[str]).
- Produces: `crm_data.contacts.generate_contacts(rng: random.Random, accounts: list[dict], count: int = 600) -> list[dict]`, each dict has keys `contact_id` (str, `"CON-0001"`), `account_id` (str, FK into `accounts`), `first_name`, `last_name`, `title` (str), `email` (str), `role` (one of `"Economic Buyer"`, `"Technical Evaluator"`, `"Champion"`).

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_accounts.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts


def test_account_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    assert len(accounts) == 200
    assert accounts[0]["account_id"] == "ACC-0001"
    assert accounts[-1]["account_id"] == "ACC-0200"


def test_account_ids_are_unique():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    ids = [a["account_id"] for a in accounts]
    assert len(ids) == len(set(ids))


def test_account_fields_present():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=5)
    for a in accounts:
        assert a["name"]
        assert a["industry"]
        assert isinstance(a["employee_count"], int) and a["employee_count"] > 0
        assert a["region"]
        assert isinstance(a["tech_stack_tags"], str)
```

Create `scripts/tests/test_contacts.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.contacts import generate_contacts


def test_contact_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    contacts = generate_contacts(rng, accounts, count=600)
    assert len(contacts) == 600
    assert contacts[0]["contact_id"] == "CON-0001"
    assert contacts[-1]["contact_id"] == "CON-0600"


def test_contact_account_ids_reference_existing_accounts():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    contacts = generate_contacts(rng, accounts, count=600)
    valid_ids = {a["account_id"] for a in accounts}
    for c in contacts:
        assert c["account_id"] in valid_ids


def test_contact_role_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    contacts = generate_contacts(rng, accounts, count=600)
    for c in contacts:
        assert c["role"] in {"Economic Buyer", "Technical Evaluator", "Champion"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts/tests && python3 -m pytest test_accounts.py test_contacts.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'crm_data.accounts'`

- [ ] **Step 3: Write the Account generator**

Create `scripts/crm_data/accounts.py`:

```python
"""Generates Fluxora's target Account records (companies being sold to)."""

import random

from faker import Faker

INDUSTRIES = [
    "Financial Services",
    "Healthcare",
    "Retail & E-commerce",
    "Media & Entertainment",
    "Manufacturing",
    "Logistics",
    "Insurance",
    "Telecommunications",
    "Gaming",
    "Ad Tech",
]

REGIONS = ["AMER", "EMEA", "APAC", "LATAM"]

TECH_STACK_TAGS = [
    "AWS",
    "GCP",
    "Azure",
    "Kubernetes",
    "Snowflake",
    "Kafka",
    "Spark",
    "Airflow",
    "dbt",
    "Postgres",
]


def generate_accounts(rng: random.Random, count: int = 200) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    accounts = []
    for i in range(1, count + 1):
        tags = rng.sample(TECH_STACK_TAGS, k=rng.randint(2, 4))
        accounts.append(
            {
                "account_id": f"ACC-{i:04d}",
                "name": fake.company(),
                "industry": rng.choice(INDUSTRIES),
                "employee_count": rng.randint(200, 20000),
                "region": rng.choice(REGIONS),
                "tech_stack_tags": ", ".join(tags),
            }
        )
    return accounts
```

- [ ] **Step 4: Write the Contact generator**

Create `scripts/crm_data/contacts.py`:

```python
"""Generates buyer-side Contact records linked to Accounts."""

import random

from faker import Faker

ROLES = ["Economic Buyer", "Technical Evaluator", "Champion"]

TITLES = [
    "VP of Engineering",
    "Head of Data Engineering",
    "Chief Data Officer",
    "Director of Platform Engineering",
    "Senior Data Engineer",
    "Staff Software Engineer",
    "Director of Infrastructure",
    "VP of Data Science",
]


def generate_contacts(
    rng: random.Random, accounts: list[dict], count: int = 600
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    account_ids = [a["account_id"] for a in accounts]

    contacts = []
    for i in range(1, count + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        contacts.append(
            {
                "contact_id": f"CON-{i:04d}",
                "account_id": rng.choice(account_ids),
                "first_name": first_name,
                "last_name": last_name,
                "title": rng.choice(TITLES),
                "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
                "role": rng.choice(ROLES),
            }
        )
    return contacts
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd scripts/tests && python3 -m pytest test_accounts.py test_contacts.py -v`
Expected: PASS (6 passed)

- [ ] **Step 6: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add scripts/crm_data/accounts.py scripts/crm_data/contacts.py scripts/tests/test_accounts.py scripts/tests/test_contacts.py
git commit -m "$(cat <<'EOF'
Add Account and Contact generators
EOF
)"
```

---

## Task 3: Opportunity and OpportunityTeamMember generators

**Files:**
- Create: `scripts/crm_data/opportunities.py`
- Create: `scripts/crm_data/opportunity_team_members.py`
- Test: `scripts/tests/test_opportunities.py`
- Test: `scripts/tests/test_opportunity_team_members.py`

**Interfaces:**
- Consumes: `accounts` (list[dict] from Task 2, needs `account_id`), `roster` (list[dict] from Task 1, needs `se_id`, `pod`, `role`).
- Produces: `crm_data.opportunities.generate_opportunities(rng, accounts, count=350) -> list[dict]`, each dict has `opportunity_id` (str, `"OPP-0001"`), `account_id` (FK), `stage` (str), `amount` (int), `close_date` (str, ISO `YYYY-MM-DD`), `pod` (str), `product_line` (str), `primary_competitor` (str or `""`).
- Produces: `crm_data.opportunities.STAGES`, `crm_data.opportunities.PRODUCT_LINES`, `crm_data.opportunities.COMPETITORS` (module-level lists).
- Produces: `crm_data.opportunity_team_members.generate_opportunity_team_members(rng, opportunities, roster, count=400) -> list[dict]`, each dict has `team_member_id` (str, `"OTM-0001"`), `opportunity_id` (FK), `member_type` (one of `"AE"`, `"SE"`), `member_name` (str — free text for AE since there's no AE roster; the `se_id` for SE), `role` (str, e.g. `"Primary SE"`, `"Deal Owner"`).

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_opportunities.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities, STAGES, PRODUCT_LINES


def test_opportunity_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    assert len(opps) == 350
    assert opps[0]["opportunity_id"] == "OPP-0001"
    assert opps[-1]["opportunity_id"] == "OPP-0350"


def test_opportunity_account_ids_reference_existing_accounts():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    valid_ids = {a["account_id"] for a in accounts}
    for o in opps:
        assert o["account_id"] in valid_ids


def test_opportunity_stage_and_product_line_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    for o in opps:
        assert o["stage"] in STAGES
        assert o["product_line"] in PRODUCT_LINES
        assert isinstance(o["amount"], int) and o["amount"] > 0


def test_closed_lost_or_won_opportunities_have_past_or_future_dates_as_strings():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    for o in opps:
        # ISO format YYYY-MM-DD, 10 chars, two dashes
        assert len(o["close_date"]) == 10
        assert o["close_date"][4] == "-" and o["close_date"][7] == "-"
```

Create `scripts/tests/test_opportunity_team_members.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.roster import generate_se_roster
from crm_data.opportunity_team_members import generate_opportunity_team_members


def test_team_member_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    members = generate_opportunity_team_members(rng, opps, roster, count=400)
    assert len(members) == 400
    assert members[0]["team_member_id"] == "OTM-0001"
    assert members[-1]["team_member_id"] == "OTM-0400"


def test_team_member_opportunity_ids_reference_existing_opportunities():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    members = generate_opportunity_team_members(rng, opps, roster, count=400)
    valid_ids = {o["opportunity_id"] for o in opps}
    for m in members:
        assert m["opportunity_id"] in valid_ids


def test_se_team_members_reference_existing_roster_ids():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    members = generate_opportunity_team_members(rng, opps, roster, count=400)
    valid_se_ids = {r["se_id"] for r in roster}
    for m in members:
        if m["member_type"] == "SE":
            assert m["member_name"] in valid_se_ids
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts/tests && python3 -m pytest test_opportunities.py test_opportunity_team_members.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'crm_data.opportunities'`

- [ ] **Step 3: Write the Opportunity generator**

Create `scripts/crm_data/opportunities.py`:

```python
"""Generates Opportunity (deal) records linked to Accounts."""

import random

from faker import Faker

STAGES = [
    "Discovery",
    "Technical Validation",
    "POC",
    "Business Case",
    "Negotiation",
    "Closed Won",
    "Closed Lost",
]

PRODUCT_LINES = ["Lakehouse Core", "PipelineOps", "ModelServe", "Governance Suite"]

COMPETITORS = ["Databricks", "Snowflake", "Confluent", ""]

POD_NAMES = ["Enterprise", "Strategic", "Mid-Market"]


def generate_opportunities(
    rng: random.Random, accounts: list[dict], count: int = 350
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    account_ids = [a["account_id"] for a in accounts]

    opportunities = []
    for i in range(1, count + 1):
        stage = rng.choice(STAGES)
        amount = rng.randint(40_000, 1_200_000)
        close_date = fake.date_between(start_date="-6M", end_date="+6M")

        opportunities.append(
            {
                "opportunity_id": f"OPP-{i:04d}",
                "account_id": rng.choice(account_ids),
                "stage": stage,
                "amount": amount,
                "close_date": close_date.isoformat(),
                "pod": rng.choice(POD_NAMES),
                "product_line": rng.choice(PRODUCT_LINES),
                "primary_competitor": rng.choice(COMPETITORS),
            }
        )
    return opportunities
```

- [ ] **Step 4: Write the OpportunityTeamMember generator**

Create `scripts/crm_data/opportunity_team_members.py`:

```python
"""Links AEs and SEs to Opportunities."""

import random

from faker import Faker

SE_ROLES = ["Primary SE", "Supporting SE"]
AE_ROLES = ["Deal Owner"]


def generate_opportunity_team_members(
    rng: random.Random,
    opportunities: list[dict],
    roster: list[dict],
    count: int = 400,
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    se_ids_by_pod: dict[str, list[str]] = {}
    for r in roster:
        if r["role"] == "SE":
            se_ids_by_pod.setdefault(r["pod"], []).append(r["se_id"])
    all_se_ids = [r["se_id"] for r in roster if r["role"] == "SE"]

    members = []
    opp_index = 0
    for i in range(1, count + 1):
        opp = opportunities[opp_index % len(opportunities)]
        opp_index += 1

        if i % 2 == 1:
            members.append(
                {
                    "team_member_id": f"OTM-{i:04d}",
                    "opportunity_id": opp["opportunity_id"],
                    "member_type": "AE",
                    "member_name": fake.name(),
                    "role": rng.choice(AE_ROLES),
                }
            )
        else:
            pod_ses = se_ids_by_pod.get(opp["pod"], all_se_ids)
            members.append(
                {
                    "team_member_id": f"OTM-{i:04d}",
                    "opportunity_id": opp["opportunity_id"],
                    "member_type": "SE",
                    "member_name": rng.choice(pod_ses),
                    "role": rng.choice(SE_ROLES),
                }
            )
    return members
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd scripts/tests && python3 -m pytest test_opportunities.py test_opportunity_team_members.py -v`
Expected: PASS (7 passed)

- [ ] **Step 6: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add scripts/crm_data/opportunities.py scripts/crm_data/opportunity_team_members.py scripts/tests/test_opportunities.py scripts/tests/test_opportunity_team_members.py
git commit -m "$(cat <<'EOF'
Add Opportunity and OpportunityTeamMember generators
EOF
)"
```

---

## Task 4: POC__c and SE_Activity__c generators

**Files:**
- Create: `scripts/crm_data/pocs.py`
- Create: `scripts/crm_data/se_activities.py`
- Test: `scripts/tests/test_pocs.py`
- Test: `scripts/tests/test_se_activities.py`

**Interfaces:**
- Consumes: `opportunities` (Task 3, needs `opportunity_id`), `roster` (Task 1, needs `se_id`, `role`).
- Produces: `crm_data.pocs.generate_pocs(rng, opportunities, count=120) -> list[dict]`, each dict has `poc_id` (str, `"POC-0001"`), `opportunity_id` (FK), `start_date`, `end_date` (ISO strings), `success_criteria` (str), `status` (one of `"Not Started"`, `"In Progress"`, `"At Risk"`, `"Completed - Success"`, `"Completed - Failed"`), `environment_type` (one of `"Customer Cloud"`, `"Fluxora Sandbox"`, `"Hybrid"`).
- Produces: `crm_data.pocs.STATUSES`, `crm_data.pocs.ENVIRONMENT_TYPES`.
- Produces: `crm_data.se_activities.generate_se_activities(rng, opportunities, roster, count=900) -> list[dict]`, each dict has `activity_id` (str, `"ACT-0001"`), `opportunity_id` (FK), `se_id` (FK into roster, only `role == "SE"` or `"SE Manager"`), `activity_type` (one of `"Discovery Call"`, `"Technical Demo"`, `"POC Check-in"`, `"RFP Work"`, `"Internal Sync"`), `activity_date` (ISO string), `notes` (str).
- Produces: `crm_data.se_activities.ACTIVITY_TYPES`.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_pocs.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.pocs import generate_pocs, STATUSES, ENVIRONMENT_TYPES


def test_poc_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    pocs = generate_pocs(rng, opps, count=120)
    assert len(pocs) == 120
    assert pocs[0]["poc_id"] == "POC-0001"
    assert pocs[-1]["poc_id"] == "POC-0120"


def test_poc_opportunity_ids_reference_existing_opportunities():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    pocs = generate_pocs(rng, opps, count=120)
    valid_ids = {o["opportunity_id"] for o in opps}
    for p in pocs:
        assert p["opportunity_id"] in valid_ids


def test_poc_status_and_environment_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    pocs = generate_pocs(rng, opps, count=120)
    for p in pocs:
        assert p["status"] in STATUSES
        assert p["environment_type"] in ENVIRONMENT_TYPES
        assert p["success_criteria"]
```

Create `scripts/tests/test_se_activities.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.roster import generate_se_roster
from crm_data.se_activities import generate_se_activities, ACTIVITY_TYPES


def test_activity_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    activities = generate_se_activities(rng, opps, roster, count=900)
    assert len(activities) == 900
    assert activities[0]["activity_id"] == "ACT-0001"
    assert activities[-1]["activity_id"] == "ACT-0900"


def test_activity_foreign_keys_reference_existing_rows():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    activities = generate_se_activities(rng, opps, roster, count=900)
    valid_opp_ids = {o["opportunity_id"] for o in opps}
    valid_se_ids = {r["se_id"] for r in roster if r["role"] in ("SE", "SE Manager")}
    for a in activities:
        assert a["opportunity_id"] in valid_opp_ids
        assert a["se_id"] in valid_se_ids
        assert a["activity_type"] in ACTIVITY_TYPES
        assert a["notes"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts/tests && python3 -m pytest test_pocs.py test_se_activities.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'crm_data.pocs'`

- [ ] **Step 3: Write the POC__c generator**

Create `scripts/crm_data/pocs.py`:

```python
"""Generates POC (proof-of-concept) tracking records linked to Opportunities."""

import random
from datetime import timedelta

from faker import Faker

STATUSES = [
    "Not Started",
    "In Progress",
    "At Risk",
    "Completed - Success",
    "Completed - Failed",
]

ENVIRONMENT_TYPES = ["Customer Cloud", "Fluxora Sandbox", "Hybrid"]

SUCCESS_CRITERIA_TEMPLATES = [
    "Ingest {n}TB of historical data within SLA",
    "Achieve sub-{n}s query latency on the benchmark dashboard",
    "Migrate {n} existing pipelines with zero data loss",
    "Deploy {n} ML models to production via ModelServe",
    "Demonstrate role-based access control across {n} business units",
]


def generate_pocs(
    rng: random.Random, opportunities: list[dict], count: int = 120
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    opportunity_ids = [o["opportunity_id"] for o in opportunities]

    pocs = []
    for i in range(1, count + 1):
        start_date = fake.date_between(start_date="-4M", end_date="today")
        duration_days = rng.randint(14, 45)
        end_date = start_date + timedelta(days=duration_days)
        template = rng.choice(SUCCESS_CRITERIA_TEMPLATES)
        n = rng.choice([1, 2, 3, 5, 10])

        pocs.append(
            {
                "poc_id": f"POC-{i:04d}",
                "opportunity_id": rng.choice(opportunity_ids),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "success_criteria": template.format(n=n),
                "status": rng.choice(STATUSES),
                "environment_type": rng.choice(ENVIRONMENT_TYPES),
            }
        )
    return pocs
```

- [ ] **Step 4: Write the SE_Activity__c generator**

Create `scripts/crm_data/se_activities.py`:

```python
"""Generates SE activity log records (calls, demos, RFP work, check-ins)."""

import random

from faker import Faker

ACTIVITY_TYPES = [
    "Discovery Call",
    "Technical Demo",
    "POC Check-in",
    "RFP Work",
    "Internal Sync",
]

NOTE_TEMPLATES = {
    "Discovery Call": "Discussed current {tag} stack and pain points around scaling data pipelines.",
    "Technical Demo": "Walked through {tag} integration and answered questions on governance controls.",
    "POC Check-in": "Reviewed POC progress against success criteria; {tag} environment stable.",
    "RFP Work": "Drafted responses covering {tag} security and compliance questions.",
    "Internal Sync": "Synced with AE on deal strategy and next steps involving {tag}.",
}

TAGS = ["Lakehouse Core", "PipelineOps", "ModelServe", "Governance Suite"]


def generate_se_activities(
    rng: random.Random,
    opportunities: list[dict],
    roster: list[dict],
    count: int = 900,
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    opportunity_ids = [o["opportunity_id"] for o in opportunities]
    se_ids = [r["se_id"] for r in roster if r["role"] in ("SE", "SE Manager")]

    activities = []
    for i in range(1, count + 1):
        activity_type = rng.choice(ACTIVITY_TYPES)
        tag = rng.choice(TAGS)
        activities.append(
            {
                "activity_id": f"ACT-{i:04d}",
                "opportunity_id": rng.choice(opportunity_ids),
                "se_id": rng.choice(se_ids),
                "activity_type": activity_type,
                "activity_date": fake.date_between(
                    start_date="-4M", end_date="today"
                ).isoformat(),
                "notes": NOTE_TEMPLATES[activity_type].format(tag=tag),
            }
        )
    return activities
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd scripts/tests && python3 -m pytest test_pocs.py test_se_activities.py -v`
Expected: PASS (7 passed)

- [ ] **Step 6: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add scripts/crm_data/pocs.py scripts/crm_data/se_activities.py scripts/tests/test_pocs.py scripts/tests/test_se_activities.py
git commit -m "$(cat <<'EOF'
Add POC and SE_Activity generators
EOF
)"
```

---

## Task 5: Competitor_Mention__c and RFP_Response__c generators

**Files:**
- Create: `scripts/crm_data/competitor_mentions.py`
- Create: `scripts/crm_data/rfp_responses.py`
- Test: `scripts/tests/test_competitor_mentions.py`
- Test: `scripts/tests/test_rfp_responses.py`

**Interfaces:**
- Consumes: `opportunities` (Task 3, needs `opportunity_id`).
- Produces: `crm_data.competitor_mentions.generate_competitor_mentions(rng, opportunities, count=150) -> list[dict]`, each dict has `mention_id` (str, `"CMP-0001"`), `opportunity_id` (FK), `competitor_name` (one of `"Databricks"`, `"Snowflake"`, `"Confluent"`), `context` (str), `threat_level` (one of `"Low"`, `"Medium"`, `"High"`).
- Produces: `crm_data.competitor_mentions.COMPETITOR_NAMES`, `crm_data.competitor_mentions.THREAT_LEVELS`.
- Produces: `crm_data.rfp_responses.generate_rfp_responses(rng, opportunities, count=70) -> list[dict]`, each dict has `rfp_response_id` (str, `"RFP-0001"`), `opportunity_id` (str or `""` — empty string, not FK, for ~30% of rows representing reusable master answers not tied to a deal), `question` (str), `category` (one of `"Security"`, `"Compliance"`, `"Data Governance"`, `"Architecture"`, `"Pricing & Licensing"`), `answer_text` (str).
- Produces: `crm_data.rfp_responses.CATEGORIES`.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_competitor_mentions.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.competitor_mentions import (
    generate_competitor_mentions,
    COMPETITOR_NAMES,
    THREAT_LEVELS,
)


def test_mention_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    mentions = generate_competitor_mentions(rng, opps, count=150)
    assert len(mentions) == 150
    assert mentions[0]["mention_id"] == "CMP-0001"
    assert mentions[-1]["mention_id"] == "CMP-0150"


def test_mention_opportunity_ids_reference_existing_opportunities():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    mentions = generate_competitor_mentions(rng, opps, count=150)
    valid_ids = {o["opportunity_id"] for o in opps}
    for m in mentions:
        assert m["opportunity_id"] in valid_ids


def test_mention_competitor_and_threat_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    mentions = generate_competitor_mentions(rng, opps, count=150)
    for m in mentions:
        assert m["competitor_name"] in COMPETITOR_NAMES
        assert m["threat_level"] in THREAT_LEVELS
        assert m["context"]
```

Create `scripts/tests/test_rfp_responses.py`:

```python
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.rfp_responses import generate_rfp_responses, CATEGORIES


def test_rfp_response_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    assert len(responses) == 70
    assert responses[0]["rfp_response_id"] == "RFP-0001"
    assert responses[-1]["rfp_response_id"] == "RFP-0070"


def test_rfp_response_opportunity_ids_are_valid_or_blank():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    valid_ids = {o["opportunity_id"] for o in opps}
    for r in responses:
        assert r["opportunity_id"] == "" or r["opportunity_id"] in valid_ids


def test_rfp_response_has_some_master_answers():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    master_answers = [r for r in responses if r["opportunity_id"] == ""]
    assert len(master_answers) > 0


def test_rfp_response_category_and_text_fields():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    for r in responses:
        assert r["category"] in CATEGORIES
        assert r["question"]
        assert r["answer_text"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts/tests && python3 -m pytest test_competitor_mentions.py test_rfp_responses.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'crm_data.competitor_mentions'`

- [ ] **Step 3: Write the Competitor_Mention__c generator**

Create `scripts/crm_data/competitor_mentions.py`:

```python
"""Generates competitor-mention records linked to Opportunities."""

import random

COMPETITOR_NAMES = ["Databricks", "Snowflake", "Confluent"]
THREAT_LEVELS = ["Low", "Medium", "High"]

CONTEXT_TEMPLATES = {
    "Databricks": "Customer's data science team already has {competitor} notebooks in production; migration friction is the main objection.",
    "Snowflake": "Customer standardized on {competitor} for warehousing and is comparing total cost of ownership.",
    "Confluent": "Customer runs {competitor} for streaming and wants to know how PipelineOps interoperates with existing Kafka topics.",
}


def generate_competitor_mentions(
    rng: random.Random, opportunities: list[dict], count: int = 150
) -> list[dict]:
    opportunity_ids = [o["opportunity_id"] for o in opportunities]

    mentions = []
    for i in range(1, count + 1):
        competitor = rng.choice(COMPETITOR_NAMES)
        mentions.append(
            {
                "mention_id": f"CMP-{i:04d}",
                "opportunity_id": rng.choice(opportunity_ids),
                "competitor_name": competitor,
                "context": CONTEXT_TEMPLATES[competitor].format(competitor=competitor),
                "threat_level": rng.choice(THREAT_LEVELS),
            }
        )
    return mentions
```

- [ ] **Step 4: Write the RFP_Response__c generator**

Create `scripts/crm_data/rfp_responses.py`:

```python
"""Generates RFP/security-questionnaire response records.

Roughly 30% of rows are reusable "master answers" not tied to any single
Opportunity (opportunity_id == ""); the rest are deal-specific responses.
"""

import random

CATEGORIES = [
    "Security",
    "Compliance",
    "Data Governance",
    "Architecture",
    "Pricing & Licensing",
]

QA_TEMPLATES = {
    "Security": (
        "Does Fluxora encrypt data at rest and in transit?",
        "Yes. All data at rest is encrypted with AES-256, and all data in transit uses TLS 1.2+.",
    ),
    "Compliance": (
        "Is Fluxora SOC 2 Type II certified?",
        "Yes, Fluxora maintains a current SOC 2 Type II report, available under NDA upon request.",
    ),
    "Data Governance": (
        "How does Fluxora support role-based access control across business units?",
        "Governance Suite provides row- and column-level access policies scoped by team, workspace, or business unit.",
    ),
    "Architecture": (
        "Can Fluxora deploy in a customer's own cloud VPC?",
        "Yes, Lakehouse Core supports customer-managed VPC deployment on AWS, GCP, and Azure.",
    ),
    "Pricing & Licensing": (
        "Is pricing based on compute usage or seat count?",
        "Fluxora pricing is primarily consumption-based (compute + storage), with optional seat-based add-ons for Governance Suite.",
    ),
}


def generate_rfp_responses(
    rng: random.Random, opportunities: list[dict], count: int = 70
) -> list[dict]:
    opportunity_ids = [o["opportunity_id"] for o in opportunities]

    responses = []
    for i in range(1, count + 1):
        category = rng.choice(CATEGORIES)
        question, answer = QA_TEMPLATES[category]
        is_master_answer = rng.random() < 0.3
        responses.append(
            {
                "rfp_response_id": f"RFP-{i:04d}",
                "opportunity_id": "" if is_master_answer else rng.choice(opportunity_ids),
                "question": question,
                "category": category,
                "answer_text": answer,
            }
        )
    return responses
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd scripts/tests && python3 -m pytest test_competitor_mentions.py test_rfp_responses.py -v`
Expected: PASS (7 passed)

- [ ] **Step 6: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add scripts/crm_data/competitor_mentions.py scripts/crm_data/rfp_responses.py scripts/tests/test_competitor_mentions.py scripts/tests/test_rfp_responses.py
git commit -m "$(cat <<'EOF'
Add Competitor_Mention and RFP_Response generators
EOF
)"
```

---

## Task 6: Main script — orchestration, CSV writing, and determinism test

**Files:**
- Create: `scripts/generate_crm_data.py`
- Create: `scripts/crm_data/csv_writer.py`
- Test: `scripts/tests/test_generate_crm_data.py`

**Interfaces:**
- Consumes: every generator from Tasks 1-5 (`generate_se_roster`, `generate_accounts`, `generate_contacts`, `generate_opportunities`, `generate_opportunity_team_members`, `generate_pocs`, `generate_se_activities`, `generate_competitor_mentions`, `generate_rfp_responses`).
- Produces: `crm_data.csv_writer.write_csv(rows: list[dict], path: str) -> None` — writes `rows` to `path` using `csv.DictWriter`, header from the first row's keys, `newline=""` to avoid extra blank lines on any platform.
- Produces: `scripts/generate_crm_data.py` as a runnable script (`python3 generate_crm_data.py`) that writes all 8 CSVs to `output/` relative to the repo root, and prints a one-line summary per file (name + row count).

- [ ] **Step 1: Write the failing test for the CSV writer**

Create `scripts/tests/test_generate_crm_data.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts/tests && python3 -m pytest test_generate_crm_data.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'crm_data.csv_writer'`

- [ ] **Step 3: Write the CSV writer helper**

Create `scripts/crm_data/csv_writer.py`:

```python
"""Writes a list of flat dicts to a CSV file with a header row."""

import csv


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        raise ValueError(f"Cannot write CSV with no rows: {path}")

    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
```

- [ ] **Step 4: Write the main orchestration script**

Create `scripts/generate_crm_data.py`:

```python
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
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd scripts/tests && python3 -m pytest test_generate_crm_data.py -v`
Expected: PASS (4 passed)

- [ ] **Step 6: Run the full test suite**

Run: `cd scripts/tests && python3 -m pytest -v`
Expected: All tests across all files PASS (approx. 34 passed)

- [ ] **Step 7: Run the script for real and inspect output**

Run: `cd /Users/aprokaeva/TECH/personal/CRM_agent/scripts && python3 generate_crm_data.py`
Expected output (row counts, order may vary slightly in wording but not values):
```
accounts.csv: 200 rows
contacts.csv: 600 rows
opportunities.csv: 350 rows
opportunity_team_members.csv: 400 rows
pocs.csv: 120 rows
se_activities.csv: 900 rows
competitor_mentions.csv: 150 rows
rfp_responses.csv: 70 rows
```
Then spot-check: `head -5 /Users/aprokaeva/TECH/personal/CRM_agent/output/accounts.csv`

- [ ] **Step 8: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add scripts/generate_crm_data.py scripts/crm_data/csv_writer.py scripts/tests/test_generate_crm_data.py output/
git commit -m "$(cat <<'EOF'
Add main CRM data generation script and generated output
EOF
)"
```

---

## Task 7: ChatGPT Enterprise setup guideline document

**Files:**
- Create: `docs/chatgpt-enterprise-setup-guide.md`

**Interfaces:**
- None (standalone Markdown document; no code dependencies).

- [ ] **Step 1: Write the guideline document**

Create `docs/chatgpt-enterprise-setup-guide.md`:

```markdown
# Setting Up "Fluxora SE Copilot" in ChatGPT Enterprise

> **Caveat:** ChatGPT Enterprise's Agent/Skill/Connector feature set is new
> and actively evolving as of this writing (mid-2026). Menu names, exact
> steps, and capability boundaries described below may have shifted by the
> time you read this — treat this as directionally accurate, not a pinned
> reference. Where a claim is time-sensitive, it's flagged explicitly.
>
> This guide is documentation only. No agent, skill, or connector described
> here has been created in a live workspace, and no CRM system is actually
> connected — see the design spec's "Out of Scope" section.

## 1. Create the Workspace Agent

1. In ChatGPT Enterprise, open the workspace admin's **Agents** area
   (sidebar → Agents, or Settings → Agents depending on your workspace's
   rollout). Agent creation/building/publishing are gated by workspace
   RBAC toggles — a workspace admin must enable "allow building agents"
   for your role before you'll see a create option.
2. Create a new agent named **"Fluxora SE Copilot"**.
3. Set the agent's **instructions** to describe its role: a Sales
   Engineering assistant for Fluxora, a data/AI infrastructure company,
   that helps SEs with discovery prep, POC tracking, RFP drafting, and
   deal briefs, always grounding answers in the connected CRM data and
   uploaded knowledge files rather than invented facts.
4. Pick a model appropriate for reasoning over structured CRM data and
   drafting long-form text (a mid-to-high-reasoning-tier model, not the
   fastest/cheapest tier).

## 2. Define the Four Skills

Configure each of the following as a distinct Skill under the agent, so a
user can invoke them explicitly (e.g. via a slash command or a labeled
button) rather than relying on the agent to infer intent every time:

| Skill | What it should do | Primary CRM objects it reads |
|---|---|---|
| **Discovery Prep** | Given an Account name or Opportunity ID, summarize company background, infer likely pain points, and draft discovery questions. | Account, Contact, SE_Activity__c |
| **POC Tracker** | Given an SE name or pod, list active POCs, flag ones that are stalled or missing success criteria, and draft a status update. | POC__c, Opportunity |
| **RFP Drafting** | Given a pasted question or uploaded questionnaire, draft answers reusing past RFP_Response__c records and flag gaps needing SME input. | RFP_Response__c, knowledge files |
| **Deal Brief** | Given an Opportunity ID, produce an AE-facing brief covering deal health, competitive landscape, and next steps. | Opportunity, OpportunityTeamMember, SE_Activity__c, Competitor_Mention__c |

Each Skill's own instructions should specify its expected input, which CRM
objects/fields it's allowed to read, and the output format (e.g. Deal
Brief should always produce the same section headers so AEs can skim it
quickly).

## 3. Upload Knowledge Files

Upload reference material the agent should retrieve from but never
treat as instructions:

- Product battlecards (one per product line: Lakehouse Core, PipelineOps,
  ModelServe, Governance Suite)
- Competitor comparison sheets (Databricks, Snowflake, Confluent)
- A master RFP answer document (a superset of the `rfp_responses.csv`
  rows where `opportunity_id` is blank)

As of this writing, ChatGPT's knowledge file limits are on the order of a
few dozen files and several hundred MB per file — check your workspace's
current documented limits before uploading, since these numbers move
between releases.

## 4. Configure the CRM Connector (Conceptual)

This demo does not connect a live CRM. If you were to wire this up for
real, the current recommended pattern is:

1. The CRM (e.g. Salesforce) exposes its data via a **hosted MCP server**
   rather than a hand-written OpenAPI Action — this is the direction
   OpenAI and major CRM vendors have been moving, and it typically
   supports finer-grained, per-user permission enforcement than a shared
   API key.
2. In the ChatGPT Enterprise workspace, an admin registers the CRM's MCP
   server as a **Connector** under Workspace Settings → Apps/Connectors,
   authenticating via OAuth (the CRM side is typically an OAuth client
   registration distinct from a legacy "Connected App" — check your CRM's
   current terminology).
3. Scope the connector to **read-only** access across the 8 objects in
   this dataset (Account, Contact, Opportunity, OpportunityTeamMember,
   POC__c, SE_Activity__c, Competitor_Mention__c, RFP_Response__c) for the
   Discovery Prep, POC Tracker, and Deal Brief skills.
4. If you later want the RFP Drafting skill (or any skill) to *write*
   back to the CRM — e.g., saving a drafted RFP answer as a new
   RFP_Response__c row — gate that specific write action behind an
   explicit per-action approval step, so no CRM record changes without a
   human confirming it first.

## 5. Workspace Admin Controls to Review

Before publishing this agent org-wide, a workspace admin should check:

- **Who can create/edit/publish agents** — RBAC toggles for "enable
  agents," "enable building," and "enable publishing" (and, separately,
  "enable publishing with personal connections," which controls whether a
  published agent can carry over an individual's personal connector
  authorizations to other users — you do NOT want this enabled for a
  shared CRM connector).
- **Connector/domain allowlisting** — whether the workspace restricts
  which external domains or MCP servers an agent is allowed to connect
  to. If the CRM's MCP server domain isn't allowlisted, the connector
  won't be selectable when configuring the agent.
- **Sharing scope** — whether "Fluxora SE Copilot" is shared with the
  whole workspace, just the SE org, or a smaller pilot group first.

## 6. Fallback: Custom GPT + Actions

If your workspace doesn't yet have Agents/Skills enabled, the same
narrative can be approximated with a classic **Custom GPT**:

- Build one Custom GPT ("Fluxora SE Copilot") via the GPT Builder/Editor
  (chatgpt.com/gpts → Create).
- Use the GPT's **Instructions** field to describe all four workflows
  (Discovery Prep, POC Tracker, RFP Drafting, Deal Brief) as sections,
  since Custom GPTs have no first-class Skill concept — the GPT infers
  which "mode" to use from the user's request or from **Conversation
  Starters** you define per workflow.
- Connect the CRM via a custom **Action** (OpenAPI schema + API key or
  OAuth), instead of a Connector. Note the platform constraint: a GPT can
  use *either* Actions *or* Apps/Connectors, not both — so if you need
  both a CRM Action and a separate pre-built App/Connector, this fallback
  path won't support that combination and you'd need the full Agent
  path instead.
- Upload the same knowledge files as described in Section 3.

This fallback is simpler to set up but is a strictly smaller feature set
than the Agent + Skills + Connector path — use it only if Agents aren't
available in your workspace yet.
```

- [ ] **Step 2: Verify the file was created correctly**

Run: `cat /Users/aprokaeva/TECH/personal/CRM_agent/docs/chatgpt-enterprise-setup-guide.md | head -20`
Expected: renders the title and caveat block without errors.

- [ ] **Step 3: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add docs/chatgpt-enterprise-setup-guide.md
git commit -m "$(cat <<'EOF'
Add ChatGPT Enterprise setup guideline document
EOF
)"
```

---

## Task 8: Top-level README tying it all together

**Files:**
- Create: `README.md`

**Interfaces:**
- None (standalone Markdown document).

- [ ] **Step 1: Write the README**

Create `README.md`:

```markdown
# Fluxora SE Copilot Demo

A demo of how a ChatGPT Enterprise workspace — with a custom Agent, Skills,
and a CRM Connector — could help a Sales Engineer at a fictional,
aggressively-scaling data/AI infrastructure company ("Fluxora") do their
day-to-day job.

This repo contains the **design spec**, the **synthetic CRM data
generator**, and the **ChatGPT Enterprise setup guide** for the demo. No
live system is connected — see "Scope" below.

## Contents

- `docs/superpowers/specs/2026-07-16-crm-agent-demo-design.md` — the full
  design spec: business narrative, agent/skill architecture, CRM data
  model, and script plan.
- `docs/superpowers/plans/2026-07-16-crm-agent-demo.md` — the
  implementation plan that produced this repo's code.
- `docs/chatgpt-enterprise-setup-guide.md` — step-by-step guidance for
  configuring the corresponding Agent, Skills, and Connector in a real
  ChatGPT Enterprise workspace.
- `scripts/generate_crm_data.py` — generates the synthetic CRM dataset.
- `output/*.csv` — the generated dataset (8 files, one per CRM object).

## Running the data generator

```bash
cd scripts
python3 generate_crm_data.py
```

Requires Python 3 and the `faker` package (`pip3 install faker`). Writes 8
CSV files to `../output/`. Uses a fixed random seed, so re-running produces
identical output.

Run the test suite with:

```bash
cd scripts/tests
python3 -m pytest -v
```

## Scope

This repo produces data and documentation only. It does not create any
agent, skill, or connector in a live ChatGPT Enterprise workspace, and does
not connect the generated data to any real CRM system.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/aprokaeva/TECH/personal/CRM_agent
git add README.md
git commit -m "$(cat <<'EOF'
Add top-level README
EOF
)"
```
