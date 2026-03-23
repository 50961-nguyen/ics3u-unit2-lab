"""
Unit 1 Lab: Easter Egg Hunt at Celebration Square

Your file must be named unit1_lab_bronze.py, unit1_lab_silver.py,
or unit1_lab_gold.py -- the tier is detected automatically.

TESTS PER TIER
--------------
  Bronze  ->  4 tests
  Silver  ->  8 tests   (Bronze + Silver)
  Gold    ->  13 tests  (Bronze + Silver + Gold)

Skipped tests are normal: they mean that check does not apply to your tier.
"""

import os
import re
import subprocess
import sys

import pytest


# ---------------------------------------------------------------------------
# Auto-detect student file and tier
# ---------------------------------------------------------------------------

def _find_student_file():
    for fname in sorted(os.listdir(".")):
        if re.match(r"unit1_lab_(bronze|silver|gold)\.py$", fname, re.IGNORECASE):
            return fname
    return None


def _detect_tier(sf):
    if sf:
        m = re.search(r"(bronze|silver|gold)", sf, re.IGNORECASE)
        if m:
            return m.group(1).lower()
    return "bronze"


STUDENT_FILE = _find_student_file()
TIER = _detect_tier(STUDENT_FILE)


# ---------------------------------------------------------------------------
# Runner helpers
# ---------------------------------------------------------------------------

