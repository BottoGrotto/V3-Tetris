# Tetris made w/Python & Pygame
## Table of Contents
* [Project Description](#project-description)
* [Design Choices](#design-choices)
* [File Descriptions](#file-descriptions)
## Project Description:
> For my final project I decided to remake a very popular game called Tetris. I did this by using **Python** for the game logic and a library called **Pygame** for displaying everything. My biggest issue was collision checking, I had to come up with a way for any piece to be able to fall and collide properly with the other pieces, regardless of rotation, on the grid even after parts of the other pieces had been cleared. I cracked the _"code"_ with the idea of checking where the piece wants to be and avoiding itself during the checking. The project was fun to take on and I think that it turned into a fun little game. I've played a lot of it during development!

## Design Choices:
#### <font color="#28a4f7">**Menus & UI**</font> :<br/>
> I found designing the menus to be fairly difficult so I ultimately went with a simple look. I chose colors for the text that went along with the colors of the pieces which _surprisingly_ didn't come to me at first. When it came to the button design I found that just having text for the button flowed the best in development and went along with the theme of the menus.

#### <font color="#28a4f7">**Pieces**</font> :<br/>
> I chose to make the pieces have a little depth to them (_there is a secret keybind on `I` that allows you to change the size of the depth, I used it for testing_), it helped seperate them and allow you to easier see where the actual piece is. Without it all the pieces blend together. As well, for the colors of the pieces I had to pick colors that contrasted nicely and wouldn't become a distraction when you're moving rapidly.

## File Descriptions:
#### <font color="#28a4f7">**main.py**</font> :<br/>
>This is the main file for the game. It contains the <font color="#61fa32"> **Game** </font>class, which manages **creating the window** using pygame, the main **game loop** under the run function, the **game state** (i.e., settings menu, playing, menu, gameover), **rendering the board** (i.e., which things to render, pieces, lines, ghost, text), **user input** like mouse click and certain button presses (through the pygame library), **scoring**, and **settings**. As well, the Game class handles spawning new shapes through the [shapespawner.py](#shapespawnerLink) class <font color="#61fa32">**ShapeSpawner**</font>.


#### <font color="#28a4f7">**shape.py**</font> :<br/>
> This is an extensive file that contains the base <font color="#61fa32">**Shape**</font> class and subclasses for each of the 7 Tetris pieces (**Square, L_1, L_2, T, I, Z_1, Z_2**). The base shape class allows for management of its own **position**, **rotation**, **movement** (detection of piece movement through user input) or falling which is set by the timer falling speed using the <font color="#61fa32">**Timer**</font> class in [timer.py](#timerLink), **collision detection**, and **rendering logic** (adding the shape to the grid). Thus each Tetris piece is able to detect input (independently from the main game loop), and check if it's able to move based on that input then it moves accordingly. The ghost is also calculated in this class and is rendered when the function <font color="#fff314">**render_ghost()**</font> is called.

#### <font color="#28a4f7"><a id="shapespawnerLink"></a>**shapespawner.py**</font> :<br/>
> This file implements the <font color="#61fa32">**ShapeSpawner**</font> class, which helps manage **spawning** the different pieces according to the **7 bag randomization** system. Each piece is pulled once before a new bag is generated, this ensures all the pieces occure once on the game board before any are repeated. To get a random shape you just have to call the <font color="#fff314">**pull_randomly_from_bag()**</font> function and it'll return a shape and if the bags empty it'll generate a new one.

#### <font color="#28a4f7"><a id="timerLink"></a>**timer.py**</font> :<br/>
> This is a very simple file that provides a <font color="#61fa32">**Timer**</font> class for managing timed events, like the animations or making the pieces fall. It's pretty simple and supports **looping**, **stoping**, **starting**, and checking if it's expired. It utilizes the pygame <font color="#fff314">**get_ticks()**</font> function for calculating the time since starting the timer.

#### <font color="#28a4f7">**color.py**</font> :<br/>
> This file contains a <font color="#61fa32">Color</font> class which helps simplify managing color for the different tetris pieces. It has a function for subtracting an integer from all three values (<font color="#ff1f1f">r</font>, <font color="#66ff1f">g</font>, <font color="#0a50ff">b</font>) this is utilized for creating depth in the tetris piece. It's a nice utility for making colors easier to deal with.

#### <font color="#28a4f7">**utilities.py**</font> :<br/>
> This contains utility classes for the game's UI. That includes the <font color="#61fa32">Button</font> class (this allows for **clickable buttons** that run given functions when clicked) and the <font color="#61fa32">Slider</font> class (**adjustable sliders**, e.g., for volume). Both of these classes handle rendering of their respective buttons and user interactions for their UI elements. They are simple to implement into your own code with a line for creation and a single call to handle all checks and updates.