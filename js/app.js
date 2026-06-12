/* VaaniBridge — speak in your language, the other side hears professional English. */

(() => {
  "use strict";

  // ---------- Elements ----------
  const micBtn = document.getElementById("micBtn");
  const micRings = document.getElementById("micRings");
  const statusText = document.getElementById("statusText");
  const interimText = document.getElementById("interimText");
  const conversation = document.getElementById("conversation");
  const emptyState = document.getElementById("emptyState");
  const sourceLang = document.getElementById("sourceLang");
  const voiceSelect = document.getElementById("voiceSelect");
  const settingsBtn = document.getElementById("settingsBtn");
  const closeSettings = document.getElementById("closeSettings");
  const settingsPanel = document.getElementById("settingsPanel");
  const overlay = document.getElementById("overlay");
  const autoSpeak = document.getElementById("autoSpeak");
  const speechRate = document.getElementById("speechRate");
  const rateValue = document.getElementById("rateValue");
  const apiKeyInput = document.getElementById("apiKey");
  const toneSelect = document.getElementById("toneSelect");

  // ---------- State ----------
  let recognition = null;
  let listening = false;
  let englishVoices = [];

  const LANG_NAMES = {
    "mr-IN": "Marathi", "hi-IN": "Hindi", "gu-IN": "Gujarati",
    "ta-IN": "Tamil", "te-IN": "Telugu", "kn-IN": "Kannada",
    "bn-IN": "Bengali", "pa-IN": "Punjabi", "ml-IN": "Malayalam", "ur-IN": "Urdu",
  };

  const TONE_PROMPTS = {
    professional: "clear, confident, professional business English suitable for a work call",
    formal: "polite, formal English suitable for an official conversation",
    friendly: "natural, friendly conversational English",
  };

  // ---------- Settings persistence ----------
  const store = {
    get(key, fallback) {
      const v = localStorage.getItem("vaanibridge:" + key);
      return v === null ? fallback : v;
    },
    set(key, value) {
      localStorage.setItem("vaanibridge:" + key, value);
    },
  };

  function loadSettings() {
    sourceLang.value = store.get("sourceLang", "mr-IN");
    autoSpeak.checked = store.get("autoSpeak", "1") === "1";
    speechRate.value = store.get("speechRate", "1.0");
    rateValue.textContent = parseFloat(speechRate.value).toFixed(1);
    apiKeyInput.value = store.get("apiKey", "");
    toneSelect.value = store.get("tone", "professional");
  }

  sourceLang.addEventListener("change", () => {
    store.set("sourceLang", sourceLang.value);
    if (listening) restartRecognition();
  });
  autoSpeak.addEventListener("change", () => store.set("autoSpeak", autoSpeak.checked ? "1" : "0"));
  speechRate.addEventListener("input", () => {
    rateValue.textContent = parseFloat(speechRate.value).toFixed(1);
    store.set("speechRate", speechRate.value);
  });
  apiKeyInput.addEventListener("change", () => store.set("apiKey", apiKeyInput.value.trim()));
  toneSelect.addEventListener("change", () => store.set("tone", toneSelect.value));
  voiceSelect.addEventListener("change", () => store.set("voice", voiceSelect.value));

  // ---------- Settings panel ----------
  function openPanel() {
    settingsPanel.classList.add("open");
    overlay.classList.add("open");
  }
  function closePanel() {
    settingsPanel.classList.remove("open");
    overlay.classList.remove("open");
  }
  settingsBtn.addEventListener("click", openPanel);
  closeSettings.addEventListener("click", closePanel);
  overlay.addEventListener("click", closePanel);

  // ---------- Voices (English TTS) ----------
  function populateVoices() {
    englishVoices = speechSynthesis.getVoices().filter((v) => v.lang.startsWith("en"));
    const saved = store.get("voice", "");
    voiceSelect.innerHTML = '<option value="">Professional English (auto voice)</option>';
    for (const v of englishVoices) {
      const opt = document.createElement("option");
      opt.value = v.name;
      opt.textContent = `${v.name} (${v.lang})`;
      if (v.name === saved) opt.selected = true;
      voiceSelect.appendChild(opt);
    }
  }
  populateVoices();
  if (typeof speechSynthesis !== "undefined") {
    speechSynthesis.onvoiceschanged = populateVoices;
  }

  function pickVoice() {
    const selected = englishVoices.find((v) => v.name === voiceSelect.value);
    if (selected) return selected;
    // Prefer Indian English, then US/UK English.
    return (
      englishVoices.find((v) => v.lang === "en-IN") ||
      englishVoices.find((v) => v.lang === "en-US") ||
      englishVoices.find((v) => v.lang === "en-GB") ||
      englishVoices[0] ||
      null
    );
  }

  function speakEnglish(text, replayBtn) {
    if (!("speechSynthesis" in window)) return;
    speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    const voice = pickVoice();
    if (voice) utter.voice = voice;
    utter.lang = voice ? voice.lang : "en-US";
    utter.rate = parseFloat(speechRate.value) || 1.0;
    if (replayBtn) {
      replayBtn.classList.add("speaking");
      utter.onend = () => replayBtn.classList.remove("speaking");
      utter.onerror = () => replayBtn.classList.remove("speaking");
    }
    speechSynthesis.speak(utter);
  }

  // ---------- Translation ----------
  async function polishWithOpenAI(text, fromLangName, apiKey) {
    const tone = TONE_PROMPTS[toneSelect.value] || TONE_PROMPTS.professional;
    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.3,
        messages: [
          {
            role: "system",
            content:
              `You are a real-time interpreter on a phone call. The user speaks ${fromLangName}. ` +
              `Translate what they say into ${tone}. ` +
              `Keep the meaning exact, fix grammar, and make it sound natural — as if a fluent professional said it. ` +
              `Reply with ONLY the English sentence, nothing else.`,
          },
          { role: "user", content: text },
        ],
      }),
    });
    if (!res.ok) throw new Error(`OpenAI API error (${res.status})`);
    const data = await res.json();
    const out = data.choices?.[0]?.message?.content?.trim();
    if (!out) throw new Error("Empty response from OpenAI");
    return out;
  }

  async function translateWithGoogle(text, fromCode) {
    const sl = fromCode.split("-")[0];
    const url =
      "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" +
      encodeURIComponent(sl) +
      "&tl=en&dt=t&q=" +
      encodeURIComponent(text);
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Translate error (${res.status})`);
    const data = await res.json();
    const out = (data[0] || []).map((seg) => seg[0]).join(" ").trim();
    if (!out) throw new Error("Empty translation");
    return out;
  }

  async function translateWithMyMemory(text, fromCode) {
    const sl = fromCode.split("-")[0];
    const url =
      "https://api.mymemory.translated.net/get?q=" +
      encodeURIComponent(text) +
      `&langpair=${sl}|en`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Translate error (${res.status})`);
    const data = await res.json();
    const out = data.responseData?.translatedText?.trim();
    if (!out) throw new Error("Empty translation");
    return out;
  }

  async function translate(text, fromCode) {
    const apiKey = apiKeyInput.value.trim();
    const fromLangName = LANG_NAMES[fromCode] || "an Indian language";
    if (apiKey) {
      try {
        return await polishWithOpenAI(text, fromLangName, apiKey);
      } catch (err) {
        console.warn("OpenAI failed, falling back to free translation:", err);
      }
    }
    try {
      return await translateWithGoogle(text, fromCode);
    } catch (err) {
      console.warn("Google endpoint failed, trying MyMemory:", err);
      return await translateWithMyMemory(text, fromCode);
    }
  }

  // ---------- Conversation UI ----------
  function addExchange(originalText, fromCode) {
    if (emptyState) emptyState.style.display = "none";

    const card = document.createElement("div");
    card.className = "exchange";
    card.innerHTML = `
      <div class="original">
        <span class="tag">${LANG_NAMES[fromCode] || "You"}</span>
        <div class="original-text"></div>
      </div>
      <div class="english pending">
        <div>
          <span class="tag">English</span>
          <div class="english-text">Translating…</div>
        </div>
      </div>
    `;
    card.querySelector(".original-text").textContent = originalText;
    conversation.prepend(card);
    return card;
  }

  function fillExchange(card, englishTextValue) {
    const englishBox = card.querySelector(".english");
    englishBox.classList.remove("pending");
    card.querySelector(".english-text").textContent = englishTextValue;

    const replayBtn = document.createElement("button");
    replayBtn.className = "replay-btn";
    replayBtn.title = "पुन्हा ऐकवा / Speak again";
    replayBtn.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>' +
      '<path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>';
    replayBtn.addEventListener("click", () => speakEnglish(englishTextValue, replayBtn));
    englishBox.appendChild(replayBtn);
    return replayBtn;
  }

  function failExchange(card, message) {
    const englishBox = card.querySelector(".english");
    englishBox.classList.remove("pending");
    englishBox.classList.add("error-text");
    card.querySelector(".english-text").textContent = message;
  }

  async function handleFinalTranscript(text) {
    const cleaned = text.trim();
    if (!cleaned) return;
    const fromCode = sourceLang.value;
    const card = addExchange(cleaned, fromCode);
    try {
      const english = await translate(cleaned, fromCode);
      const replayBtn = fillExchange(card, english);
      if (autoSpeak.checked) speakEnglish(english, replayBtn);
    } catch (err) {
      console.error(err);
      failExchange(card, "भाषांतर अयशस्वी — इंटरनेट तपासा / Translation failed, check your connection.");
    }
  }

  // ---------- Speech recognition ----------
  const SpeechRecognitionImpl =
    window.SpeechRecognition || window.webkitSpeechRecognition || null;

  function setStatus(text) {
    statusText.textContent = text;
  }

  function buildRecognition() {
    const rec = new SpeechRecognitionImpl();
    rec.lang = sourceLang.value;
    rec.continuous = true;
    rec.interimResults = true;

    rec.onresult = (event) => {
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          handleFinalTranscript(result[0].transcript);
        } else {
          interim += result[0].transcript;
        }
      }
      interimText.textContent = interim;
    };

    rec.onerror = (event) => {
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        stopListening();
        setStatus("⚠️ Mic ची परवानगी द्या (browser मध्ये Allow करा)");
      } else if (event.error === "no-speech") {
        // Ignore; onend will restart while listening.
      } else {
        console.warn("Speech recognition error:", event.error);
      }
    };

    rec.onend = () => {
      interimText.textContent = "";
      // Chrome stops recognition after silence; keep it alive while toggled on.
      if (listening) {
        try { rec.start(); } catch (_) { /* already started */ }
      }
    };

    return rec;
  }

  function startListening() {
    if (!SpeechRecognitionImpl) return;
    recognition = buildRecognition();
    try {
      recognition.start();
      listening = true;
      micRings.classList.add("listening");
      setStatus("👂 ऐकतोय… बोला! (थांबवण्यासाठी पुन्हा दाबा)");
    } catch (err) {
      console.error(err);
      setStatus("⚠️ Mic सुरू करता आला नाही");
    }
  }

  function stopListening() {
    listening = false;
    micRings.classList.remove("listening");
    interimText.textContent = "";
    if (recognition) {
      recognition.onend = null;
      try { recognition.stop(); } catch (_) { /* noop */ }
      recognition = null;
    }
    setStatus("🎙️ बटण दाबा आणि मराठीत बोला");
  }

  function restartRecognition() {
    stopListening();
    startListening();
  }

  micBtn.addEventListener("click", () => {
    if (listening) stopListening();
    else startListening();
  });

  // ---------- Init ----------
  loadSettings();

  if (!SpeechRecognitionImpl) {
    micBtn.disabled = true;
    micBtn.style.opacity = "0.5";
    setStatus("⚠️ हा browser speech recognition ला support करत नाही. कृपया Chrome किंवा Edge वापरा.");
  }
})();
