import cv2
import mediapipe as mp
import random
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk

GESTURE_LABELS = {0: 'Rock', 1: 'Paper', 2: 'Scissors'}
GESTURE_EMOJIS = {0: '✊', 1: '🖐️', 2: '✌️'}

user_score = 0
ai_score = 0
rounds = 3
current_round = 1

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def classify_gesture(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1,5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    if sum(fingers[1:]) == 0:
        return 0
    elif sum(fingers[1:]) == 4:
        return 1
    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        return 2
    return None

def determine_winner(user, ai):
    if user == ai:
        return "draw"
    elif (user == 0 and ai == 2) or (user == 1 and ai == 0) or (user == 2 and ai == 1):
        return "win"
    else:
        return "lose"

class RPSGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Rock Paper Scissors - Hand Gesture vs AI")
        self.master.geometry("950x600")
        self.video_frame = tk.Label(master)
        self.video_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.round_label = tk.Label(self.info_frame, text="", font=("Arial", 18))
        self.round_label.pack(pady=10)
        self.score_label = tk.Label(self.info_frame, text="", font=("Arial", 16))
        self.score_label.pack(pady=10)
        self.ai_label = tk.Label(self.info_frame, text="", font=("Arial", 16))
        self.ai_label.pack(pady=10)
        self.user_label = tk.Label(self.info_frame, text="", font=("Arial", 16))
        self.user_label.pack(pady=10)
        self.result_label = tk.Label(self.info_frame, text="", font=("Arial", 18, "bold"))
        self.result_label.pack(pady=20)
        self.final_label = tk.Label(self.info_frame, text="", font=("Arial", 20, "bold"), fg="green")
        self.final_label.pack(pady=20)
        self.start_button = tk.Button(self.info_frame, text="Start Game", font=("Arial", 16), command=self.start_game)
        self.start_button.pack(pady=30)
        self.replay_button = tk.Button(self.info_frame, text="Play Again", font=("Arial", 16), command=self.replay_game, state=tk.DISABLED)
        self.replay_button.pack(pady=5)
        self.running = False

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        self.replay_button.config(state=tk.DISABLED)
        threading.Thread(target=self.game_loop, daemon=True).start()

    def replay_game(self):
        # Reset scores and round, re-enable start button
        global user_score, ai_score, current_round
        user_score = 0
        ai_score = 0
        current_round = 1
        self.final_label.config(text="")
        self.result_label.config(text="")
        self.ai_label.config(text="")
        self.user_label.config(text="")
        self.start_game()

    def game_loop(self):
        global user_score, ai_score, current_round
        user_score = 0
        ai_score = 0
        current_round = 1
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.final_label.config(text="")
        self.running = True

        while current_round <= rounds and self.running:
            # Countdown
            for count in [3,2,1]:
                ret, frame = cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)
                self.show_frame(frame)
                self.update_info(f"Round: {current_round}/{rounds}", f"Your Score: {user_score} | AI Score: {ai_score}", "", "", f"Get ready: {count}")
                time.sleep(0.7)
            self.update_info(f"Round: {current_round}/{rounds}", f"Your Score: {user_score} | AI Score: {ai_score}", "", "", "GO!")
            time.sleep(0.7)
            # Detect hand for 5 seconds max
            gesture = None
            start_time = time.time()
            detected = False
            ai_choice = random.randint(0,2)
            while time.time() - start_time < 5 and self.running:
                ret, frame = cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        gesture = classify_gesture(hand_landmarks)
                self.show_frame(frame)
                self.update_info(
                    f"Round: {current_round}/{rounds}",
                    f"Your Score: {user_score} | AI Score: {ai_score}",
                    f"AI Choice: {GESTURE_LABELS[ai_choice]} {GESTURE_EMOJIS[ai_choice]}",
                    f"Your gesture: {GESTURE_LABELS[gesture]+' '+GESTURE_EMOJIS[gesture] if gesture is not None else '-'}",
                    "Show your hand! ✊ 🖐️ ✌️"
                )
                if gesture is not None:
                    detected = True
                    break
                self.master.update()
            # Show result
            if detected:
                round_result = determine_winner(gesture, ai_choice)
                if round_result == "win":
                    user_score += 1
                    ai_score -= 1
                    result_msg = "✅ You win this round!"
                elif round_result == "lose":
                    user_score -= 1
                    ai_score += 1
                    result_msg = "❌ AI wins this round!"
                else:
                    result_msg = "🤝 Draw!"
            else:
                result_msg = "No gesture detected! Try again."
            self.update_info(
                f"Round: {current_round}/{rounds}",
                f"Your Score: {user_score} | AI Score: {ai_score}",
                f"AI Choice: {GESTURE_LABELS[ai_choice]} {GESTURE_EMOJIS[ai_choice]}",
                f"Your gesture: {GESTURE_LABELS[gesture]+' '+GESTURE_EMOJIS[gesture] if gesture is not None else '-'}",
                result_msg
            )
            time.sleep(2)
            current_round += 1

        # Final result
        if user_score > ai_score:
            final_msg = "🏆 YOU WIN against AI!"
        elif user_score < ai_score:
            final_msg = "😎 AI wins! Try again!"
        else:
            final_msg = "🤝 It's a DRAW!"
        self.final_label.config(text=final_msg)
        self.running = False
        cap.release()
        self.replay_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)

    def show_frame(self, frame):
        if frame is not None:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)

    def update_info(self, round_text, score_text, ai_text, user_text, result_text):
        self.round_label.config(text=round_text)
        self.score_label.config(text=score_text)
        self.ai_label.config(text=ai_text)
        self.user_label.config(text=user_text)
        self.result_label.config(text=result_text)
        self.master.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()