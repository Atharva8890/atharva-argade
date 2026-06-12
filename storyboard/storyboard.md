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
| 0 | `00_title.jpg` | title | pushin | Let me tell you about a man who heard the word no... more than a thousand times. | Extreme close-up of elderly Colonel Sanders' eyes behind glasses, white goatee, dramatic chiaroscuro lighting, photoreal, archival |
| 1 | `01_portrait.jpg` | portrait | pushin | He was sixty-five years old. | Dignified portrait of Colonel Harland Sanders in his white suit and string tie, warm window light, photoreal, archival |
| 2 | `02_crowd.jpg` | crowd | parallax_r | Most folks his age were settling into retirement. | Older Americans relaxing on a quiet 1950s small-town main street, golden hour, nostalgic, photoreal documentary |
| 3 | `03_portrait.jpg` | portrait | pushin | Harland Sanders was just getting started. | Determined Colonel Sanders looking toward the horizon, hopeful morning light, 1950s, photoreal |
| 4 | `04_closed.jpg` | closed | pushin | His restaurant had gone under. | A small 1950s American roadside restaurant, empty and closed, overcast, melancholic, photoreal |
| 5 | `05_money.jpg` | money | pullout | The money was gone. | Empty cash register and a few coins on a worn diner counter, 1950s, dim light, photoreal still life |
| 6 | `06_horizon.jpg` | horizon | parallax_l | And the road ahead was wide open... and terrifying. | Lone empty American highway stretching into fog at a crossroads, 1950s, uncertain mood, photoreal, cinematic |
| 7 | `07_crowd.jpg` | crowd | parallax_l | Most people would have called it quits. | Tired men sitting in a 1950s small-town diner booth, muted colors, photoreal documentary |
| 8 | `08_horizon.jpg` | horizon | pushin | Most people would have packed it in. | A man's back as he stares down a dead-end road, 1950s, low contrast, melancholic, photoreal |
| 9 | `09_portrait.jpg` | portrait | pushin | But this old man had one thing he believed in. | Close-up of Colonel Sanders' resolute face, single key light, hope in his eyes, photoreal, cinematic |
| 10 | `10_recipe.jpg` | recipe | zoom3d | A recipe. Eleven herbs and spices. | Steam rising from a skillet of golden fried chicken on a 1950s diner counter, photoreal, macro, warm |
| 11 | `11_car.jpg` | car | parallax_r | So with almost nothing to his name... | A worn 1950s sedan packed with belongings outside a modest house at dawn, photoreal, cinematic |
| 12 | `12_road.jpg` | road | track_left | He loaded up his car and hit the road, crisscrossing America. | A vintage 1950s car driving down an open American highway, vast landscape, golden hour, photoreal, motion |
| 13 | `13_door_closed.jpg` | door_closed | pushin | And door after door, they turned him down. | A restaurant owner closing the door on a hopeful salesman, 1950s diner entrance, photoreal, dramatic |
| 14 | `14_door_closed.jpg` | door_closed | pushin | One no. | A single closed wooden diner door, hard shadow, 1950s, photoreal |
| 15 | `15_doors_many.jpg` | doors_many | parallax_r | Ten no's. | A row of closed restaurant doors down a 1950s main street, repetition, photoreal, cinematic |
| 16 | `16_doors_many.jpg` | doors_many | parallax_l | A hundred no's. | An endless corridor of closing doors, deep perspective, 1950s tones, photoreal, dramatic |
| 17 | `17_doors_many.jpg` | doors_many | pushin | Then hundreds more. | An overwhelming montage of slamming doors, fast motion blur, 1950s, photoreal, intense |
| 18 | `18_horizon.jpg` | horizon | parallax_l | Every rejection was another reason to give up. | An exhausted older man resting his head on a car steering wheel at night, rain on the windshield, photoreal, emotional |
| 19 | `19_portrait.jpg` | portrait | pushin | He refused. | Defiant close-up of Colonel Sanders, jaw set, dramatic rim light, photoreal, powerful |
| 20 | `20_horizon.jpg` | horizon | parallax_l | Where others saw a dead end... | A barricaded dead-end road under grey skies, 1950s, photoreal |
| 21 | `21_sunrise.jpg` | sunrise | rise | He saw a door. | Sunrise breaking over an open American road, hopeful light rays, photoreal, cinematic warm |
| 22 | `22_crowd.jpg` | crowd | parallax_r | Where others quit... | People standing still in a 1950s town square, muted, photoreal |
| 23 | `23_road.jpg` | road | track_left | He kept driving. | Determined hands firm on the wheel of a 1950s car, open road ahead, photoreal, motion blur |
| 24 | `24_crowd.jpg` | crowd | parallax_l | Where others complained... | A group of men grumbling in a 1950s diner booth, photoreal |
| 25 | `25_portrait.jpg` | portrait | pushin | He kept believing. | Colonel Sanders looking upward with quiet faith, soft halo light, photoreal, hopeful |
| 26 | `26_time.jpg` | time | zoom3d | Years went by. | Changing seasons over an American highway, time passing, 1950s, photoreal, cinematic |
| 27 | `27_road.jpg` | road | track_right | The struggle didn't let up. | A lonely car on an endless highway at dusk, 1950s, photoreal, moody |
| 28 | `28_portrait.jpg` | portrait | pushin | But neither did he. | Weathered but resolute Colonel Sanders, steady gaze, dramatic light, photoreal |
| 29 | `29_door_closed.jpg` | door_closed | pushin | And then one day... | A hand reaching toward a door handle, anticipation, a shaft of light, 1950s, photoreal, cinematic |
| 30 | `30_handshake.jpg` | handshake | pushin | Somebody finally said yes. | A warm handshake between two men in a 1950s restaurant, deal sealed, golden light, photoreal, emotional |
| 31 | `31_sunrise.jpg` | sunrise | rise | And that one yes changed everything. | A radiant sunrise over a small American town, new beginning, photoreal, uplifting |
| 32 | `32_growth.jpg` | growth | zoom3d | The recipe caught on. | Fried chicken served to delighted 1950s diners, busy restaurant, warm light, photoreal |
| 33 | `33_growth.jpg` | growth | pushin | The business took off. | Rows of bustling 1950s American restaurants with neon signs at dusk, photoreal, cinematic |
| 34 | `34_map.jpg` | map | zoom3d | And that little brand spread clear across America. | A vintage map of the United States lighting up city by city, 1950s aesthetic, photoreal, glowing |
| 35 | `35_portrait.jpg` | portrait | pushin | The man nobody wanted... | A proud Colonel Sanders in white suit and string tie, iconic look, warm portrait light, photoreal |
| 36 | `36_success.jpg` | success | rise | Became one of the most successful entrepreneurs this country has ever seen. | Iconic Colonel Sanders standing tall, triumphant, golden hour, photoreal |
| 37 | `37_lesson.jpg` | lesson | pushin | Now, this isn't a story about fried chicken. | Clean dark cinematic background with soft volumetric light, minimal, photoreal |
| 38 | `38_lesson.jpg` | lesson | pullout | It's not even about business. | Clean dark cinematic background, drifting dust particles, photoreal |
| 39 | `39_lesson.jpg` | lesson | pushin | It's about persistence. | A single beam of light cutting through darkness onto an open road, symbolic, photoreal, cinematic |
| 40 | `40_lesson.jpg` | lesson | parallax_r | Success doesn't go to the smartest person in the room. | Abstract cinematic light rays over a dark backdrop, photoreal |
| 41 | `41_lesson.jpg` | lesson | parallax_l | It doesn't go to the luckiest. | Abstract cinematic light rays, dust motes, dark backdrop, photoreal |
| 42 | `42_sunrise.jpg` | sunrise | rise | It goes to the ones who refuse to quit. | A silhouette of a determined figure walking into a glowing sunrise, photoreal, triumphant, cinematic |
| 43 | `43_sunrise.jpg` | sunrise | pushin | Because your big break might be just one more shot away. | Dawn light flooding an open horizon, hopeful, photoreal, cinematic |
| 44 | `44_lesson.jpg` | lesson | pushin | One more phone call. | A vintage 1950s rotary telephone in dramatic light, photoreal |
| 45 | `45_handshake.jpg` | handshake | pushin | One more meeting. | Two men shaking hands in a doorway of light, photoreal |
| 46 | `46_sunrise.jpg` | sunrise | rise | One more try. | A single figure stepping forward into radiant light, photoreal |
| 47 | `47_lesson.jpg` | lesson | pushin | So remember this. | Dark cinematic backdrop, a single soft spotlight, photoreal |
| 48 | `48_crowd.jpg` | crowd | parallax_l | The people who change their lives aren't always the most talented. | Ordinary 1950s Americans with hopeful faces, photoreal |
| 49 | `49_road.jpg` | road | track_left | They're the ones who keep going long after everybody else gives up. | One car driving on while others sit parked at the roadside, 1950s, sunrise, photoreal, symbolic |
| 50 | `50_final.jpg` | final | pushin | Success belongs to those who refuse to quit. | Epic golden sunrise over America, cinematic, photoreal |
| 51 | `51_final.jpg` | final | pushin | One more try. | Glowing horizon, particles, cinematic, photoreal |
| 52 | `52_final.jpg` | final | pushin | One more step. | Glowing horizon, particles, cinematic, photoreal |
| 53 | `53_final.jpg` | final | pushin | Never quit. | Blinding triumphant light, cinematic, photoreal |
