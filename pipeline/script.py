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
    "quit", "never", "refuse", "refused", "refuses", "refusing",
    "believe", "believed", "believing", "belief",
    "opportunity", "yes", "no", "nos", "breakthrough", "recipe",
    "more", "again", "keep", "going", "broke", "chance",
}

# The four hero keywords that always render in full caps with maximum glow.
HERO_WORDS = {"REJECTED", "PERSISTENCE", "SUCCESS", "NEVER QUIT"}


_RAW: list[Beat] = [
    # ===== ACT 1 — THE SUSPENSEFUL HOOK ====================================
    Beat("Picture a man.", "title", "pushin", 0.6, 1.1, "fade",
         prompt="Extreme close-up of an elderly man's eyes behind glasses in "
                "shadow, mysterious, dramatic chiaroscuro, photoreal, archival"),
    Beat("Sixty-five years old.", "portrait", "pushin", 0.6, 0.9, "light_flash",
         prompt="Silhouetted elderly man, face half in shadow, 1950s, photoreal"),
    Beat("Flat broke.", "money", "pushin", 0.7, 0.9, "speed_ramp",
         prompt="A few coins and a worn wallet on an empty table, dim light, "
                "photoreal still life"),
    Beat("Living on a single Social Security check.", "money", "pullout", 0.65, 0.9, "whip_r",
         prompt="A government check on a kitchen table in a humble 1950s home, "
                "photoreal, melancholic"),
    Beat("Driving a beat-up car across America...", "car", "track_left", 0.6, 0.8, "dissolve",
         prompt="An old 1950s sedan on a lonely highway at dawn, photoreal"),
    Beat("Sleeping in the back seat...", "car", "parallax_r", 0.6, 1.0, "dissolve",
         prompt="A man sleeping in the back seat of a 1950s car at night, "
                "streetlight glow, photoreal, intimate"),
    Beat("Knocking on door after door...", "door_closed", "pushin", 0.7, 0.8, "speed_ramp",
         prompt="A weathered hand knocking on a diner door, 1950s, photoreal"),
    Beat("And hearing the same word every single time. No.", "door_closed", "pushin", 0.9, 1.3, "light_flash",
         prompt="A door closing in the viewer's face, hard shadow, 1950s, photoreal, dramatic"),
    Beat("By some accounts, he heard it more than a thousand times.",
         "doors_many", "zoom3d", 0.85, 1.2, "dissolve",
         prompt="An endless corridor of closing doors, deep perspective, photoreal, intense"),
    Beat("Most men would have quit a lifetime ago.", "crowd", "parallax_l", 0.55, 0.9, "dissolve",
         prompt="Defeated men in a dim 1950s bar, muted tones, photoreal"),
    Beat("But this man was only just getting started.", "portrait", "pushin", 0.8, 1.1, "light_flash",
         prompt="Determined elderly man lifting his gaze toward the light, photoreal"),
    Beat("And what he was about to build...", "map", "zoom3d", 0.7, 0.9, "speed_ramp",
         prompt="A glowing vintage map of America, lights beginning to appear, photoreal"),
    Beat("you would recognize anywhere in the world.", "success", "rise", 0.85, 1.2, "light_flash",
         prompt="Bright neon restaurant signs glowing at dusk, iconic, photoreal"),
    Beat("This is the story of Colonel Harland Sanders.", "title", "pushin", 0.9, 1.6, "light_flash",
         prompt="Iconic Colonel Sanders in white suit and string tie, warm key "
                "light, dignified, photoreal, archival"),

    # ===== ACT 2 — HUMBLE, HARD BEGINNINGS =================================
    Beat("He was born in 1890, in a small Indiana town.", "portrait", "parallax_r", 0.45, 0.9, "dissolve",
         prompt="A young man's vintage sepia portrait, early 1900s, photoreal, archival"),
    Beat("When he was just five years old, his father died.", "portrait", "pushin", 0.7, 1.1, "whip_l",
         prompt="A somber young boy in early 1900s clothing, soft window light, photoreal"),
    Beat("His mother went to work to keep food on the table.", "crowd", "parallax_l", 0.5, 0.8, "dissolve",
         prompt="A hardworking woman in an early 1900s kitchen, warm light, photoreal"),
    Beat("And little Harland was left to cook for his brother and sister.",
         "recipe", "pushin", 0.55, 0.9, "dissolve",
         prompt="A child's hands cooking at an old wood stove, early 1900s kitchen, photoreal"),
    Beat("By the age of seven, he could cook a full meal.", "recipe", "zoom3d", 0.55, 0.9, "whip_r",
         prompt="A simple home-cooked meal on a rustic table, warm light, photoreal"),
    Beat("By thirteen, he left home to make his own way.", "road", "track_left", 0.6, 1.0, "speed_ramp",
         prompt="A young boy walking down a dirt country road with a small bag, "
                "dawn, photoreal, cinematic"),
    Beat("And for the next forty years...", "time", "zoom3d", 0.6, 0.9, "dissolve",
         prompt="Changing seasons and passing years over rural America, photoreal"),
    Beat("life knocked him down again... and again... and again.",
         "horizon", "pushin", 0.7, 1.2, "light_flash",
         prompt="A lone figure walking into a hard wind on an empty road, photoreal, moody"),

    # ===== ACT 3 — A LIFE OF FAILURE =======================================
    Beat("He worked as a farmhand.", "crowd", "parallax_r", 0.4, 0.7, "whip_l",
         prompt="A man working a field on an early American farm, photoreal"),
    Beat("A streetcar conductor.", "crowd", "parallax_l", 0.4, 0.7, "whip_r",
         prompt="A vintage streetcar on a city street, early 1900s, photoreal"),
    Beat("A railroad fireman.", "road", "track_right", 0.45, 0.7, "speed_ramp",
         prompt="A steam locomotive and railway, vintage, photoreal, dramatic"),
    Beat("He sold insurance. He sold tires.", "crowd", "pushin", 0.45, 0.8, "dissolve",
         prompt="A door-to-door salesman with a case, 1920s street, photoreal"),
    Beat("He ran a ferry boat. He even studied law...", "horizon", "parallax_l", 0.5, 0.9, "dissolve",
         prompt="A small ferry crossing a wide river, vintage, photoreal"),
    Beat("until a courtroom fight ended that dream, too.", "closed", "pushin", 0.6, 1.0, "light_flash",
         prompt="An empty vintage courtroom in dramatic light, photoreal"),
    Beat("He lost job after job.", "closed", "parallax_r", 0.6, 0.7, "whip_r",
         prompt="A 'closed' sign hanging in a dusty window, photoreal"),
    Beat("Business after business.", "closed", "pushin", 0.65, 0.9, "speed_ramp",
         prompt="A shuttered storefront on a quiet street, photoreal, melancholic"),
    Beat("By the age when most men think about slowing down...", "horizon", "parallax_l", 0.55, 1.0, "dissolve",
         prompt="An older man's silhouette at a crossroads at dusk, photoreal"),
    Beat("Harland Sanders had almost nothing to show for it.", "portrait", "pushin", 0.7, 1.2, "light_flash",
         prompt="A weary but dignified older man's face, soft shadow, photoreal"),

    # ===== ACT 4 — THE SPARK ==============================================
    Beat("But in a little gas station in Corbin, Kentucky...", "recipe", "parallax_r", 0.55, 0.9, "dissolve",
         prompt="A 1930s roadside gas station with a small cafe, photoreal, warm"),
    Beat("he started cooking for hungry travelers.", "recipe", "pushin", 0.6, 0.8, "whip_l",
         prompt="A cook serving plates at a busy roadside counter, 1930s, photoreal"),
    Beat("Fried chicken. Country ham. Fresh biscuits.", "recipe", "zoom3d", 0.65, 0.9, "speed_ramp",
         prompt="A spread of fried chicken, ham and biscuits on a diner table, photoreal, warm"),
    Beat("And people drove for miles just to taste it.", "crowd", "parallax_l", 0.6, 0.9, "whip_r",
         prompt="Cars lined up outside a busy roadside diner, 1940s, photoreal"),
    Beat("He perfected a secret recipe...", "recipe", "pushin", 0.7, 1.0, "light_flash",
         prompt="Hands blending herbs and spices on a wooden table, macro, photoreal"),
    Beat("eleven herbs and spices.", "recipe", "zoom3d", 0.75, 1.1, "dissolve",
         prompt="Steam rising from golden fried chicken, close-up, photoreal, warm"),
    Beat("He found a faster way to cook it.", "recipe", "pushin", 0.6, 0.8, "whip_l",
         prompt="A vintage pressure cooker in a busy 1940s kitchen, photoreal"),
    Beat("And for the first time in his life... things were working.", "growth", "rise", 0.78, 1.1, "light_flash",
         prompt="A warm, full restaurant with happy customers, 1940s, photoreal"),
    Beat("The state even made him a Kentucky Colonel.", "portrait", "pushin", 0.7, 1.0, "dissolve",
         prompt="A proud man receiving an honor, warm portrait light, photoreal"),
    Beat("Finally, after all those years... he had built something.", "success", "rise", 0.82, 1.3, "light_flash",
         prompt="A thriving roadside restaurant at golden hour, photoreal, hopeful"),

    # ===== ACT 5 — ROCK BOTTOM AT 65 ======================================
    Beat("And then...", "horizon", "pushin", 0.7, 1.3, "speed_ramp",
         prompt="Dark storm clouds rolling over an open highway, photoreal, ominous"),
    Beat("they built a brand-new highway.", "road", "track_left", 0.6, 0.8, "dissolve",
         prompt="A new interstate highway under construction, 1950s, photoreal"),
    Beat("And it ran right past his door.", "road", "parallax_r", 0.7, 1.0, "whip_r",
         prompt="An empty old road bypassed by a distant new highway, photoreal, lonely"),
    Beat("The customers vanished.", "closed", "pushin", 0.7, 0.9, "speed_ramp",
         prompt="An empty diner with stacked chairs, dim light, photoreal, melancholic"),
    Beat("The restaurant he loved... was finished.", "closed", "pushin", 0.78, 1.2, "light_flash",
         prompt="A 'closed' sign on a darkened restaurant door, photoreal, somber"),
    Beat("He sold everything at auction...", "money", "pullout", 0.7, 0.9, "dissolve",
         prompt="An auction of restaurant equipment, 1950s, photoreal, sad"),
    Beat("and barely paid off his debts.", "money", "pushin", 0.65, 0.9, "whip_l",
         prompt="Empty hands holding a few dollar bills, dim light, photoreal"),
    Beat("Sixty-five years old. Dead broke. Starting over.", "portrait", "pushin", 0.85, 1.3, "light_flash",
         prompt="A broke but unbroken older man staring ahead, dramatic light, photoreal"),
    Beat("He could have given up. And no one would have blamed him.", "horizon", "parallax_l", 0.6, 1.0, "dissolve",
         prompt="A lone man at a foggy crossroads at dusk, photoreal, uncertain"),
    Beat("But he believed in one thing. His recipe.", "recipe", "zoom3d", 0.85, 1.4, "light_flash",
         prompt="A handwritten recipe card held in weathered hands, photoreal, warm"),

    # ===== ACT 6 — THE ROAD & THE REJECTIONS ==============================
    Beat("So he packed his car and hit the road.", "car", "track_left", 0.6, 0.8, "speed_ramp",
         prompt="A packed 1950s car pulling onto an open highway at dawn, photoreal"),
    Beat("Town to town. Kitchen to kitchen.", "road", "parallax_r", 0.6, 0.8, "whip_r",
         prompt="A 1950s car driving through small American towns, photoreal, motion"),
    Beat("He would cook his chicken right there for the owner...", "recipe", "pushin", 0.6, 0.9, "dissolve",
         prompt="An older man cooking chicken in someone else's kitchen, photoreal"),
    Beat("and ask for just a nickel for every one they sold.", "handshake", "pushin", 0.65, 1.0, "whip_l",
         prompt="A nickel coin held up in the light, close-up, photoreal"),
    Beat("And the answer, almost every time, was no.", "door_closed", "pushin", 0.75, 1.0, "speed_ramp",
         prompt="A restaurant owner shaking his head, doorway, 1950s, photoreal"),
    Beat("One no.", "door_closed", "pushin", 0.6, 0.7, "light_flash",
         prompt="A single closed diner door, hard shadow, photoreal"),
    Beat("Ten no's.", "doors_many", "parallax_r", 0.68, 0.7, "whip_r",
         prompt="A row of closed restaurant doors, repetition, photoreal"),
    Beat("A hundred no's.", "doors_many", "parallax_l", 0.78, 0.7, "whip_l",
         prompt="An endless corridor of closing doors, photoreal, dramatic"),
    Beat("Then hundreds more.", "doors_many", "pushin", 0.85, 1.1, "speed_ramp",
         prompt="A fast montage of slamming doors, motion blur, photoreal, intense"),
    Beat("Every single rejection was a reason to stop.", "horizon", "parallax_l", 0.65, 1.0, "dissolve",
         prompt="An exhausted man resting on a steering wheel at night, photoreal, emotional"),
    Beat("He refused.", "portrait", "pushin", 0.92, 1.3, "light_flash",
         prompt="A defiant close-up, jaw set, dramatic rim light, photoreal, powerful"),
    Beat("Where others saw a broke old man...", "crowd", "parallax_r", 0.55, 0.8, "dissolve",
         prompt="People dismissing an older man on a busy street, photoreal"),
    Beat("he saw a second chance.", "sunrise", "rise", 0.78, 1.0, "light_flash",
         prompt="Sunrise breaking over an open road, hopeful rays, photoreal"),
    Beat("While the world kept saying no...", "crowd", "parallax_l", 0.6, 0.8, "dissolve",
         prompt="A sea of indifferent faces, muted, photoreal"),
    Beat("he just kept driving.", "road", "track_left", 0.8, 1.1, "speed_ramp",
         prompt="A determined driver, hands on the wheel, open road, photoreal, motion"),

    # ===== ACT 7 — THE FIRST YES & THE RISE ===============================
    Beat("And then, one day...", "door_closed", "pushin", 0.75, 1.4, "speed_ramp",
         prompt="A hand reaching toward a door handle, shaft of light, photoreal"),
    Beat("somebody finally said yes.", "handshake", "pushin", 0.92, 1.3, "light_flash",
         prompt="A warm handshake between two men in a 1950s restaurant, photoreal, emotional"),
    Beat("One handshake. One deal.", "handshake", "zoom3d", 0.8, 0.9, "whip_r",
         prompt="Two men shaking hands in golden light, close-up, photoreal"),
    Beat("And that one yes changed everything.", "sunrise", "rise", 0.88, 1.2, "speed_ramp",
         prompt="A radiant sunrise over a small American town, photoreal, uplifting"),
    Beat("The chicken was a hit.", "growth", "zoom3d", 0.78, 0.7, "whip_r",
         prompt="Delighted diners enjoying fried chicken, busy restaurant, photoreal"),
    Beat("Then another restaurant signed on. Then another.", "growth", "pushin", 0.82, 0.8, "whip_l",
         prompt="Several bustling 1950s restaurants with neon signs, photoreal"),
    Beat("They gave it a name. Kentucky Fried Chicken.", "map", "zoom3d", 0.85, 1.1, "light_flash",
         prompt="A glowing vintage map of the USA lighting up city by city, photoreal"),
    Beat("And it spread... clear across America.", "map", "pushin", 0.88, 1.2, "speed_ramp",
         prompt="Lights spreading across a map of the United States, photoreal, glowing"),

    # ===== ACT 8 — SUCCESS & LEGACY =======================================
    Beat("Within just a few short years, there were hundreds of locations.",
         "growth", "pushin", 0.8, 0.9, "dissolve",
         prompt="Rows of thriving restaurants at dusk, neon glow, photoreal"),
    Beat("The man who had nothing at sixty-five...", "portrait", "pushin", 0.8, 1.0, "whip_l",
         prompt="A dignified older man in a white suit, warm portrait light, photoreal"),
    Beat("sold his company for millions.", "success", "rise", 0.9, 1.1, "light_flash",
         prompt="A triumphant older man before a thriving restaurant empire, photoreal"),
    Beat("And he became the face of the brand...", "portrait", "pushin", 0.82, 1.0, "dissolve",
         prompt="Iconic Colonel Sanders portrait, white suit and string tie, photoreal"),
    Beat("the man in the white suit the whole world would come to know.",
         "success", "rise", 0.92, 1.3, "light_flash",
         prompt="The iconic white-suited Colonel, warm golden light, photoreal"),
    Beat("From a roadside kitchen...", "recipe", "parallax_r", 0.7, 0.8, "whip_r",
         prompt="A humble roadside diner kitchen, warm light, photoreal"),
    Beat("to one of the most famous names on the planet.", "success", "rise", 0.95, 1.5, "light_flash",
         prompt="Glowing iconic restaurant signs against a sunset sky, photoreal, epic"),

    # ===== ACT 9 — THE LESSONS ============================================
    Beat("So what can a story like this teach us?", "lesson", "pushin", 0.55, 1.0, "dissolve",
         prompt="Clean dark cinematic background, soft volumetric light, photoreal"),
    Beat("First. It is never too late.", "lesson", "pushin", 0.8, 1.1, "light_flash",
         prompt="A single beam of light breaking through darkness, photoreal"),
    Beat("He started over at an age when most people stop.", "portrait", "parallax_r", 0.6, 0.9, "dissolve",
         prompt="An older man stepping forward into light, photoreal, hopeful"),
    Beat("Second. Failure is not the end.", "lesson", "pullout", 0.8, 1.1, "light_flash",
         prompt="A road rising out of shadow into light, symbolic, photoreal"),
    Beat("He failed for forty years before he won.", "portrait", "pushin", 0.7, 1.0, "dissolve",
         prompt="A weathered, resolute face in dramatic light, photoreal"),
    Beat("Third. Persistence beats talent.", "lesson", "pushin", 0.85, 1.2, "light_flash",
         prompt="Bold light rays over a dark cinematic backdrop, photoreal"),
    Beat("He wasn't the smartest, or the luckiest.", "crowd", "parallax_l", 0.6, 0.9, "dissolve",
         prompt="An ordinary man among a crowd, photoreal"),
    Beat("He was simply the one who would not quit.", "portrait", "pushin", 0.9, 1.3, "light_flash",
         prompt="A determined elderly man, unbroken stare, dramatic light, photoreal"),
    Beat("Your breakthrough could be just one more try away.", "sunrise", "rise", 0.88, 1.2, "speed_ramp",
         prompt="Dawn flooding an open horizon, hopeful, photoreal, cinematic"),
    Beat("One more phone call.", "lesson", "pushin", 0.7, 0.7, "whip_l",
         prompt="A vintage 1950s rotary telephone in dramatic light, photoreal"),
    Beat("One more door.", "door_closed", "pushin", 0.72, 0.7, "whip_r",
         prompt="A door opening into warm light, photoreal"),
    Beat("One more yes.", "handshake", "rise", 0.8, 1.1, "light_flash",
         prompt="Two hands meeting in a handshake in golden light, photoreal"),
    Beat("So whatever you're up against today...", "crowd", "parallax_l", 0.65, 1.0, "dissolve",
         prompt="Everyday people with hopeful, determined faces, photoreal"),
    Beat("remember the old man in the white suit.", "success", "rise", 0.9, 1.5, "speed_ramp",
         prompt="The iconic white-suited Colonel glowing in golden light, photoreal, epic"),

    # ===== FINAL SCREEN ===================================================
    Beat("It is never too late.", "final", "pushin", 0.95, 1.2, "light_flash", is_final=True,
         prompt="Epic golden sunrise over America, cinematic, photoreal"),
    Beat("Success belongs to those who refuse to quit.", "final", "pushin", 0.95, 1.3, "light_flash",
         is_final=True, prompt="Radiant horizon with particles, cinematic, photoreal"),
    Beat("One more try.", "final", "pushin", 0.9, 1.0, "dissolve", is_final=True,
         prompt="Glowing horizon, particles, cinematic, photoreal"),
    Beat("Never quit.", "final", "pushin", 1.0, 2.4, "light_flash", is_final=True,
         prompt="Blinding triumphant light, cinematic, photoreal"),
]


def storyboard() -> list[Beat]:
    """Return the storyboard with stable per-beat indices assigned."""
    for i, b in enumerate(_RAW):
        b._index = i
    return _RAW
