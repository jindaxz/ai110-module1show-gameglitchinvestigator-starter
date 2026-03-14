from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# FIX: verify inverted-hint bug is gone — guessing 1 when secret is 50
# must say "Too Low", not "Too High"
def test_hint_not_inverted():
    assert check_guess(1, 50) == "Too Low"
    assert check_guess(99, 50) == "Too High"


# FIX: verify the even-attempt string-comparison bug is gone —
# check_guess should always compare numerically
def test_check_guess_numeric_not_string():
    # "9" > "10" lexicographically but 9 < 10 numerically
    assert check_guess(9, 10) == "Too Low"
    assert check_guess(10, 9) == "Too High"


def test_parse_guess_valid():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False


def test_hard_difficulty_range_is_hardest():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    # FIX: Hard should have the widest range
    assert hard_high > normal_high > easy_high


def test_update_score_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 90  # 100 - 10*1


def test_update_score_wrong_guess_decreases():
    score = update_score(50, "Too High", 1)
    assert score == 45
    score = update_score(50, "Too Low", 1)
    assert score == 45
