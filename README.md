# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player picks a difficulty, receives a secret number range, and tries to guess the number within a limited number of attempts. Hints guide the player higher or lower after each wrong guess.

**Bugs found:**
1. **Inverted hint messages** — `check_guess` paired "Too High" with "Go HIGHER!" and "Too Low" with "Go LOWER!" (both backwards).
2. **Even-attempt string comparison** — On every even-numbered attempt `app.py` cast the secret to a string, causing lexicographic instead of numeric comparison (e.g. `"9" > "10"` is True as strings).
3. **Hard difficulty easier than Normal** — `get_range_for_difficulty("Hard")` returned `(1, 50)`, narrower than Normal's `(1, 100)`.
4. **`logic_utils.py` was empty stubs** — All functions raised `NotImplementedError`; logic lived only in `app.py`.
5. **New Game ignored difficulty** — The "New Game" button hardcoded `random.randint(1, 100)` instead of using the selected difficulty range.
6. **Attempts counter off-by-one** — `attempts` initialized to `1` instead of `0`, so the first submit was counted as attempt 2.

**Fixes applied:**
- Moved all logic functions into `logic_utils.py` with correct implementations.
- `check_guess` now returns only the outcome string ("Win" / "Too High" / "Too Low"); messages are looked up in a dict in `app.py`.
- Removed the even/odd secret-string-cast block entirely.
- Fixed Hard difficulty range to `(1, 200)`.
- Fixed "New Game" to use `get_range_for_difficulty` and reset all state.
- Fixed attempts to start at `0`.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
