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

**Describe the game's purpose.**  
This is a number guessing game built with Streamlit. The player selects a difficulty level, which determines the range of the secret number and the number of attempts allowed. The player then submits guesses and receives higher/lower hints after each one, with the goal of guessing the correct number before running out of attempts.

**Detail which bugs you found.**
- Attempt counter started at 1 instead of 0 on first load
- Secret number was generated outside the selected difficulty range
- Clicking "New Game" did not clear the guess history or game status
- Hint direction was inverted — "Go Higher" and "Go Lower" were swapped
- Attempt counter and history did not update on the first Submit click due to Streamlit's top-down render order
- Type mismatch in check_guess caused incorrect comparisons between the guess and secret number

**Explain what fixes you applied.**
- Bugs fixed:
   - Attempt counter initialized to 0 instead of 1 (off-by-one on first load)
   - Difficulty range correctly applied to secret number generation
   - New game reset guess history and status in addition to attempts
   - Inverted hint direction in check_guess ("Go Higher"/"Go Lower" were swapped)
   - Hint display and attempt counter now render correctly after submit (via st.session_state.last_hint + st.rerun() to fix Streamlit render-order issue)
   - Removed type-juggling in check_guess that caused incorrect string comparisons
- Refactor:
   - Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` from app.py into logic_utils.py; app.py now imports from logic_utils


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. On page load, the game starts immediately with Normal difficulty as the default — no need to click "New Game" before your first guess. The attempt counter starts at 0 and the guess history is empty.
2. Type a number into the input field and click "Submit" to make a guess. The attempt counter increments by 1 and the guess appears in the history log. A hint appears indicating whether the secret number is higher or lower than your guess.
3. To change the difficulty, select a different level (Easy, Medium, or Hard) from the selector. The displayed range and attempt limit will update immediately, but you must click "New Game" to generate a new secret number within the updated range.
4. Continue guessing until you either guess the correct number — triggering a success message — or exhaust all allowed attempts, triggering a game over message.
5. Click "New Game" at any point to fully reset the game: the secret number, attempt counter, guess history, and status message all clear and a new round begins within the currently selected difficulty range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
====================================================== test session starts =======================================================
platform win32 -- Python 3.13.6, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\Faustine Chen\FC\Master\CodePath\AI110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 24 items                                                                                                                

tests\test_game_logic.py ........................                                                                           [100%]

======================================================= 24 passed in 0.13s =======================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
