import cv2
import mediapipe as mp
import random
import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load sounds
win_sound = pygame.mixer.Sound("sounds/win.wav")
lose_sound = pygame.mixer.Sound("sounds/lose.wav")
draw_sound = pygame.mixer.Sound("sounds/draw.wav")

# Load images
rock_img = cv2.imread("images/rock.jpeg")
paper_img = cv2.imread("images/paper.jpeg")
scissors_img = cv2.imread("images/scissors.jpeg")
vs_img = cv2.imread("images/vs.jpeg")
bg = cv2.imread("images/bg.jpeg")

# Resize images
rock_img = cv2.resize(rock_img, (200, 200))
paper_img = cv2.resize(paper_img, (200, 200))
scissors_img = cv2.resize(scissors_img, (200, 200))
vs_img = cv2.resize(vs_img, (200, 200))
bg = cv2.resize(bg, (900, 600))

choices = ["rock", "paper", "scissors"]

# SCORE
user_score = 0
computer_score = 0
round_count = 0
MAX_ROUNDS = 10

# Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def detect_gesture(lm):
    finger_tips = [8, 12, 16, 20]
    fingers = [(1 if lm[tip].y < lm[tip - 2].y else 0) for tip in finger_tips]

    if fingers == [0, 0, 0, 0]:
        return "rock"
    if fingers == [1, 1, 1, 1]:
        return "paper"
    if fingers[:2] == [1, 1] and fingers[2:] == [0, 0]:
        return "scissors"
    return None

cap = cv2.VideoCapture(0)

while True:

    # ---------------------------------------------
    # LIVE GAME LOOP
    # ---------------------------------------------
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    display = bg.copy()

    # Live webcam
    display[300:500, 50:250] = cv2.resize(frame, (200, 200))

    # Scoreboard
    cv2.putText(display, f"YOU: {user_score}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(display, f"COMPUTER: {computer_score}", (600, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 200, 255), 3)
    cv2.putText(display, f"Round: {round_count}/{MAX_ROUNDS}", (330, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    cv2.putText(display, "SPACE = Play   R = Restart   ESC = Exit",
                (180, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    cv2.imshow("Rock Paper Scissors", display)

    key = cv2.waitKey(1)

    # ⭐ EXIT ANYTIME
    if key == 27:
        break

    # ⭐ RESTART ANYTIME
    if key in [ord('r'), ord('R')]:
        user_score = 0
        computer_score = 0
        round_count = 0
        continue

    # ---------------------------------------------
    # SPACE → START COUNTDOWN
    # ---------------------------------------------
    if key == 32:

        # COUNTDOWN
        for c in [3, 2, 1]:
            temp = bg.copy()
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            temp[300:500, 50:250] = cv2.resize(frame, (200, 200))

            cv2.putText(temp, str(c), (420, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10)

            cv2.putText(temp, "Press R = Restart | ESC = Exit", (200, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

            cv2.imshow("Rock Paper Scissors", temp)
            k2 = cv2.waitKey(1000)

            # ⭐ Restart/Exit DURING countdown
            if k2 == 27:
                cap.release()
                cv2.destroyAllWindows()
                exit()

            if k2 in [ord('r'), ord('R')]:
                user_score = 0
                computer_score = 0
                round_count = 0
                break  # restart immediately


        # CAPTURE image after countdown
        ret, frozen = cap.read()
        frozen = cv2.flip(frozen, 1)

        rgb = cv2.cvtColor(frozen, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        gesture = None

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0].landmark
            gesture = detect_gesture(lm)

            mp_draw.draw_landmarks(
                frozen, result.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0,255,0), thickness=2),
                mp_draw.DrawingSpec(color=(0,0,255), thickness=2)
            )

        if gesture is None:
            gesture = "unknown"

        computer = random.choice(choices)

        # RESULT SCREEN
        game = bg.copy()
        game[300:500, 50:250] = cv2.resize(frozen, (200, 200))
        game[300:500, 350:550] = vs_img

        if computer == "rock":
            game[300:500, 650:850] = rock_img
        elif computer == "paper":
            game[300:500, 650:850] = paper_img
        else:
            game[300:500, 650:850] = scissors_img

        # DECIDE WINNER
        if gesture == computer:
            result_text = "DRAW"
            draw_sound.play()
        elif (gesture == "rock" and computer == "scissors") or \
             (gesture == "paper" and computer == "rock") or \
             (gesture == "scissors" and computer == "paper"):
            result_text = "YOU WIN!"
            user_score += 1
            win_sound.play()
        else:
            result_text = "YOU LOSE!"
            computer_score += 1
            lose_sound.play()

        round_count += 1

        cv2.putText(game, result_text, (220, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 6)

        cv2.putText(game, "Press R = Restart | ESC = Exit", (200, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

        cv2.imshow("Rock Paper Scissors", game)

        # ⭐ ALLOW EXIT/RESTART DURING RESULT SCREEN
        k3 = cv2.waitKey(2500)

        if k3 == 27:
            break

        if k3 in [ord('r'), ord('R')]:
            user_score = 0
            computer_score = 0
            round_count = 0
            continue


cap.release()
cv2.destroyAllWindows()