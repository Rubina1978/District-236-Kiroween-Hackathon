# District 236 - Credits

A spooky 2.5D forest adventure about an ant soldier, giant spiders and a legendary bottle of Ant Whiskey.
Made for the 2026 Kiroween Hackathon.

District 236 is a fan-made, non-commercial project. It is inspired by *Kota 236*, the 2001 promotional game
of the Czech company Jan Becher (Becherovka). It is not affiliated with or endorsed by Jan Becher.

---

## The team

### Hana ([@Rubina1978](https://github.com/Rubina1978)) - project owner, game development and integration

- Set up the project: the Pygame window and game loop, the project structure, the Kiro steering documents
  and the GitHub project board.
- World boundaries around the map.
- Shooting: firing bullets, bullet range and removal, the ammo limit, aiming with the mouse, and the ant
  turning to face the direction it shoots.
- Loot boxes: random rewards (ammo and extra lives) with the reward pop-up.
- Lives: the `LifeLine` class (3 lives, up to 5, losing and gaining lives, death).
- Combat balance: 2 seconds of protection after a spider bite, the ant blinking, the red damage flash,
  knockback, spiders backing away while the ant is protected, and the spider speed range.
- Added the spiders into the game and joined everyone's work together (merging branches).
- Game states and menus: the main menu with its typewriter story and the ant and spider that turn to face
  each other, plus the Help, Credits, Game Over and Victory screens.
- The ending: the chest opens, the bottle floats up out of it, then the Victory screen.
- The ant drawn at double size, and the rename to District 236.

### Dylan ([@DylanAustin-TheDreamer](https://github.com/DylanAustin-TheDreamer)) - art, audio, enemies, interface and website

- Created the ant character and its idle and run animations, and the animation controllers.
- The spider class, spawning and pooling, spider movement and death, and the bullet collisions
  (written with help from AI tools, see below).
- Y-sorting and the camera, the lighting, and the sprite cache.
- The interface: the health and ammo display, the reward pop-up, the score and best score, and the mute button.
- The end-game chest and the game-over and victory logic.
- All music and sound editing (see Audio below).
- The website (`index.html`), the web build, and the development documentation.

---

## Tools and AI assistance

- **Pygame** for the game.
- **Kiro** (IDE and AI assistant) was used throughout the project for code help and explanations.
  Hana held the Kiro credits.
- **ChatGPT** was used by Dylan in the early stages of the spider code (see his development notes in
  `Game/Assets/Dylan'sDocumentation/Development.md`).

---

## Artwork

- **Cardboard box (loot box)** - Dani Maccari, https://dani-maccari.itch.io/
  Free for personal and commercial use as long as it is credited to DANI MACCARI.
- **Chest and other props** - "Pixel Worlds - 50 Dungeon & Dragon Castle Props (Free)" by SdavGha.
  The images were generated with Krea 2 Turbo (Krea AI), then cut and turned into pixel art by SdavGha.
  No attribution is required by the licence.
- **Ant character and animations** - Dylan.
- **Spider, bottle, tiles, trees and rocks, icons** - *to be confirmed:* artist, source and licence.
- **Menu pictures** - the menu uses the game's own ant and spider sprites, enlarged for the title screen.

## Audio

Full details are in `Game/Assets/Audio/AttributionAudio.md`.

- **Music: "Retro Ant Soldiers" and the other game tracks** - Dylan Austin. Produced and mastered with BandLab.
  Rights reserved for the time being.
- **Footsteps** - "Fantozzi's Footsteps (Grass/Sand/Stone)", Fantozzi, https://opengameart.org/content/fantozzis-footsteps-grasssand-stone
  Licence: CC0. Edited by Dylan (cut into short loops).
- **Gun shots** - Michel Baradari, https://opengameart.org/content/chaingun-pistol-rifle-shotgun-shots
  Licence: CC BY 3.0, https://creativecommons.org/licenses/by/3.0/. Edited by Dylan (cut into short clips).
- **Cardboard box** - newagesoup, https://freesound.org/people/newagesoup/sounds/364740/ (CC0).
- **"oh sh-t"** - xtrgamr, https://freesound.org/people/xtrgamr/sounds/278895/ (Creative Commons, attribution required).
- **Splat / squish** - mrickey13, https://freesound.org/s/515621/ (CC0).

---

## Asset credits still to fill in

Before submitting, please add the source and licence for anything marked "to be confirmed" above.

| Asset | Creator | Source URL | Licence |
|---|---|---|---|
| Spider artwork | | | |
| Bottle artwork (AntWhiskey) | | | |
| Ground tiles, trees, rocks, bushes | | | |
| Icons (heart, ammo, music) | | | |
