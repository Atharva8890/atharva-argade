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
    Beat("Let me tell you about a man who heard the word no... more than a thousand times.",
         "title", "pushin", 0.85, 0.6, "fade",
         prompt="Extreme close-up of elderly Colonel Sanders' eyes behind glasses, "
                "white goatee, dramatic chiaroscuro lighting, photoreal, archival"),

    # ----- STORY: THE BEGINNING --------------------------------------------
    Beat("He was sixty-five years old.", "portrait", "pushin", 0.45, 1.1, "light_flash",
         prompt="Dignified portrait of Colonel Harland Sanders in his white suit and "
                "string tie, warm window light, photoreal, archival"),
    Beat("Most folks his age were settling into retirement.", "crowd", "parallax_r", 0.35, 0.7, "dissolve",
         prompt="Older Americans relaxing on a quiet 1950s small-town main street, "
                "golden hour, nostalgic, photoreal documentary"),
    Beat("Harland Sanders was just getting started.", "portrait", "pushin", 0.5, 0.9, "whip_l",
         prompt="Determined Colonel Sanders looking toward the horizon, hopeful "
                "morning light, 1950s, photoreal"),
    Beat("His restaurant had gone under.", "closed", "pushin", 0.6, 0.9, "speed_ramp",
         prompt="A small 1950s American roadside restaurant, empty and closed, "
                "overcast, melancholic, photoreal"),
    Beat("The money was gone.", "money", "pullout", 0.6, 0.8, "whip_r",
         prompt="Empty cash register and a few coins on a worn diner counter, "
                "1950s, dim light, photoreal still life"),
    Beat("And the road ahead was wide open... and terrifying.", "horizon", "parallax_l", 0.55, 1.0, "dissolve",
         prompt="Lone empty American highway stretching into fog at a crossroads, "
                "1950s, uncertain mood, photoreal, cinematic"),
    Beat("Most people would have called it quits.", "crowd", "parallax_l", 0.4, 0.7, "dissolve",
         prompt="Tired men sitting in a 1950s small-town diner booth, "
                "muted colors, photoreal documentary"),
    Beat("Most people would have packed it in.", "horizon", "pushin", 0.45, 0.9, "dissolve",
         prompt="A man's back as he stares down a dead-end road, 1950s, "
                "low contrast, melancholic, photoreal"),
    Beat("But this old man had one thing he believed in.", "portrait", "pushin", 0.7, 1.0, "light_flash",
         prompt="Close-up of Colonel Sanders' resolute face, single key light, "
                "hope in his eyes, photoreal, cinematic"),
    Beat("A recipe. Eleven herbs and spices.", "recipe", "zoom3d", 0.7, 1.3, "speed_ramp",
         prompt="Steam rising from a skillet of golden fried chicken on a 1950s "
                "diner counter, photoreal, macro, warm"),

    # ----- THE JOURNEY ------------------------------------------------------
    Beat("So with almost nothing to his name...", "car", "parallax_r", 0.55, 1.0, "dissolve",
         prompt="A worn 1950s sedan packed with belongings outside a modest house "
                "at dawn, photoreal, cinematic"),
    Beat("He loaded up his car and hit the road, crisscrossing America.",
         "road", "track_left", 0.55, 0.7, "whip_l",
         prompt="A vintage 1950s car driving down an open American highway, vast "
                "landscape, golden hour, photoreal, motion"),
    Beat("And door after door, they turned him down.", "door_closed", "pushin", 0.65, 0.9, "speed_ramp",
         prompt="A restaurant owner closing the door on a hopeful salesman, "
                "1950s diner entrance, photoreal, dramatic"),
    Beat("One no.", "door_closed", "pushin", 0.6, 0.8, "light_flash",
         prompt="A single closed wooden diner door, hard shadow, 1950s, photoreal"),
    Beat("Ten no's.", "doors_many", "parallax_r", 0.68, 0.7, "whip_r",
         prompt="A row of closed restaurant doors down a 1950s main street, "
                "repetition, photoreal, cinematic"),
    Beat("A hundred no's.", "doors_many", "parallax_l", 0.78, 0.7, "whip_l",
         prompt="An endless corridor of closing doors, deep perspective, 1950s "
                "tones, photoreal, dramatic"),
    Beat("Then hundreds more.", "doors_many", "pushin", 0.85, 1.0, "speed_ramp",
         prompt="An overwhelming montage of slamming doors, fast motion blur, "
                "1950s, photoreal, intense"),
    Beat("Every rejection was another reason to give up.", "horizon", "parallax_l", 0.6, 0.9, "dissolve",
         prompt="An exhausted older man resting his head on a car steering wheel "
                "at night, rain on the windshield, photoreal, emotional"),
    Beat("He refused.", "portrait", "pushin", 0.92, 1.3, "light_flash",
         prompt="Defiant close-up of Colonel Sanders, jaw set, dramatic rim light, "
                "photoreal, powerful"),

    # ----- THE MINDSET ------------------------------------------------------
    Beat("Where others saw a dead end...", "horizon", "parallax_l", 0.5, 0.7, "dissolve",
         prompt="A barricaded dead-end road under grey skies, 1950s, photoreal"),
    Beat("He saw a door.", "sunrise", "rise", 0.72, 0.9, "light_flash",
         prompt="Sunrise breaking over an open American road, hopeful light rays, "
                "photoreal, cinematic warm"),
    Beat("Where others quit...", "crowd", "parallax_r", 0.5, 0.7, "dissolve",
         prompt="People standing still in a 1950s town square, muted, photoreal"),
    Beat("He kept driving.", "road", "track_left", 0.72, 0.9, "whip_l",
         prompt="Determined hands firm on the wheel of a 1950s car, open road "
                "ahead, photoreal, motion blur"),
    Beat("Where others complained...", "crowd", "parallax_l", 0.5, 0.7, "dissolve",
         prompt="A group of men grumbling in a 1950s diner booth, photoreal"),
    Beat("He kept believing.", "portrait", "pushin", 0.74, 1.1, "light_flash",
         prompt="Colonel Sanders looking upward with quiet faith, soft halo light, "
                "photoreal, hopeful"),

    # ----- THE GRIND --------------------------------------------------------
    Beat("Years went by.", "time", "zoom3d", 0.55, 1.0, "dissolve",
         prompt="Changing seasons over an American highway, time passing, 1950s, "
                "photoreal, cinematic"),
    Beat("The struggle didn't let up.", "road", "track_right", 0.6, 0.8, "dissolve",
         prompt="A lonely car on an endless highway at dusk, 1950s, photoreal, moody"),
    Beat("But neither did he.", "portrait", "pushin", 0.78, 1.2, "light_flash",
         prompt="Weathered but resolute Colonel Sanders, steady gaze, dramatic "
                "light, photoreal"),

    # ----- THE TURN ---------------------------------------------------------
    Beat("And then one day...", "door_closed", "pushin", 0.7, 1.4, "speed_ramp",
         prompt="A hand reaching toward a door handle, anticipation, a shaft of "
                "light, 1950s, photoreal, cinematic"),
    Beat("Somebody finally said yes.", "handshake", "pushin", 0.9, 1.2, "light_flash",
         prompt="A warm handshake between two men in a 1950s restaurant, deal "
                "sealed, golden light, photoreal, emotional"),
    Beat("And that one yes changed everything.", "sunrise", "rise", 0.85, 1.1, "speed_ramp",
         prompt="A radiant sunrise over a small American town, new beginning, "
                "photoreal, uplifting"),
    Beat("The recipe caught on.", "growth", "zoom3d", 0.75, 0.7, "whip_r",
         prompt="Fried chicken served to delighted 1950s diners, busy restaurant, "
                "warm light, photoreal"),
    Beat("The business took off.", "growth", "pushin", 0.8, 0.7, "whip_l",
         prompt="Rows of bustling 1950s American restaurants with neon signs at "
                "dusk, photoreal, cinematic"),
    Beat("And that little brand spread clear across America.", "map", "zoom3d", 0.85, 1.0, "speed_ramp",
         prompt="A vintage map of the United States lighting up city by city, "
                "1950s aesthetic, photoreal, glowing"),
    Beat("The man nobody wanted...", "portrait", "pushin", 0.78, 1.1, "dissolve",
         prompt="A proud Colonel Sanders in white suit and string tie, iconic "
                "look, warm portrait light, photoreal"),
    Beat("Became one of the most successful entrepreneurs this country has ever seen.",
         "success", "rise", 0.95, 1.4, "light_flash",
         prompt="Iconic Colonel Sanders standing tall, triumphant, golden hour, "
                "photoreal"),

    # ----- THE LESSON -------------------------------------------------------
    Beat("Now, this isn't a story about fried chicken.", "lesson", "pushin", 0.5, 0.9, "dissolve",
         prompt="Clean dark cinematic background with soft volumetric light, "
                "minimal, photoreal"),
    Beat("It's not even about business.", "lesson", "pullout", 0.5, 0.9, "dissolve",
         prompt="Clean dark cinematic background, drifting dust particles, photoreal"),
    Beat("It's about persistence.", "lesson", "pushin", 0.82, 1.3, "light_flash",
         prompt="A single beam of light cutting through darkness onto an open road, "
                "symbolic, photoreal, cinematic"),
    Beat("Success doesn't go to the smartest person in the room.", "lesson", "parallax_r", 0.6, 0.8, "dissolve",
         prompt="Abstract cinematic light rays over a dark backdrop, photoreal"),
    Beat("It doesn't go to the luckiest.", "lesson", "parallax_l", 0.6, 0.8, "dissolve",
         prompt="Abstract cinematic light rays, dust motes, dark backdrop, photoreal"),
    Beat("It goes to the ones who refuse to quit.", "sunrise", "rise", 0.9, 1.4, "speed_ramp",
         prompt="A silhouette of a determined figure walking into a glowing "
                "sunrise, photoreal, triumphant, cinematic"),
    Beat("Because your big break might be just one more shot away.", "sunrise", "pushin", 0.85, 1.2, "light_flash",
         prompt="Dawn light flooding an open horizon, hopeful, photoreal, cinematic"),
    Beat("One more phone call.", "lesson", "pushin", 0.7, 0.7, "whip_l",
         prompt="A vintage 1950s rotary telephone in dramatic light, photoreal"),
    Beat("One more meeting.", "handshake", "pushin", 0.72, 0.7, "whip_r",
         prompt="Two men shaking hands in a doorway of light, photoreal"),
    Beat("One more try.", "sunrise", "rise", 0.8, 1.2, "light_flash",
         prompt="A single figure stepping forward into radiant light, photoreal"),
    Beat("So remember this.", "lesson", "pushin", 0.7, 1.1, "dissolve",
         prompt="Dark cinematic backdrop, a single soft spotlight, photoreal"),
    Beat("The people who change their lives aren't always the most talented.",
         "crowd", "parallax_l", 0.6, 0.8, "dissolve",
         prompt="Ordinary 1950s Americans with hopeful faces, photoreal"),
    Beat("They're the ones who keep going long after everybody else gives up.",
         "road", "track_left", 0.88, 1.4, "speed_ramp",
         prompt="One car driving on while others sit parked at the roadside, "
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
