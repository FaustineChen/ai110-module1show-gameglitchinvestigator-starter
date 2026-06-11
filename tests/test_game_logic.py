import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# TEST get_range_for_difficulty()
@pytest.mark.parametrize("difficulty,expected_low,expected_high", [
    ("Easy", 1, 20),
    ("Normal", 1, 100),
    ("Hard", 1, 50),
])
def test_get_range_for_difficulty(difficulty, expected_low, expected_high):
    low, high = get_range_for_difficulty(difficulty)
    assert low == expected_low
    assert high == expected_high

# TEST: parse_guess()
@pytest.mark.parametrize("guess_str,expected_ok,expected_guess, expected_error", [
    (None, False, None, "Enter a guess."),
    ("", False, None, "Enter a guess."),
    ("50", True, 50, None),
    ("50.9", True, 50, None),
    ("abc", False, None, "That is not a number."),
])
def test_parse_guess_valid(guess_str, expected_ok, expected_guess, expected_error):
    ok, guess, error = parse_guess(guess_str)
    assert ok == expected_ok
    assert guess == expected_guess
    assert error == expected_error


# TEST: check_guess()
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, word = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, word = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, word = check_guess(40, 50)
    assert result == "Too Low"

# TEST: update_score()
# attempt_number comes in after attempts += 1, so minimum realistic value is 1
@pytest.mark.parametrize("current_score,outcome,attempt_number,expected_score", [
    # Win: points = 100 - 10 * (attempt + 1), minimum 10
    (0,   "Win", 1,  80),   # 100 - 10*2 = 80  (first guess)
    (0,   "Win", 5,  40),   # 100 - 10*6 = 40
    (0,   "Win", 8,  10),   # 100 - 10*9 = 10  (floor)
    (0,   "Win", 9,  10),   # 100 - 10*10 = 0 → clamped to 10
    (50,  "Win", 1,  130),  # non-zero starting score
    # Too High: even attempt → +5, odd attempt → -5
    (100, "Too High", 2, 105),  # even → +5
    (100, "Too High", 4, 105),  # even → +5
    (100, "Too High", 1, 95),   # odd  → -5
    (100, "Too High", 3, 95),   # odd  → -5
    # Too Low: always -5
    (100, "Too Low", 1, 95),
    (100, "Too Low", 4, 95),
    # Unknown outcome: score unchanged
    (100, "Draw",    1, 100),
    (0,   "Invalid", 5, 0),
])
def test_update_score(current_score, outcome, attempt_number, expected_score):
    result = update_score(current_score, outcome, attempt_number)
    assert result == expected_score
