"""
Tests for the Unit 2 Halloween Candy Crawl lab.

Each pytest test is an independent grading check that can be assigned points
separately in a GitHub Classroom autograding workflow.

Expected student files:
  Bronze: unit1_lab_bronze.py or unit2_lab_bronze.py
  Silver: unit1_lab_silver.py or unit2_lab_silver.py
  Gold:   unit1_lab_gold.py or unit2_lab_gold.py

When multiple tier files are present, the highest tier is tested.
"""

import ast
import os
import re
import subprocess
import sys

import pytest


TIER_ORDER = {"bronze": 0, "silver": 1, "gold": 2}


def _find_student_file():
    candidates = []
    for filename in os.listdir("."):
        match = re.fullmatch(
            r"unit[12]_lab_(bronze|silver|gold)\.py", filename, re.IGNORECASE
        )
        if match:
            tier = match.group(1).lower()
            candidates.append((TIER_ORDER[tier], filename))
    if candidates:
        return max(candidates)[1]
    return None


STUDENT_FILE = _find_student_file()
TIER = (
    re.search(r"(bronze|silver|gold)", STUDENT_FILE, re.IGNORECASE).group(1).lower()
    if STUDENT_FILE
    else "bronze"
)


def run_script(inputs):
    if STUDENT_FILE is None:
        pytest.fail(
            "No student file found. Expected unit2_lab_bronze.py, "
            "unit2_lab_silver.py, or unit2_lab_gold.py (unit1_lab_* names "
            "from the README are also accepted)."
        )

    try:
        result = subprocess.run(
            [sys.executable, STUDENT_FILE],
            input="\n".join(inputs) + "\n",
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The program did not finish within 10 seconds.")

    assert result.returncode == 0, (
        f"The program exited with status {result.returncode}.\n"
        f"Standard error:\n{result.stderr}\n"
        f"Standard output:\n{result.stdout}"
    )
    return result.stdout


def make_inputs(name="Alex", houses="3", candies=None, sentinel="done"):
    inputs = [name, houses]
    if TIER != "bronze":
        if candies is None:
            candies = ["chocolate", "gummy", "lollipop"]
        inputs.extend(candies)
        inputs.append(sentinel)
    return inputs


def skip_if_bronze():
    if TIER == "bronze":
        pytest.skip("Candy collection is not required for Bronze.")


def skip_if_not_gold():
    if TIER != "gold":
        pytest.skip("Candy validation and scoring are Gold-tier requirements.")


def _student_tree():
    if STUDENT_FILE is None:
        pytest.fail(
            "No student file found. Expected unit2_lab_bronze.py, "
            "unit2_lab_silver.py, or unit2_lab_gold.py (unit1_lab_* names "
            "from the README are also accepted)."
        )
    with open(STUDENT_FILE, encoding="utf-8") as student_file:
        return ast.parse(student_file.read(), filename=STUDENT_FILE)


def _has_done_sentinel(test):
    for node in ast.walk(test):
        if not isinstance(node, ast.Compare):
            continue
        if not any(
            isinstance(operator, (ast.Eq, ast.NotEq)) for operator in node.ops
        ):
            continue
        operands = [node.left, *node.comparators]
        if any(
            isinstance(operand, ast.Constant)
            and isinstance(operand.value, str)
            and operand.value.lower() == "done"
            for operand in operands
        ):
            return True
    return False


# Bronze requirements apply to every tier.

def test_welcome_message():
    output = run_script(make_inputs())
    assert "Welcome to the Celebration Square Halloween Candy Crawl!" in output


def test_name_is_used_in_message():
    output = run_script(make_inputs(name="Jordan", houses="2"))
    assert "Enter your name:" in output
    assert "Enter the amount of houses you visited today:" in output
    assert "Great job Jordan! Let's celebrate each house you visited!" in output


def test_house_loop_uses_keep_going_then_happy_halloween():
    output = run_script(make_inputs(houses="3"))
    lines = output.splitlines()
    assert "House 1 visited! Keep going!" in lines
    assert "House 2 visited! Keep going!" in lines
    assert "House 3 visited! Happy Halloween!" in lines


def test_one_house_only_prints_final_message():
    output = run_script(make_inputs(houses="1"))
    assert "House 1 visited! Happy Halloween!" in output
    assert "Keep going!" not in output


# Silver and Gold requirements.

def test_candy_bag_prompt_is_printed():
    skip_if_bronze()
    output = run_script(make_inputs(candies=["gummy"]))
    assert "Time to log your candy bag!" in output
    assert "Enter each candy type (or 'done' to finish):" in output


def test_sentinel_stops_candy_collection():
    skip_if_bronze()
    output = run_script(make_inputs(candies=[]))
    assert re.search(r"(?i)Total candies:\s*0\b", output)


def test_chocolate_is_counted_and_gets_special_message():
    skip_if_bronze()
    output = run_script(make_inputs(candies=["chocolate"]))
    assert "A chocolate treat! What a classic!" in output
    assert re.search(r"(?i)Total candies:\s*1\b", output)
    assert re.search(r"(?i)Chocolate candies:\s*1\b", output)
    assert "Amazing, Alex! You collected some chocolate!" in output


def test_other_candy_is_counted_and_gets_tier_message():
    skip_if_bronze()
    output = run_script(make_inputs(candies=["gummy"]))
    if TIER == "gold":
        assert "A gummy treat! Spooky and chewy!" in output
    else:
        assert "A gummy treat added to your bag!" in output
    assert re.search(r"(?i)Total candies:\s*1\b", output)
    assert re.search(r"(?i)Chocolate candies:\s*0\b", output)
    assert "No chocolate this time, Alex. Keep trick-or-treating!" in output


def test_silver_summary_counts_multiple_candies():
    skip_if_bronze()
    output = run_script(make_inputs(candies=["gummy", "chocolate"]))
    assert re.search(r"(?i)Total candies:\s*2\b", output)
    assert re.search(r"(?i)Chocolate candies:\s*1\b", output)


def test_silver_candy_names_are_case_sensitive():
    if TIER != "silver":
        pytest.skip("Case-sensitive candy names are a Silver-tier requirement.")
    output = run_script(make_inputs(candies=["Chocolate"]))
    assert "A Chocolate treat added to your bag!" in output
    assert re.search(r"(?i)Chocolate candies:\s*0\b", output)


def test_while_loop_uses_done_sentinel():
    skip_if_bronze()
    loops = [
        node for node in ast.walk(_student_tree()) if isinstance(node, ast.While)
    ]
    assert any(_has_done_sentinel(loop.test) for loop in loops), (
        "A while-loop condition must compare against the 'done' sentinel."
    )


def test_no_break_statements():
    assert not any(isinstance(node, ast.Break) for node in ast.walk(_student_tree())), (
        "Do not use break to exit a loop; use the 'done' sentinel."
    )


def test_no_continue_statements():
    assert not any(
        isinstance(node, ast.Continue) for node in ast.walk(_student_tree())
    ), "Do not use continue in the loop."


def test_no_while_true_syntax():
    while_loops = [
        node for node in ast.walk(_student_tree()) if isinstance(node, ast.While)
    ]
    assert not any(
        isinstance(loop.test, ast.Constant) and loop.test.value is True
        for loop in while_loops
    ), "Use a sentinel or another loop condition instead of while True."


# Gold requirements.

def test_gold_rejects_invalid_candy_and_accepts_next_valid_input():
    skip_if_not_gold()
    output = run_script(make_inputs(candies=["blue", "gummy"]))
    assert "Invalid input." in output
    assert re.search(r"(?i)Total candies:\s*1\b", output)
    assert re.search(r"(?i)Gummy candies:\s*1\b", output)


def test_gold_accepts_capitalized_candy_and_sentinel():
    skip_if_not_gold()
    output = run_script(make_inputs(candies=["Chocolate"], sentinel="DoNe"))
    assert "Invalid input." not in output
    assert re.search(r"(?i)Total candies:\s*1\b", output)
    assert re.search(r"(?i)Chocolate candies:\s*1\b", output)


@pytest.mark.parametrize(
    ("candy", "expected_score"),
    [("chocolate", 10), ("gummy", 5), ("lollipop", 1)],
)
def test_gold_candy_points(candy, expected_score):
    skip_if_not_gold()
    output = run_script(make_inputs(candies=[candy]))
    assert re.search(
        rf"(?im)^(?:Your total score|Total score):\s*{expected_score}\b", output
    )


def test_gold_summary_counts_all_candy_types():
    skip_if_not_gold()
    output = run_script(
        make_inputs(candies=["chocolate", "gummy", "lollipop"])
    )
    assert re.search(r"(?i)Total candies:\s*3\b", output)
    assert re.search(r"(?i)Chocolate candies:\s*1\b", output)
    assert re.search(r"(?i)Gummy candies:\s*1\b", output)
    assert re.search(r"(?i)Lollipops:\s*1\b", output)
    assert re.search(r"(?im)^(?:Your total score|Total score):\s*16\b", output)


@pytest.mark.parametrize(
    ("candies", "expected_prize"),
    [
        (["gummy"], "Better luck next time!"),
        (["chocolate", "lollipop"], "Candy Corn winner!"),
        (["chocolate", "gummy", "lollipop"], "Haunted Basket winner!"),
        (
            ["chocolate", "gummy", "gummy", "lollipop"],
            "Halloween Candy Champion!",
        ),
    ],
)
def test_gold_prize_tier(candies, expected_prize):
    skip_if_not_gold()
    output = run_script(make_inputs(candies=candies))
    assert expected_prize.lower().rstrip("!") in output.lower()
