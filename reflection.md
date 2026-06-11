# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The  attempt counter already showed 1 instead of 0. 
  - The difficulty selector was visible but the range setting was not correctly applied to the secret number.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  - The attempt counter starts at 1 when the page first loads, instead of 0.
  - The difficulty range is not applied correctly —  the secret number can still be outside that range.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Page first loads | Attempt counter starts at 0 | Attempt counter starts at 1 immediately on load | No errors in console |
| Select "Easy" difficulty, click New Game, start guessing | Secret number should be within Easy's range (e.g. 1–20) | Secret number can be outside the selected range (e.g. 50) | No errors in console |
| Click "New Game" mid-game | All state resets: secret number, attempts, and guess history log all clear | Secret number and attempts reset, but the guess history log is not cleared | No errors in console |
| Submit a guess lower than the secret number | Hint displays "Go higher" | Hint displays "Go lower" (hint logic is inverted) | No errors in console |
| game over then click "New Game" and try to submit a guess | Game resets fully; new guesses can be submitted | secret and attempts update reset but the Submit button no longer responds — game is stuck | No errors in console |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - ChatGPT, Claude, Copilot
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - I described the bug where the first Submit click shows the hint but does not update the attempt counter or history — those only appear on the second click.
  - Streamlit re-runs the entire script from the top on every interaction.
  - Because the display elements (attempt counter and history) are rendered *before* the submit block executes, they always show the previous session state.The hint appears correctly only because it lives inside the submit block.
  - The AI suggested three steps to fix this: storing the hint in `st.session_state` as `last_hint`, calling `st.rerun()` at the end of the submit block to force an immediate re-rende.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - I asked the AI why the `check_guess()` function had unnecessary repetition of the equality check `if g == secret`, and that it was "illogical" because the two values would rarely be equal after a TypeError occurred.
  - It suggested the except block's equality check was unnecessary because TypeError would make them unequal. However, when I traced through the code with `parse_guess()`, I realized the real bug was the string comparison `str(guess) > str(secret)` would produce incorrect results like `str(20) > str(100)` returning `True`.
  - The actual issue was that the entire try-except block was unnecessary since `parse_guess()` already guarantees `guess` is an integer.
  
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - For logic functions in logic_utils.py, I wrote pytest test cases and confirmed the function returned the correct output for known inputs.
  - For Streamlit-related bugs (render order, session state, button behavior), I verified fixes manually by running the app and interacting with it directly
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - I wrote pytest tests for the core logic functions in logic_utils.py.
  - For example, I tested the hint direction function with inputs where the guess was below, above, and equal to the secret number, and tested get_range() to confirm each difficulty level returned the correct boundaries.
  - Running these tests revealed that the hint comparison was inverted — the function was returning "Go lower" when the guess was below the secret number.
- Did AI help you design or understand any tests? How?
  - I was unfamiliar with @pytest.mark.parametrize, so I asked the AI to explain the syntax and how to use it to run the same test across multiple input combinations without repeating code.
  - AI suggested additional edge cases I had not considered for test_update_score — such as what happens when the score is updated at exactly the attempt limit, or when an invalid input is passed. These extra cases helped me catch behavior I would have otherwise missed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Every time a user interacts with the app — clicking a button, changing a slider, submitting a form — Streamlit reruns the entire script from the top, line by line. This means any regular variable gets reset to its initial value on every interaction, which makes it impossible to track things like attempt counts or guess history across clicks.
  - Values stored in session_state persist across reruns — Streamlit keeps them alive between interactions until explicitly change or clear them.
  - This also means the order of the code matters. Since Streamlit renders from top to bottom, any display element that appears before a state update will show the old value. For example, if you display the attempt counter on line 10 but increment it on line 50, the counter will always appear one step behind. The fix is to update state first, then call st.rerun() to trigger a fresh render so all display elements reflect the latest values.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
