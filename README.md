# Nova Voice Agent

Nova is a self-contained browser voice agent. It uses the Web Speech APIs for
speech recognition and speech synthesis, then routes commands through a small
local agent core.

## What it can do

- Listen through the browser microphone.
- Reply out loud with speech synthesis.
- Accept typed commands when microphone access is unavailable.
- Answer time and date questions.
- Save, list, and clear reminders in the current browser session.
- Repeat the last answer.

## Run locally

```bash
npm start
```

Then open <http://localhost:4173>.

Speech recognition support varies by browser. Chrome, Edge, and other Chromium
browsers provide the best experience. Typed commands work in any modern browser.

## Test

```bash
npm test
```

## Example commands

- "What time is it?"
- "What is the date?"
- "Set a reminder to drink water."
- "List reminders."
- "Clear reminders."
- "Repeat that."
