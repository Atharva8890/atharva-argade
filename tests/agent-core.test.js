import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { LocalVoiceAgent } from "../src/agent-core.js";

const fixedClock = () => new Date("2026-06-12T17:45:00Z");

describe("LocalVoiceAgent", () => {
  it("answers help requests with supported commands", () => {
    const agent = new LocalVoiceAgent({ clock: fixedClock });

    const result = agent.respond("help");

    assert.equal(result.intent, "help");
    assert.match(result.response, /set a reminder/i);
  });

  it("stores and lists reminders", () => {
    const agent = new LocalVoiceAgent({ clock: fixedClock });

    const saved = agent.respond("Remind me to review the launch notes.");
    const listed = agent.respond("list reminders");

    assert.equal(saved.intent, "set-reminder");
    assert.deepEqual(saved.reminders, ["review the launch notes"]);
    assert.match(listed.response, /review the launch notes/);
  });

  it("clears reminders", () => {
    const agent = new LocalVoiceAgent({ reminders: ["stretch"], clock: fixedClock });

    const result = agent.respond("clear reminders");

    assert.equal(result.intent, "clear-reminders");
    assert.deepEqual(result.reminders, []);
  });

  it("repeats the last response", () => {
    const agent = new LocalVoiceAgent({ clock: fixedClock });

    const first = agent.respond("what time is it");
    const repeated = agent.respond("repeat that");

    assert.equal(repeated.intent, "repeat");
    assert.equal(repeated.response, first.response);
  });

  it("returns a fallback for unsupported commands", () => {
    const agent = new LocalVoiceAgent({ clock: fixedClock });

    const result = agent.respond("book a flight");

    assert.equal(result.intent, "fallback");
    assert.match(result.response, /local voice commands/i);
  });
});
