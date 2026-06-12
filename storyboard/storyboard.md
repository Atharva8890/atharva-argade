# Storyboard & Image Prompts

Drop a photoreal image for any beat into `assets/images/` using the
**file name** column below (e.g. `assets/images/04_closed.jpg`). The
renderer will use it automatically with full cinematic motion; any beat
without a supplied image falls back to a synthesized cinematic plate.

**Montage / many clips.** The edit cuts several quick sub-clips per line.
To feed the montage with real footage, supply *multiple* assets per beat:

- Extra photos: `04_closed-2.jpg`, `04_closed-3.jpg`, ... (any number).
- Video clips: `04_closed.mp4` (or `assets/clips/04_closed.mp4`), plus
  `04_closed-2.mp4`, ... — used as moving B-roll for that line.

If only one image is supplied, the montage automatically re-frames it
(different zoom/crop per cut). Control cut speed with `--clip-density`.

Recommended size: 2560x1440 or larger, 16:9. Suggested style suffix for
every prompt: *photoreal, 1950s America, cinematic lighting, Kodachrome,
film grain, shallow depth of field, ultra realistic, no text*.

| # | File name | Scene | Effect | Narration | Image prompt |
|---|-----------|-------|--------|-----------|--------------|
| 0 | `00_title.jpg` | title | pushin | Picture a man. | Extreme close-up of an elderly man's eyes behind glasses in shadow, mysterious, dramatic chiaroscuro, photoreal, archival |
| 1 | `01_portrait.jpg` | portrait | pushin | Sixty-five years old. | Silhouetted elderly man, face half in shadow, 1950s, photoreal |
| 2 | `02_money.jpg` | money | pushin | Flat broke. | A few coins and a worn wallet on an empty table, dim light, photoreal still life |
| 3 | `03_money.jpg` | money | pullout | Living on a single Social Security check. | A government check on a kitchen table in a humble 1950s home, photoreal, melancholic |
| 4 | `04_car.jpg` | car | track_left | Driving a beat-up car across America... | An old 1950s sedan on a lonely highway at dawn, photoreal |
| 5 | `05_car.jpg` | car | parallax_r | Sleeping in the back seat... | A man sleeping in the back seat of a 1950s car at night, streetlight glow, photoreal, intimate |
| 6 | `06_door_closed.jpg` | door_closed | pushin | Knocking on door after door... | A weathered hand knocking on a diner door, 1950s, photoreal |
| 7 | `07_door_closed.jpg` | door_closed | pushin | And hearing the same word every single time. No. | A door closing in the viewer's face, hard shadow, 1950s, photoreal, dramatic |
| 8 | `08_doors_many.jpg` | doors_many | zoom3d | By some accounts, he heard it more than a thousand times. | An endless corridor of closing doors, deep perspective, photoreal, intense |
| 9 | `09_crowd.jpg` | crowd | parallax_l | Most men would have quit a lifetime ago. | Defeated men in a dim 1950s bar, muted tones, photoreal |
| 10 | `10_portrait.jpg` | portrait | pushin | But this man was only just getting started. | Determined elderly man lifting his gaze toward the light, photoreal |
| 11 | `11_map.jpg` | map | zoom3d | And what he was about to build... | A glowing vintage map of America, lights beginning to appear, photoreal |
| 12 | `12_success.jpg` | success | rise | you would recognize anywhere in the world. | Bright neon restaurant signs glowing at dusk, iconic, photoreal |
| 13 | `13_title.jpg` | title | pushin | This is the story of Colonel Harland Sanders. | Iconic Colonel Sanders in white suit and string tie, warm key light, dignified, photoreal, archival |
| 14 | `14_portrait.jpg` | portrait | parallax_r | He was born in 1890, in a small Indiana town. | A young man's vintage sepia portrait, early 1900s, photoreal, archival |
| 15 | `15_portrait.jpg` | portrait | pushin | When he was just five years old, his father died. | A somber young boy in early 1900s clothing, soft window light, photoreal |
| 16 | `16_crowd.jpg` | crowd | parallax_l | His mother went to work to keep food on the table. | A hardworking woman in an early 1900s kitchen, warm light, photoreal |
| 17 | `17_recipe.jpg` | recipe | pushin | And little Harland was left to cook for his brother and sister. | A child's hands cooking at an old wood stove, early 1900s kitchen, photoreal |
| 18 | `18_recipe.jpg` | recipe | zoom3d | By the age of seven, he could cook a full meal. | A simple home-cooked meal on a rustic table, warm light, photoreal |
| 19 | `19_road.jpg` | road | track_left | By thirteen, he left home to make his own way. | A young boy walking down a dirt country road with a small bag, dawn, photoreal, cinematic |
| 20 | `20_time.jpg` | time | zoom3d | And for the next forty years... | Changing seasons and passing years over rural America, photoreal |
| 21 | `21_horizon.jpg` | horizon | pushin | life knocked him down again... and again... and again. | A lone figure walking into a hard wind on an empty road, photoreal, moody |
| 22 | `22_crowd.jpg` | crowd | parallax_r | He worked as a farmhand. | A man working a field on an early American farm, photoreal |
| 23 | `23_crowd.jpg` | crowd | parallax_l | A streetcar conductor. | A vintage streetcar on a city street, early 1900s, photoreal |
| 24 | `24_road.jpg` | road | track_right | A railroad fireman. | A steam locomotive and railway, vintage, photoreal, dramatic |
| 25 | `25_crowd.jpg` | crowd | pushin | He sold insurance. He sold tires. | A door-to-door salesman with a case, 1920s street, photoreal |
| 26 | `26_horizon.jpg` | horizon | parallax_l | He ran a ferry boat. He even studied law... | A small ferry crossing a wide river, vintage, photoreal |
| 27 | `27_closed.jpg` | closed | pushin | until a courtroom fight ended that dream, too. | An empty vintage courtroom in dramatic light, photoreal |
| 28 | `28_closed.jpg` | closed | parallax_r | He lost job after job. | A 'closed' sign hanging in a dusty window, photoreal |
| 29 | `29_closed.jpg` | closed | pushin | Business after business. | A shuttered storefront on a quiet street, photoreal, melancholic |
| 30 | `30_horizon.jpg` | horizon | parallax_l | By the age when most men think about slowing down... | An older man's silhouette at a crossroads at dusk, photoreal |
| 31 | `31_portrait.jpg` | portrait | pushin | Harland Sanders had almost nothing to show for it. | A weary but dignified older man's face, soft shadow, photoreal |
| 32 | `32_recipe.jpg` | recipe | parallax_r | But in a little gas station in Corbin, Kentucky... | A 1930s roadside gas station with a small cafe, photoreal, warm |
| 33 | `33_recipe.jpg` | recipe | pushin | he started cooking for hungry travelers. | A cook serving plates at a busy roadside counter, 1930s, photoreal |
| 34 | `34_recipe.jpg` | recipe | zoom3d | Fried chicken. Country ham. Fresh biscuits. | A spread of fried chicken, ham and biscuits on a diner table, photoreal, warm |
| 35 | `35_crowd.jpg` | crowd | parallax_l | And people drove for miles just to taste it. | Cars lined up outside a busy roadside diner, 1940s, photoreal |
| 36 | `36_recipe.jpg` | recipe | pushin | He perfected a secret recipe... | Hands blending herbs and spices on a wooden table, macro, photoreal |
| 37 | `37_recipe.jpg` | recipe | zoom3d | eleven herbs and spices. | Steam rising from golden fried chicken, close-up, photoreal, warm |
| 38 | `38_recipe.jpg` | recipe | pushin | He found a faster way to cook it. | A vintage pressure cooker in a busy 1940s kitchen, photoreal |
| 39 | `39_growth.jpg` | growth | rise | And for the first time in his life... things were working. | A warm, full restaurant with happy customers, 1940s, photoreal |
| 40 | `40_portrait.jpg` | portrait | pushin | The state even made him a Kentucky Colonel. | A proud man receiving an honor, warm portrait light, photoreal |
| 41 | `41_success.jpg` | success | rise | Finally, after all those years... he had built something. | A thriving roadside restaurant at golden hour, photoreal, hopeful |
| 42 | `42_horizon.jpg` | horizon | pushin | And then... | Dark storm clouds rolling over an open highway, photoreal, ominous |
| 43 | `43_road.jpg` | road | track_left | they built a brand-new highway. | A new interstate highway under construction, 1950s, photoreal |
| 44 | `44_road.jpg` | road | parallax_r | And it ran right past his door. | An empty old road bypassed by a distant new highway, photoreal, lonely |
| 45 | `45_closed.jpg` | closed | pushin | The customers vanished. | An empty diner with stacked chairs, dim light, photoreal, melancholic |
| 46 | `46_closed.jpg` | closed | pushin | The restaurant he loved... was finished. | A 'closed' sign on a darkened restaurant door, photoreal, somber |
| 47 | `47_money.jpg` | money | pullout | He sold everything at auction... | An auction of restaurant equipment, 1950s, photoreal, sad |
| 48 | `48_money.jpg` | money | pushin | and barely paid off his debts. | Empty hands holding a few dollar bills, dim light, photoreal |
| 49 | `49_portrait.jpg` | portrait | pushin | Sixty-five years old. Dead broke. Starting over. | A broke but unbroken older man staring ahead, dramatic light, photoreal |
| 50 | `50_horizon.jpg` | horizon | parallax_l | He could have given up. And no one would have blamed him. | A lone man at a foggy crossroads at dusk, photoreal, uncertain |
| 51 | `51_recipe.jpg` | recipe | zoom3d | But he believed in one thing. His recipe. | A handwritten recipe card held in weathered hands, photoreal, warm |
| 52 | `52_car.jpg` | car | track_left | So he packed his car and hit the road. | A packed 1950s car pulling onto an open highway at dawn, photoreal |
| 53 | `53_road.jpg` | road | parallax_r | Town to town. Kitchen to kitchen. | A 1950s car driving through small American towns, photoreal, motion |
| 54 | `54_recipe.jpg` | recipe | pushin | He would cook his chicken right there for the owner... | An older man cooking chicken in someone else's kitchen, photoreal |
| 55 | `55_handshake.jpg` | handshake | pushin | and ask for just a nickel for every one they sold. | A nickel coin held up in the light, close-up, photoreal |
| 56 | `56_door_closed.jpg` | door_closed | pushin | And the answer, almost every time, was no. | A restaurant owner shaking his head, doorway, 1950s, photoreal |
| 57 | `57_door_closed.jpg` | door_closed | pushin | One no. | A single closed diner door, hard shadow, photoreal |
| 58 | `58_doors_many.jpg` | doors_many | parallax_r | Ten no's. | A row of closed restaurant doors, repetition, photoreal |
| 59 | `59_doors_many.jpg` | doors_many | parallax_l | A hundred no's. | An endless corridor of closing doors, photoreal, dramatic |
| 60 | `60_doors_many.jpg` | doors_many | pushin | Then hundreds more. | A fast montage of slamming doors, motion blur, photoreal, intense |
| 61 | `61_horizon.jpg` | horizon | parallax_l | Every single rejection was a reason to stop. | An exhausted man resting on a steering wheel at night, photoreal, emotional |
| 62 | `62_portrait.jpg` | portrait | pushin | He refused. | A defiant close-up, jaw set, dramatic rim light, photoreal, powerful |
| 63 | `63_crowd.jpg` | crowd | parallax_r | Where others saw a broke old man... | People dismissing an older man on a busy street, photoreal |
| 64 | `64_sunrise.jpg` | sunrise | rise | he saw a second chance. | Sunrise breaking over an open road, hopeful rays, photoreal |
| 65 | `65_crowd.jpg` | crowd | parallax_l | While the world kept saying no... | A sea of indifferent faces, muted, photoreal |
| 66 | `66_road.jpg` | road | track_left | he just kept driving. | A determined driver, hands on the wheel, open road, photoreal, motion |
| 67 | `67_door_closed.jpg` | door_closed | pushin | And then, one day... | A hand reaching toward a door handle, shaft of light, photoreal |
| 68 | `68_handshake.jpg` | handshake | pushin | somebody finally said yes. | A warm handshake between two men in a 1950s restaurant, photoreal, emotional |
| 69 | `69_handshake.jpg` | handshake | zoom3d | One handshake. One deal. | Two men shaking hands in golden light, close-up, photoreal |
| 70 | `70_sunrise.jpg` | sunrise | rise | And that one yes changed everything. | A radiant sunrise over a small American town, photoreal, uplifting |
| 71 | `71_growth.jpg` | growth | zoom3d | The chicken was a hit. | Delighted diners enjoying fried chicken, busy restaurant, photoreal |
| 72 | `72_growth.jpg` | growth | pushin | Then another restaurant signed on. Then another. | Several bustling 1950s restaurants with neon signs, photoreal |
| 73 | `73_map.jpg` | map | zoom3d | They gave it a name. Kentucky Fried Chicken. | A glowing vintage map of the USA lighting up city by city, photoreal |
| 74 | `74_map.jpg` | map | pushin | And it spread... clear across America. | Lights spreading across a map of the United States, photoreal, glowing |
| 75 | `75_growth.jpg` | growth | pushin | Within just a few short years, there were hundreds of locations. | Rows of thriving restaurants at dusk, neon glow, photoreal |
| 76 | `76_portrait.jpg` | portrait | pushin | The man who had nothing at sixty-five... | A dignified older man in a white suit, warm portrait light, photoreal |
| 77 | `77_success.jpg` | success | rise | sold his company for millions. | A triumphant older man before a thriving restaurant empire, photoreal |
| 78 | `78_portrait.jpg` | portrait | pushin | And he became the face of the brand... | Iconic Colonel Sanders portrait, white suit and string tie, photoreal |
| 79 | `79_success.jpg` | success | rise | the man in the white suit the whole world would come to know. | The iconic white-suited Colonel, warm golden light, photoreal |
| 80 | `80_recipe.jpg` | recipe | parallax_r | From a roadside kitchen... | A humble roadside diner kitchen, warm light, photoreal |
| 81 | `81_success.jpg` | success | rise | to one of the most famous names on the planet. | Glowing iconic restaurant signs against a sunset sky, photoreal, epic |
| 82 | `82_lesson.jpg` | lesson | pushin | So what can a story like this teach us? | Clean dark cinematic background, soft volumetric light, photoreal |
| 83 | `83_lesson.jpg` | lesson | pushin | First. It is never too late. | A single beam of light breaking through darkness, photoreal |
| 84 | `84_portrait.jpg` | portrait | parallax_r | He started over at an age when most people stop. | An older man stepping forward into light, photoreal, hopeful |
| 85 | `85_lesson.jpg` | lesson | pullout | Second. Failure is not the end. | A road rising out of shadow into light, symbolic, photoreal |
| 86 | `86_portrait.jpg` | portrait | pushin | He failed for forty years before he won. | A weathered, resolute face in dramatic light, photoreal |
| 87 | `87_lesson.jpg` | lesson | pushin | Third. Persistence beats talent. | Bold light rays over a dark cinematic backdrop, photoreal |
| 88 | `88_crowd.jpg` | crowd | parallax_l | He wasn't the smartest, or the luckiest. | An ordinary man among a crowd, photoreal |
| 89 | `89_portrait.jpg` | portrait | pushin | He was simply the one who would not quit. | A determined elderly man, unbroken stare, dramatic light, photoreal |
| 90 | `90_sunrise.jpg` | sunrise | rise | Your breakthrough could be just one more try away. | Dawn flooding an open horizon, hopeful, photoreal, cinematic |
| 91 | `91_lesson.jpg` | lesson | pushin | One more phone call. | A vintage 1950s rotary telephone in dramatic light, photoreal |
| 92 | `92_door_closed.jpg` | door_closed | pushin | One more door. | A door opening into warm light, photoreal |
| 93 | `93_handshake.jpg` | handshake | rise | One more yes. | Two hands meeting in a handshake in golden light, photoreal |
| 94 | `94_crowd.jpg` | crowd | parallax_l | So whatever you're up against today... | Everyday people with hopeful, determined faces, photoreal |
| 95 | `95_success.jpg` | success | rise | remember the old man in the white suit. | The iconic white-suited Colonel glowing in golden light, photoreal, epic |
| 96 | `96_final.jpg` | final | pushin | It is never too late. | Epic golden sunrise over America, cinematic, photoreal |
| 97 | `97_final.jpg` | final | pushin | Success belongs to those who refuse to quit. | Radiant horizon with particles, cinematic, photoreal |
| 98 | `98_final.jpg` | final | pushin | One more try. | Glowing horizon, particles, cinematic, photoreal |
| 99 | `99_final.jpg` | final | pushin | Never quit. | Blinding triumphant light, cinematic, photoreal |
