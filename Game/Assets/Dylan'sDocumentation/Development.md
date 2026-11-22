# Dylan's Documentation

### First appearance

- As soon as I came into the project I downgraded python, set up venv and installed pygame.
- For the second task, I read main.py and give it a quick run
- On the third task I set up my Dylan files, and within these files are folders for my docs, artwork and animation controller scripts. 
- Lastly, I also made a 'Gamescripts' folder for shared development. it starts with a world_builder.py and a simple function. I feel that the world_builder.py is a good place for describing levels as opposed to using main.py for everything.

---

### Making an environment map grid with Kiro Free
![alt text](image.png)
---

### How the Environment grid map is coming out so far
![alt text](image-1.png)

---

### Recently Acquired an asset pack
- Cardboard Boxes by DANI MACCARI
- I took one cardboard box and animated the box as if it was opening
- I used a lightweight pixel art studio known as 'Piskel'

### Alongside finding asset packs
- I created my own ant character with idle and run animations

---

# Back to Kiro
### I had some help from free Kiro AI to help me with animations.
- It shows an explanation of why my method was not working, and the AI put my code on the Player class instead.
- The first animation implementation is working in main.py
![alt text](image-2.png)

### When developing 8 directions worth of spites
- I had to ask Kiro to implement animation triggers depending upon 8 different directions. I did not know how Kiro implementing the animation triggers so I ask for help. 
- Below is Kiro's implementation
![alt text](image-3.png)

### I also had kiro help implement the shoot function
- This only triggers the animation it doesn't include actual shooting logic just yet
![alt text](image-4.png)

---

### Wholesome notes
17/11/2026
- I have set the foundations for the spider class for Hana to look at. I have made it similar to the player class in how it functions in regards to triggering animations and handling directions.
- I have suggested Hana look at shooting, spider AI, improving the player, UI, health and ammo for both player and spider, look into loot boxes.
- I have some pressing matters with the map, boundaries, isometric tiles (potentially because it will improve the look of our game), sound effects, music and anywhere else I can support the cause.

---

### Back to Kiro
- I have ran out of my free plan of Kiro and now I am having to undertake research to finish off my work.
- Last thing Kiro did was show me how to increase sizes of my sprites in environment_obj.py
- I'm out here on my own now.... I need to figure out how to implement these isometric tiles and deactivate images that aren't in the camera view.... oh my life

---

### Since My free Kiro ran out, I was getting some help from online research and other AI.
- ESPECIALLY, for detecting boundaries (though I was right in implementing is boundary to objects on all 4 sides of the tile map grid), AI gave me code for detecting the rectangular collision of objects in the boundaries list. 

---

### Making of the spider AI, death and Bullet collision
- I initially had chatGPT help with using the right code to get collisions working, spiders spawning, and spiders moving. I set up a lot of the foundations in the classes, as well as the poolsystem and how the pool system connects to the y-sorted camera groups etc etc.

- However I couldn't understand how to make the spiders die and why bullet collisions were not responsive in the right way, and Kiro managed to wire it better
![alt text](image-5.png)


### I heard about sprite / animation caching to save performance
- I did not full understand how to implement this and the project architecture has already become quite large
- a quick Kiro prompt resolved this issue for how the player and spiders read and call animations. The scripts now no longer read images from disk every time animations change
![alt text](image-6.png)

---

### Without Kiro I had other AI help me keep shooting only available after animation has ended
- I tried this before and I couldn't get it to work
- I tried to do it by monitoring if shooting sound effect was playing - to no avail though
- AI helped in the end because I had two seperate things going on in the program loop and the player class. So AI wired both systems together to only shoot after sound effect is finished and after the last frame of the previous shooting animation.

---

### I have currently been working on:
- General Game design - Spider spawning interval adjustments & spider speed adjustments
- Score display and multipliers
- updating rewards from boxes to give the multipliers
- set up a perma multiplier for when you find the alcohol bottle

- things have taken a turn since finding out about copyright issues so we use a Pennine logo as satire for amazon, and we are no longer refering to the alcohol bottle as a bottle of Jack Daniel's whiskey.

- I have also been playing the game a lot because it is quite addictive in my opinion... probably not a good thing

---
# IMPORTANT

- Due to the need for getting the game playale in the web with pygodine, I have had to alter the file structure. All that is done is the game related files are in their own folder called 'Game' and the main.py is run through an async function called main. All of this was a requirement for making a build of the game for web browser.

---
# IMPORTANT

- Since running out of kiro and not receiving the credits to begin with and being very busy at the time such that I didn't re apply - I have been getting help from chatgpt.... to do things truly begond my skills level and knoweldge. 

- All of these things kiro could have done and also previously suggested such that I could remember what I needed to do. World chunking was one of these things to boost performance significantly. Kiro's suggestion and external AI implementation considering the circumstances. 

- I had to get help with pygame.mixer buffering and other specifications. I AM SO NEW TO PYGAME... and also I am a junior programmer and there is a lot I don't understand when it comes to what is happening on the hardware level. This is essential to know about for performance related things when building software. 

- HOWEVER - Hana has the kiro credits and kiro has done a lot for this game already. I have used the IDE, it is fine, I have had no problems it is the same as VS code on the surface and I have not had the time to explore various other features. Take pity on me

- I believe kiro took my isometric tiles and duplicated them around the corners of the map boundary and I could not for life of me figure that out.

- Lastly, I architectured quite a lot by systems design and giving the AI a good foundation to work from. I did this intuitively and applying the knowledge I already have to scaffolding this project, the classes, how things fit together etc. AI just helped us with py game because we were completely new to it. I would love to rebuild this in unity.