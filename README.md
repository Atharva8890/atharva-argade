# VaaniBridge 🎙️→🇬🇧

**बोला तुमच्या भाषेत — समोरच्याला ऐकू येईल professional English मध्ये.**

Speak in Marathi (or Hindi, Gujarati, Tamil, and more) and VaaniBridge instantly translates your words into clear, professional English and **speaks them out loud** — so the person on the other side of your call hears fluent English.

## हे app काय करतं? / What it does

1. 🎤 तुम्ही mic बटण दाबून **मराठीत बोलता**
2. 🔁 App तुमचं बोलणं ओळखून ते **professional English मध्ये भाषांतर** करतं
3. 🔊 App ते English वाक्य **मोठ्याने बोलून दाखवतं** — call वरच्या समोरच्या व्यक्तीला ते ऐकू जातं

## कसं चालवायचं? / How to run

कोणताही build/install लागत नाही. फक्त एक local server सुरू करा:

```bash
# Option 1: Python
python3 -m http.server 8000

# Option 2: Node.js
npx serve .
```

मग **Chrome किंवा Edge** मध्ये उघडा: `http://localhost:8000`

> ⚠️ Speech recognition साठी Chrome/Edge browser आवश्यक आहे (Web Speech API). Mic ची परवानगी विचारल्यावर **Allow** करा.

## Call वर कसं वापरायचं? / Using it on a call

1. तुमचा call **speakerphone** वर ठेवा, किंवा हा app दुसऱ्या device/laptop वर उघडा
2. Mic बटण दाबा आणि मराठीत बोला
3. App तुमचं वाक्य English मध्ये बोलेल — तो आवाज call च्या mic मधून समोरच्या व्यक्तीपर्यंत पोहोचेल

## Features

- 🗣️ **10 भारतीय भाषा** — मराठी, हिंदी, गुजराती, तमिळ, तेलुगू, कन्नड, बंगाली, पंजाबी, मल्याळम, उर्दू
- 🤖 **Optional OpenAI integration** — settings मध्ये API key टाकल्यास भाषांतर अधिक polished आणि professional होतं (key फक्त तुमच्या browser च्या localStorage मध्ये राहते)
- 🎚️ **Tone निवडा** — Professional / Formal / Friendly
- 🔊 **Voice आणि speed निवडा** — Indian English voice ला प्राधान्य
- 📜 **Conversation history** — प्रत्येक वाक्य पुन्हा ऐकवण्यासाठी replay बटण
- 📱 **Mobile-friendly** responsive design

## Tech

Plain HTML + CSS + JavaScript — no frameworks, no build step.

| गोष्ट | तंत्रज्ञान |
|---|---|
| Speech-to-text (मराठी ओळखणं) | Web Speech API (`SpeechRecognition`) |
| भाषांतर | Google Translate endpoint (free) → MyMemory fallback → optional OpenAI polish |
| Text-to-speech (English बोलणं) | Web Speech API (`speechSynthesis`) |

## मर्यादा / Limitations

- हे app फोन call च्या audio मध्ये थेट घुसून आवाज बदलू शकत नाही (operating systems हे security साठी allow करत नाहीत). म्हणून speakerphone पद्धत वापरावी लागते.
- Speech recognition ला internet लागतं (Chrome चं recognition cloud-based आहे).
- भाषांतराची गुणवत्ता free API वर अवलंबून आहे; OpenAI key दिल्यास खूप चांगला निकाल मिळतो.
