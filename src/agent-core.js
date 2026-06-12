const DEFAULT_HELP = [
  "Ask me for the time or date.",
  "Say 'set a reminder to call Sam' to save a reminder.",
  "Say 'list reminders' or 'clear reminders'.",
  "Say 'repeat that' to hear my last answer again.",
  "Say 'help' to hear these options."
];

function normalizeText(value) {
  return String(value || "")
    .trim()
    .replace(/\s+/g, " ");
}

function startsWithAny(value, phrases) {
  return phrases.find((phrase) => value.startsWith(phrase));
}

function stripLeadingCommand(value, phrases) {
  const phrase = startsWithAny(value, phrases);
  if (!phrase) {
    return "";
  }

  return normalizeText(value.slice(phrase.length).replace(/^[\s:,-]+/, ""));
}

function formatList(items) {
  if (items.length === 1) {
    return items[0];
  }

  return `${items.slice(0, -1).join(", ")} and ${items.at(-1)}`;
}

export class LocalVoiceAgent {
  constructor(options = {}) {
    this.name = options.name || "Nova";
    this.help = options.help || DEFAULT_HELP;
    this.clock = options.clock || (() => new Date());
    this.reminders = [...(options.reminders || [])];
    this.lastResponse = "";
  }

  getSnapshot() {
    return {
      name: this.name,
      reminders: [...this.reminders],
      lastResponse: this.lastResponse
    };
  }

  respond(input) {
    const transcript = normalizeText(input);
    const normalized = transcript.toLowerCase();
    let response;
    let intent = "fallback";

    if (!transcript) {
      response = "I did not catch that. Please try again.";
      intent = "empty";
    } else if (this.isGreeting(normalized)) {
      response = `Hi, I am ${this.name}. ${this.help[0]} Say help for more options.`;
      intent = "greeting";
    } else if (this.isHelpRequest(normalized)) {
      response = `Here is what I can do: ${formatList(this.help)}`;
      intent = "help";
    } else if (this.isRepeatRequest(normalized)) {
      response = this.lastResponse || "I have not said anything yet.";
      intent = "repeat";
    } else if (this.isTimeRequest(normalized)) {
      response = `It is ${this.clock().toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit"
      })}.`;
      intent = "time";
    } else if (this.isDateRequest(normalized)) {
      response = `Today is ${this.clock().toLocaleDateString([], {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric"
      })}.`;
      intent = "date";
    } else if (this.isClearReminderRequest(normalized)) {
      this.reminders = [];
      response = "All reminders are cleared.";
      intent = "clear-reminders";
    } else if (this.isListReminderRequest(normalized)) {
      response = this.reminders.length
        ? `Your reminders are: ${formatList(this.reminders)}.`
        : "You do not have any reminders yet.";
      intent = "list-reminders";
    } else {
      const reminder = this.extractReminder(normalized, transcript);

      if (reminder) {
        this.reminders.push(reminder);
        response = `Reminder saved: ${reminder}.`;
        intent = "set-reminder";
      } else {
        response = [
          "I can handle local voice commands right now.",
          "Try asking for the time, setting a reminder, or saying help."
        ].join(" ");
      }
    }

    this.lastResponse = response;

    return {
      intent,
      input: transcript,
      response,
      reminders: [...this.reminders]
    };
  }

  isGreeting(value) {
    return /^(hello|hi|hey|good morning|good afternoon|good evening)\b/.test(value);
  }

  isHelpRequest(value) {
    return /\b(help|what can you do|commands|options)\b/.test(value);
  }

  isRepeatRequest(value) {
    return /\b(repeat that|say that again|repeat your answer)\b/.test(value);
  }

  isTimeRequest(value) {
    return /\b(what time is it|current time|tell me the time|time now)\b/.test(value);
  }

  isDateRequest(value) {
    return /\b(what day is it|what is the date|today's date|date today|current date)\b/.test(value);
  }

  isListReminderRequest(value) {
    return /\b(list reminders|show reminders|what are my reminders|read reminders)\b/.test(value);
  }

  isClearReminderRequest(value) {
    return /\b(clear reminders|delete reminders|remove reminders|forget reminders)\b/.test(value);
  }

  extractReminder(normalized, original) {
    const command = stripLeadingCommand(normalized, [
      "set a reminder to",
      "set reminder to",
      "remind me to",
      "remember to",
      "add reminder to"
    ]);

    if (!command) {
      return "";
    }

    const originalCommand = original.slice(original.toLowerCase().indexOf(command));
    return normalizeText(originalCommand).replace(/[.?!]+$/, "");
  }
}

export const SUPPORT_MESSAGE =
  "Speech recognition is available in Chrome, Edge, and some Chromium browsers. Speech synthesis is supported by most modern browsers.";
