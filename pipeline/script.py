"""The documentary storyboard.

Each :class:`Beat` is one narration line that becomes roughly one 2-4 second
scene, which keeps the edit constantly moving (a retention requirement).  The
narration timing is measured from the actual synthesized audio, so the visuals
always stay locked to the voice.

Fields
------
text        spoken narration (use "" for a silent beat)
pause       extra dramatic silence held *after* the line (seconds, pre-scaled)
scene       visual archetype key (see ``scenes.py``)
effect      primary camera move for the scene
intensity   0..1 emotional weight -> drives shake, grade, bloom and music
trans       transition used to cut *into* this beat
is_final    render line as a giant centered title card (final screen)
prompt      photoreal image-generation prompt (storyboard sheet + asset names)
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Beat:
    text: str
    scene: str
    effect: str = "pushin"
    intensity: float = 0.4
    pause: float = 0.7
    trans: str = "dissolve"
    is_final: bool = False
    prompt: str = ""

    @property
    def key(self) -> str:
        # Stable identifier used for cached scene art / dropped-in photos.
        return f"{self._index:02d}_{self.scene}"

    _index: int = field(default=0, repr=False)


# Words that get the accent colour + glow treatment wherever they appear.
HIGHLIGHT_WORDS = {
    "rejected", "rejection", "rejections",
    "persistence", "persist", "persisted",
    "success", "successful",
    "quit", "never", "refuse", "refused", "refuses",
    "believe", "believed", "believing", "belief",
    "opportunity", "yes", "breakthrough", "recipe",
    "more", "again", "keep", "going",
}

# The four hero keywords that always render in full caps with maximum glow.
HERO_WORDS = {"REJECTED", "PERSISTENCE", "SUCCESS", "NEVER QUIT"}


_RAW: list[Beat] = [
    # ----- COLD OPEN HOOK (first 3 seconds) ---------------------------------
    Beat("This is the story of a man the world rejected... over a thousand times.",
         "title", "pushin", 0.85, 0.6, "fade",
         prompt="Extreme close-up of a weathered elderly American man's eyes, "
                "1950s, dramatic chiaroscuro lighting, photoreal, film grain"),

    # ----- STORY: THE BEGINNING --------------------------------------------
    Beat("At sixty-five years old...", "portrait", "pushin", 0.45, 1.1, "light_flash",
         prompt="Portrait of a dignified 65 year old American man in a white suit, "
                "1950s small town, warm window light, photoreal, Kodachrome"),
    Beat("Most people were preparing for retirement.", "crowd", "parallax_r", 0.35, 0.7, "dissolve",
         prompt="Elderly Americans relaxing on porches in a 1950s small town, "
                "golden hour, nostalgic, photoreal documentary"),
    Beat("Harland Sanders was preparing for a new beginning.", "portrait", "pushin", 0.5, 0.9, "whip_l",
         prompt="Determined elderly man buttoning his jacket, looking toward horizon, "
                "1950s, hopeful morning light, photoreal"),
    Beat("His restaurant failed.", "closed", "pushin", 0.6, 0.9, "speed_ramp",
         prompt="A small 1950s American roadside restaurant, closed sign on door, "
                "empty, overcast, melancholic, photoreal"),
    Beat("His income disappeared.", "money", "pullout", 0.6, 0.8, "whip_r",
         prompt="Empty cash register and a few coins on a wooden counter, "
                "1950s diner, dim light, photoreal still life"),
    Beat("His future looked uncertain.", "horizon", "parallax_l", 0.55, 1.0, "dissolve",
         prompt="Lone elderly man silhouette at a foggy crossroads, empty highway, "
                "1950s, uncertain mood, photoreal, cinematic"),
    Beat("Most people would have accepted defeat.", "crowd", "parallax_l", 0.4, 0.7, "dissolve",
         prompt="Tired men sitting defeated in a 1950s small town bar, "
                "muted colors, photoreal documentary"),
    Beat("Most people would have stopped trying.", "horizon", "pushin", 0.45, 0.9, "dissolve",
         prompt="A man's back as he stares at a dead-end road, 1950s, "
                "low contrast, melancholic, photoreal"),
    Beat("But Sanders believed in one thing.", "portrait", "pushin", 0.7, 1.0, "light_flash",
         prompt="Close-up of resolute elderly man's face, single key light, "
                "1950s, hope in his eyes, photoreal, cinematic"),
    Beat("His recipe.", "recipe", "zoom3d", 0.7, 1.3, "speed_ramp",
         prompt="Steam rising from a cast iron skillet of fried chicken, "
                "eleven herbs and spices on a table, 1950s kitchen, photoreal, macro"),

    # ----- THE JOURNEY ------------------------------------------------------
    Beat("With almost nothing left...", "car", "parallax_r", 0.55, 1.0, "dissolve",
         prompt="Worn 1950s sedan packed with belongings, parked outside a modest "
                "house at dawn, photoreal, cinematic"),
    Beat("He packed his belongings into a car and started driving across America.",
         "road", "track_left", 0.55, 0.7, "whip_l",
         prompt="Vintage 1950s car driving down an open American highway, "
                "vast landscape, golden hour, photoreal, motion"),
    Beat("Restaurant after restaurant rejected him.", "door_closed", "pushin", 0.65, 0.9, "speed_ramp",
         prompt="A restaurant owner closing a door on a hopeful salesman, "
                "1950s diner entrance, photoreal, dramatic"),
    Beat("One rejection.", "door_closed", "pushin", 0.6, 0.8, "light_flash",
         prompt="A single closed wooden door, 'No' implied, 1950s, hard shadow, photoreal"),
    Beat("Ten rejections.", "doors_many", "parallax_r", 0.68, 0.7, "whip_r",
         prompt="A row of closed restaurant doors down a 1950s main street, "
                "repetition, photoreal, cinematic"),
    Beat("One hundred rejections.", "doors_many", "parallax_l", 0.78, 0.7, "whip_l",
         prompt="Endless corridor of closing doors, surreal depth, 1950s tones, "
                "photoreal, dramatic perspective"),
    Beat("Then hundreds more.", "doors_many", "pushin", 0.85, 1.0, "speed_ramp",
         prompt="Overwhelming montage of slamming doors, fast motion blur, "
                "1950s, photoreal, intense"),
    Beat("Every rejection gave him another reason to quit.", "horizon", "parallax_l", 0.6, 0.9, "dissolve",
         prompt="Exhausted elderly man resting head on car steering wheel at night, "
                "1950s, rain on windshield, photoreal, emotional"),
    Beat("But he refused.", "portrait", "pushin", 0.92, 1.3, "light_flash",
         prompt="Defiant close-up of the elderly man's determined face, jaw set, "
                "1950s, dramatic rim light, photoreal, powerful"),

    # ----- THE MINDSET ------------------------------------------------------
    Beat("While others saw failure...", "crowd", "parallax_l", 0.5, 0.7, "dissolve",
         prompt="Discouraged businessmen in 1950s office, grey tones, photoreal"),
    Beat("He saw opportunity.", "sunrise", "rise", 0.72, 0.9, "light_flash",
         prompt="Sunrise breaking over an open American road, hopeful light rays, "
                "1950s, photoreal, cinematic warm"),
    Beat("While others stopped...", "crowd", "parallax_r", 0.5, 0.7, "dissolve",
         prompt="People standing still in a 1950s town square, muted, photoreal"),
    Beat("He kept moving.", "road", "track_left", 0.72, 0.9, "whip_l",
         prompt="Determined man driving forward, hands firm on wheel, 1950s car, "
                "photoreal, motion blur"),
    Beat("While others complained...", "crowd", "parallax_l", 0.5, 0.7, "dissolve",
         prompt="Group of men arguing and grumbling in a 1950s diner booth, photoreal"),
    Beat("He kept believing.", "portrait", "pushin", 0.74, 1.1, "light_flash",
         prompt="Elderly man looking upward with quiet faith, soft halo light, "
                "1950s, photoreal, hopeful"),

    # ----- THE GRIND --------------------------------------------------------
    Beat("Years passed.", "time", "zoom3d", 0.55, 1.0, "dissolve",
         prompt="Time-lapse feel: changing seasons over an American highway, "
                "calendar pages, 1950s, photoreal, cinematic"),
    Beat("The struggle continued.", "road", "track_right", 0.6, 0.8, "dissolve",
         prompt="Lonely car on an endless highway at dusk, 1950s, photoreal, moody"),
    Beat("The uncertainty remained.", "horizon", "parallax_r", 0.58, 0.9, "dissolve",
         prompt="Foggy morning road stretching into the unknown, 1950s, photoreal"),
    Beat("But Sanders stayed committed.", "portrait", "pushin", 0.78, 1.2, "light_flash",
         prompt="Weathered but resolute elderly man, steady gaze, 1950s, "
                "dramatic light, photoreal"),

    # ----- THE TURN ---------------------------------------------------------
    Beat("Then one day...", "door_closed", "pushin", 0.7, 1.4, "speed_ramp",
         prompt="Hand reaching toward a door handle, anticipation, 1950s, "
                "shaft of light, photoreal, cinematic"),
    Beat("Someone finally said yes.", "handshake", "pushin", 0.9, 1.2, "light_flash",
         prompt="Warm handshake between two men in a 1950s restaurant, deal sealed, "
                "smiling, golden light, photoreal, emotional"),
    Beat("That single opportunity changed everything.", "sunrise", "rise", 0.85, 1.1, "speed_ramp",
         prompt="Radiant sunrise over a small American town, new beginning, "
                "1950s, photoreal, uplifting"),
    Beat("The recipe spread.", "growth", "zoom3d", 0.75, 0.7, "whip_r",
         prompt="Fried chicken being served to delighted 1950s diners, busy "
                "restaurant, warm light, photoreal"),
    Beat("The business grew.", "growth", "pushin", 0.8, 0.7, "whip_l",
         prompt="Rows of bustling 1950s American restaurants with neon signs at dusk, "
                "photoreal, cinematic"),
    Beat("The brand expanded across America.", "map", "zoom3d", 0.85, 1.0, "speed_ramp",
         prompt="Vintage map of the United States lighting up city by city, "
                "1950s aesthetic, photoreal, glowing"),
    Beat("And the man who was rejected again and again...", "portrait", "pushin", 0.78, 1.1, "dissolve",
         prompt="Proud elderly man in white suit and string tie, iconic look, "
                "1950s, warm portrait light, photoreal"),
    Beat("Became one of the most successful entrepreneurs in history.",
         "success", "rise", 0.95, 1.4, "light_flash",
         prompt="Iconic elderly entrepreneur standing tall before his thriving "
                "restaurant empire, triumphant, golden hour, 1950s, photoreal"),

    # ----- THE LESSON -------------------------------------------------------
    Beat("The lesson isn't about chicken.", "lesson", "pushin", 0.5, 0.9, "dissolve",
         prompt="Clean dark cinematic background with soft volumetric light, "
                "minimal, photoreal"),
    Beat("The lesson isn't about business.", "lesson", "pullout", 0.5, 0.9, "dissolve",
         prompt="Clean dark cinematic background, drifting dust particles, photoreal"),
    Beat("The lesson is about persistence.", "lesson", "pushin", 0.82, 1.3, "light_flash",
         prompt="Single beam of light cutting through darkness onto an open road, "
                "symbolic, photoreal, cinematic"),
    Beat("Success does not belong to the smartest.", "lesson", "parallax_r", 0.6, 0.8, "dissolve",
         prompt="Abstract cinematic light rays over dark backdrop, photoreal"),
    Beat("Success does not belong to the luckiest.", "lesson", "parallax_l", 0.6, 0.8, "dissolve",
         prompt="Abstract cinematic light rays, dust motes, dark backdrop, photoreal"),
    Beat("Success belongs to the people who refuse to quit.", "sunrise", "rise", 0.9, 1.4, "speed_ramp",
         prompt="Silhouette of a determined figure walking into a glowing sunrise, "
                "photoreal, triumphant, cinematic"),
    Beat("Because your breakthrough may be one more attempt away.", "sunrise", "pushin", 0.85, 1.2, "light_flash",
         prompt="Dawn light flooding an open horizon, hopeful, photoreal, cinematic"),
    Beat("One more phone call.", "lesson", "pushin", 0.7, 0.7, "whip_l",
         prompt="A vintage 1950s rotary telephone in dramatic light, photoreal"),
    Beat("One more meeting.", "handshake", "pushin", 0.72, 0.7, "whip_r",
         prompt="Two silhouettes shaking hands in a doorway of light, photoreal"),
    Beat("One more try.", "sunrise", "rise", 0.8, 1.2, "light_flash",
         prompt="A single figure stepping forward into radiant light, photoreal"),
    Beat("Remember this.", "lesson", "pushin", 0.7, 1.1, "dissolve",
         prompt="Dark cinematic backdrop, single soft spotlight, photoreal"),
    Beat("The people who change their lives are not always the most talented.",
         "crowd", "parallax_l", 0.6, 0.8, "dissolve",
         prompt="Ordinary 1950s Americans of all kinds, hopeful faces, photoreal"),
    Beat("They are the people who keep going when everyone else stops.",
         "road", "track_left", 0.88, 1.4, "speed_ramp",
         prompt="One car driving on while others are parked at the roadside, "
                "1950s, sunrise, photoreal, symbolic"),

    # ----- FINAL SCREEN -----------------------------------------------------
    Beat("Success belongs to those who refuse to quit.", "final", "pushin", 0.95, 1.2, "light_flash",
         is_final=True,
         prompt="Epic golden sunrise over America, cinematic, photoreal"),
    Beat("One more try.", "final", "pushin", 0.9, 1.0, "dissolve", is_final=True,
         prompt="Glowing horizon, particles, cinematic, photoreal"),
    Beat("One more step.", "final", "pushin", 0.9, 1.0, "dissolve", is_final=True,
         prompt="Glowing horizon, particles, cinematic, photoreal"),
    Beat("Never quit.", "final", "pushin", 1.0, 2.2, "light_flash", is_final=True,
         prompt="Blinding triumphant light, cinematic, photoreal"),
]


def storyboard() -> list[Beat]:
    """Return the storyboard with stable per-beat indices assigned."""
    for i, b in enumerate(_RAW):
        b._index = i
    return _RAW