def run_script(inputs):
    if STUDENT_FILE is None:
        pytest.fail(
            "No student file found. "
            "Expected unit1_lab_bronze.py, unit1_lab_silver.py, or unit1_lab_gold.py."
        )
    result = subprocess.run(
        [sys.executable, STUDENT_FILE],
        input="\n".join(inputs) + "\n",
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.stdout


def make_inputs(name="Alex", eggs="3", basket=None):
    """
    Build stdin for the current tier.
    basket = list of colours entered into the while loop (sentinel appended automatically).
    Gold tier needs valid inputs (golden / speckled / regular) due to input validation.
    """
    if basket is None:
        basket = ["golden", "regular", "speckled"]
    if TIER == "bronze":
        return [name, eggs]
    else:
        return [name, eggs] + basket + ["done"]


def skip_if_bronze():
    if TIER == "bronze":
        pytest.skip("Not required for Bronze tier.")


def skip_if_not_gold():
    if TIER != "gold":
        pytest.skip("Not required for Bronze or Silver tier.")


# ===========================================================================
# BRONZE  --  all tiers
# ===========================================================================

class TestBronze:

    def test_welcome_message(self):
        """Script prints the Celebration Square welcome message."""
        out = run_script(make_inputs())
        assert "celebration square" in out.lower(), (
            "Expected 'Welcome to the Celebration Square Easter Egg Hunt!' at the start.\n"
            f"Got:\n{out}"
        )

    def test_name_in_output(self):
        """The user's name appears in the output."""
        out = run_script(make_inputs(name="Jordan", eggs="2"))
        assert "Jordan" in out, (
            "Expected the name 'Jordan' to appear in the output.\n"
            f"Got:\n{out}"
        )

    def test_for_loop_keep_going(self):
        """Middle eggs print 'Keep going!' and the last egg prints 'Happy Easter!'."""
        out = run_script(make_inputs(name="Alex", eggs="3"))
        assert "keep going" in out.lower(), (
            "Expected 'Keep going!' for eggs before the last one.\n"
            f"Got:\n{out}"
        )
        assert "happy easter" in out.lower(), (
            "Expected 'Happy Easter!' for the final egg.\n"
            f"Got:\n{out}"
        )

    def test_for_loop_one_egg(self):
        """With only 1 egg, only 'Happy Easter!' appears -- no 'Keep going!'."""
        out = run_script(make_inputs(name="Alex", eggs="1"))
        assert "happy easter" in out.lower(), (
            "Expected 'Happy Easter!' when 1 egg is found.\n"
            f"Got:\n{out}"
        )
        assert "keep going" not in out.lower(), (
            "Should NOT print 'Keep going!' when only 1 egg is found.\n"
            f"Got:\n{out}"
        )


# ===========================================================================
# SILVER  --  silver and gold tiers
# ===========================================================================

class TestSilver:

    def test_sentinel_stops_loop(self):
        """Typing 'done' exits the while loop without hanging."""
        skip_if_bronze()
        try:
            run_script(make_inputs(name="Alex", eggs="2", basket=["golden"]))
        except subprocess.TimeoutExpired:
            pytest.fail(
                "Script timed out -- the while loop may not be checking "
                "for the sentinel value 'done'."
            )

    def test_golden_egg_message(self):
        """Entering 'golden' prints the rare golden egg message."""
        skip_if_bronze()
        out = run_script(make_inputs(name="Alex", eggs="2", basket=["golden"]))
        assert "rare" in out.lower() or "golden egg" in out.lower(), (
            "Expected a special 'very rare' message when 'golden' is entered.\n"
            f"Got:\n{out}"
        )

    def test_total_eggs_in_summary(self):
        """Total egg count in the summary matches how many were entered."""
        skip_if_bronze()
        # 3 eggs entered: golden, regular, speckled
        out = run_script(make_inputs(name="Alex", eggs="2",
                                     basket=["golden", "regular", "speckled"]))
        assert "3" in out, (
            "Expected a total egg count of 3 in the summary.\n"
            f"Got:\n{out}"
        )

    def test_golden_summary_message_with_name(self):
        """When at least one golden egg is found, the message includes the user's name."""
        skip_if_bronze()
        out = run_script(make_inputs(name="Jordan", eggs="2", basket=["golden"]))
        assert "jordan" in out.lower() and "amazing" in out.lower(), (
            "Expected 'Amazing, {name}!' when a golden egg is found.\n"
            f"Got:\n{out}"
        )

    def test_no_golden_summary_message_with_name(self):
        """When no golden eggs are found, the keep hunting message includes the user's name."""
        skip_if_bronze()
        out = run_script(make_inputs(name="Jordan", eggs="2", basket=["regular"]))
        assert "jordan" in out.lower() and (
            "no golden" in out.lower() or "keep hunting" in out.lower()
        ), (
            "Expected 'No golden eggs this time, {name}. Keep hunting!' when no golden.\n"
            f"Got:\n{out}"
        )


# ===========================================================================
# GOLD  --  gold tier only
# ===========================================================================

class TestGold:

    def test_input_validation_rejects_invalid(self):
        """Invalid colour input prints 'Invalid input.' and prompts again."""
        skip_if_not_gold()
        # "blue" is invalid; script should reject it and ask again, then accept "regular"
        out = run_script(make_inputs(name="Alex", eggs="2",
                                     basket=["blue", "regular"]))
        assert "invalid" in out.lower(), (
            "Expected 'Invalid input.' when a colour other than golden/speckled/regular is entered.\n"
            f"Got:\n{out}"
        )

    def test_input_validation_accepts_capitalized(self):
        """Capitalized inputs like 'Golden' are accepted (not rejected as invalid)."""
        skip_if_not_gold()
        out = run_script(make_inputs(name="Alex", eggs="2", basket=["Golden"]))
        assert "invalid" not in out.lower(), (
            "Expected 'Golden' (capitalized) to be accepted as a valid input.\n"
            f"Got:\n{out}"
        )

    def test_total_score_calculation(self):
        """Score = golden×10 + speckled×5 + regular×1. golden+speckled+regular = 16."""
        skip_if_not_gold()
        # 1 golden (10) + 1 speckled (5) + 1 regular (1) = 16
        out = run_script(make_inputs(name="Alex", eggs="2",
                                     basket=["golden", "speckled", "regular"]))
        assert "16" in out, (
            "Expected a total score of 16 (golden=10, speckled=5, regular=1).\n"
            f"Got:\n{out}"
        )

    def test_regular_eggs_in_summary(self):
        """Summary includes a 'Regular eggs:' line."""
        skip_if_not_gold()
        out = run_script(make_inputs(name="Alex", eggs="2", basket=["regular"]))
        assert "regular eggs" in out.lower(), (
            "Expected a 'Regular eggs: X' line in the summary.\n"
            f"Got:\n{out}"
        )

    def test_prize_better_luck(self):
        """Score < 10 -> 'Better luck next time!'"""
        skip_if_not_gold()
        # 3 regular eggs = 3 pts (<10)
        out = run_script(make_inputs(name="Alex", eggs="2",
                                     basket=["regular", "regular", "regular"]))
        assert "better luck" in out.lower(), (
            "Expected 'Better luck next time!' for a score below 10.\n"
            f"Got:\n{out}"
        )

    def test_prize_silver_basket(self):
        """Score 16-20 -> 'Silver Basket winner!'"""
        skip_if_not_gold()
        # 1 golden (10) + 1 speckled (5) + 1 regular (1) = 16
        out = run_script(make_inputs(name="Alex", eggs="2",
                                     basket=["golden", "speckled", "regular"]))
        assert "silver basket" in out.lower() or (
            "silver" in out.lower() and "winner" in out.lower()
        ), (
            "Expected 'Silver Basket winner!' for a score of 16.\n"
            f"Got:\n{out}"
        )

    def test_prize_gold_champion(self):
        """Score 21+ -> 'Gold Basket Champion!'"""
        skip_if_not_gold()
        # 2 golden (20) + 1 speckled (5) = 25
        out = run_script(make_inputs(name="Alex", eggs="2",
                                     basket=["golden", "golden", "speckled"]))
        assert "gold basket" in out.lower() or "champion" in out.lower(), (
            "Expected 'Gold Basket Champion!' for a score of 25.\n"
            f"Got:\n{out}"
        )
