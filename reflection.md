# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the app, three bugs were immediately visible in the Developer Debug Info panel.

- **Inverted hints**: The game said "Go HIGHER!" when my guess was too high and "Go LOWER!" when it was too low — the opposite of what you'd want. The `check_guess` function returned the correct *outcome label* ("Too High" / "Too Low") but paired it with the wrong *message string*, so the guidance sent the player in the wrong direction every time.

- **Every-other-attempt string comparison**: On even-numbered attempts, `app.py` silently converted the secret number to a string before passing it to `check_guess`. This caused the comparison to use Python's lexicographic string ordering rather than numeric ordering (e.g., `"9" > "10"` is `True` as strings but `False` as integers), making the hints unreliable and effectively making the game unwinnable half the time.

- **Hard difficulty was easier than Normal**: `get_range_for_difficulty("Hard")` returned `(1, 50)`, which is a *narrower* range than Normal's `(1, 100)`. Hard should be the hardest, so its range should be wider (I changed it to `(1, 200)`).

Two additional issues:
- `logic_utils.py` contained only `raise NotImplementedError` stubs — all real logic lived in `app.py`, so the existing tests couldn't even be collected.
- The "New Game" button hardcoded `random.randint(1, 100)` instead of using the selected difficulty's range.

---

## 2. How did you use AI as a teammate?

I used **Claude Code (claude-sonnet-4-6)** as the AI assistant throughout this project.

**Correct suggestion:** When I asked the AI to explain the even/odd string-conversion block (`if st.session_state.attempts % 2 == 0: secret = str(...)`), it correctly identified this as an intentional-looking but broken pattern — the string cast was likely meant to simulate a "harder" mode but instead broke numeric comparison. The AI suggested removing the cast entirely and always passing the integer secret to `check_guess`. I verified this in two ways: by reading Python's comparison semantics for mixed types, and by writing `test_check_guess_numeric_not_string` which confirms `check_guess(9, 10) == "Too Low"` (not "Too High" as string comparison would produce).

**Incorrect/misleading suggestion:** The AI initially suggested keeping `update_score`'s bonus-points logic for "Too High" on even attempts (the original code gave `+5` for wrong guesses every other attempt). It framed this as "intentional game design." I rejected this because (a) there was no documentation explaining the intent, (b) it made the score misleading, and (c) it was coupled to the same even/odd attempt counting that was already broken. I simplified `update_score` so any wrong guess always subtracts 5 points. I verified the new behavior with `test_update_score_wrong_guess_decreases`.

---

## 3. Debugging and testing your fixes

To decide a bug was fixed I required two things: a passing automated pytest case **and** a manual play-through of the live Streamlit app that reproduced the original scenario.

For the inverted-hints bug I wrote `test_hint_not_inverted` which asserts `check_guess(1, 50) == "Too Low"` and `check_guess(99, 50) == "Too High"`. Before the fix these would have passed anyway because the outcome label was already correct — the bug was in the *message* string paired with the outcome. So I also manually played the game and confirmed "📉 Go LOWER!" now appears when my guess is above the secret.

For the string-comparison bug I wrote `test_check_guess_numeric_not_string` which tests the exact edge case where lexicographic and numeric ordering diverge (`check_guess(9, 10)`). This test would have failed with the original code because `check_guess` would receive a string secret and fall into the string-comparison branch on even attempts.

The AI helped me design these tests by explaining what minimal input would most clearly expose each bug — essentially "what pair of numbers makes string order and numeric order disagree?" — which I then encoded directly into the test cases.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number *appeared* stable (it used `if "secret" not in st.session_state`) but was effectively unreliable because Streamlit reruns the entire script on every widget interaction. Without `session_state`, any variable assigned at the top of the script would get a fresh `random.randint` call on every rerun, making it impossible to compare a guess to a consistent target. The `session_state` guard `if "secret" not in` is the correct fix — it only generates the number once per session.

A Streamlit "rerun" is like refreshing a web page: every line of the script executes from top to bottom again. `session_state` is a dictionary that survives those reruns, similar to how a browser's `localStorage` survives page reloads. Without it, variables reset on every button click. The fix is to store anything that must persist (the secret, the attempt count, the score) inside `st.session_state` and guard initialization with `if "key" not in st.session_state`.

The change that gave the game a stable secret number was already in the code (`if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high)`), but the "New Game" button was bypassing it by calling `random.randint(1, 100)` unconditionally and without using the selected difficulty range. I fixed the "New Game" handler to also store into `session_state` using the correct difficulty range.

---

## 5. Looking ahead: your developer habits

**Habit to reuse:** Writing a small, failing test *before* touching the code. For the inverted-hints bug, writing `test_hint_not_inverted` first forced me to be precise about what "correct" meant before I started editing. This prevented me from making a change that looked right but still failed the edge case.

**Thing to do differently:** Next time I'll ask the AI to explain *why* suspicious code exists before asking it how to fix it. When I asked "how do I fix this even/odd string conversion?" the AI jumped to solutions. When I instead asked "why would someone have written this?" it gave a much more useful answer that helped me understand the original (broken) intent — which then made the correct fix obvious.

**How this changed my thinking about AI-generated code:** AI-generated code can look plausible and even pass a surface-level read, but it can contain internally consistent bugs — patterns that are logically coherent but semantically wrong (like the even/odd cast). The lesson is that AI code needs the same skeptical review as any other code: run it, probe the edge cases, and don't trust it just because it compiles and looks tidy.
