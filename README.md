# Trade_Of_Life
A survival game built with python where every choice has a cost. Collect green orbs to heal but shrink your platform, or red ones to stay larger and lose HP. Balance risk, reward, and endurance as difficulty rises. Inspired by the theme “Sacrifices Must Be Made.”

Trade of Life is a Python based survival game built around the theme “Sacrifices Must Be Made."
Every choice has a consequence — collect the right items to survive, but beware: your size and survival are bound by the sacrifices you make.



Gameplay Overview:

You control a platform at the bottom of the screen:

Green items restore health but shrink your platform, making survival harder.

Red items damage you but increase your size, offering safety at a cost.

HP slowly drains over time — you must keep collecting to survive.

The game ends when HP reaches 0 or your size becomes too small.

Background music and sound effects react to your actions for an immersive feel.





Features:

Smooth 60 FPS gameplay loop.

Dynamic difficulty scaling — faster fall speed, smaller items, and shorter spawn intervals as score increases.

Persistent high score system stored in high_score.json.

Background music and synthesized sound effects (no external sound files needed).

Modular and optimized code structure using OOP (Game, Player, Item classes).

Pause, resume, restart, and game-over states.





Controls:

← / A	Move Left
→ / D	Move Right
SPACE	Start / Pause / Resume / Restart
ESC	Quit the Game




Installation:

1. Make sure you have Python 3.8+ installed.


2. Install dependencies:

pip install pygame numpy



4. Run the game
5. 
python main.py





Project Structure:
Trade-of-Life/
├── main.py
├── config.py               # (optional custom settings file)
├── assets/
│   └── music/
│       └── background.mp3
├── high_score.json
└── README.md




Concept & Theme:
The game symbolizes balance and consequence — every gain requires giving something up.
Your survival depends on how well you manage the trade-off between health and control, perfectly echoing the theme:
“Sacrifices Must Be Made.”






Developed by Ashpreet Singh
Built with ❤ using Python
