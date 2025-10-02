# Rock Paper Scissors Game Collection

This project contains two interactive Rock Paper Scissors games:
- **RockPaperScissors.html**: Play in your browser against an AI, using buttons.
- **rock_paper_scissors_hand.py**: Play using hand gestures recognized via webcam, with a graphical interface (Tkinter), against an AI.

---

## 1. RockPaperScissors.html

**Type:** Web browser game  
**Tech:** HTML, CSS, JavaScript  
**Features:**
- Play against AI in 3 rounds.
- Click buttons to choose Rock, Paper, or Scissors.
- See your choice, AI's choice, round results, and score.
- "Restart" button to play again.
- No installation needed.

**How to Run:**
1. Download or copy `RockPaperScissors.html` onto your computer.
2. Double-click the file, or open it in any web browser (Chrome, Firefox, Edge, etc.).
3. Play directly!

---

## 2. rock_paper_scissors_hand.py

**Type:** Desktop application (Python/Tkinter)  
**Tech:** Python, OpenCV, MediaPipe, Pillow, Tkinter  
**Features:**
- Play against AI in 3 rounds using your hand gestures (rock, paper, scissors) captured by your webcam.
- Countdown timer before each round.
- AI choice, your detected gesture, scores, results, and round info displayed *separately* from the webcam image.
- "Play Again" button to restart the game without closing the app.
- All game info/text is displayed in the right panel, webcam video on the left.

**How to Run:**
1. Make sure you have Python **3.10 or 3.11** installed.
2. Install dependencies in your terminal:
   ```bash
   pip install opencv-python mediapipe pillow
   ```
3. Download/copy `rock_paper_scissors_hand.py` to your computer.
4. Run:
   ```bash
   python rock_paper_scissors_hand.py
   ```
5. In the window, click **Start Game**. Show your hand gesture to the webcam when prompted.
6. After 3 rounds, see the winner and points. Click **Play Again** to replay.

---

## Troubleshooting

- **rock_paper_scissors_hand.py** requires a working webcam.
- If you get errors about versions, check you are using Python 3.10/3.11 (not 3.12).
- If the webcam is not detected, check app permissions, and try restarting.
- If MediaPipe or Pillow is missing, install them with pip.

---

## Customization

- To change the number of rounds, adjust the `rounds` variable in each file.
- To change the UI, modify the HTML/CSS/JS in `RockPaperScissors.html` or the Tkinter layout in `rock_paper_scissors_hand.py`.

---

## License

Free for educational, club, or non-commercial use.  
Feel free to adapt and share!
