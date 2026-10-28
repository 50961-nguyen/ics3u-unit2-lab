"""Run one tier-appropriate pytest check for GitHub Classroom autograding."""

import argparse
import os
import re
import subprocess
import sys


TIER_ORDER = {"bronze": 0, "silver": 1, "gold": 2}
TEST_TIERS = {
    "test_welcome_message": "bronze",
    "test_name_is_used_in_message": "bronze",
    "test_house_loop_uses_keep_going_then_happy_halloween": "bronze",
    "test_one_house_only_prints_final_message": "bronze",
    "test_candy_bag_prompt_is_printed": "silver",
    "test_sentinel_stops_candy_collection": "silver",
    "test_chocolate_is_counted_and_gets_special_message": "silver",
    "test_other_candy_is_counted_and_gets_tier_message": "silver",
    "test_silver_summary_counts_multiple_candies": "silver",
    "test_silver_candy_names_are_case_sensitive": "silver",
    "test_while_loop_uses_done_sentinel": "silver",
    "test_no_break_statements": "silver",
    "test_no_continue_statements": "silver",
    "test_no_while_true_syntax": "silver",
    "test_gold_rejects_invalid_candy_and_accepts_next_valid": "gold",
    "test_gold_accepts_capitalized_candy_and_sentinel": "gold",
    "test_gold_candy_points": "gold",
    "test_gold_summary_counts_all_candy_types": "gold",
    "test_gold_prize_tier": "gold",
}


def _submitted_tier():
    candidates = []
    for filename in os.listdir("."):
        match = re.fullmatch(
            r"unit[12]_lab_(bronze|silver|gold)\.py", filename, re.IGNORECASE
        )
        if match:
            tier = match.group(1).lower()
            candidates.append((TIER_ORDER[tier], tier))
    if candidates:
        return max(candidates)[1]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_name", choices=TEST_TIERS)
    args = parser.parse_args()

    required_tier = TEST_TIERS[args.test_name]
    submitted_tier = _submitted_tier()
    if submitted_tier is None:
        print(
            "No student file found. Expected unit2_lab_bronze.py, "
            "unit2_lab_silver.py, or unit2_lab_gold.py (unit1_lab_* names "
            "from the README are also accepted)."
        )
        return 1
    if TIER_ORDER[submitted_tier] < TIER_ORDER[required_tier]:
        print(
            f"{required_tier.title()} points require at least the "
            f"{required_tier.title()} tier; submitted tier is "
            f"{submitted_tier.title()}."
        )
        return 1

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "test_unit2_lab.py",
            "-k",
            args.test_name,
        ],
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
