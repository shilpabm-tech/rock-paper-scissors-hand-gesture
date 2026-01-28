# Rock Paper Scissors – Hand Gesture Game 🎮✋

A real-time Rock Paper Scissors game built using *Python, **OpenCV, **MediaPipe, and **Pygame*.  
The player plays against the computer using *hand gestures detected via webcam*.

## 🚀 Features

- Live webcam feed using OpenCV
- Real-time hand gesture detection with MediaPipe
- Play up to *10 rounds* against the computer
- Automatic countdown (3 → 2 → 1)
- Sound effects for *win / lose / draw*
- Final winner scoreboard after 10 rounds
- Restart or exit anytime using keyboard keys


## 📁 Project Structure

rock_paper_scissors/
│
├── main.py                # Main Python file (run this)
│
├── images/                # Game images
│   ├── rock.jpeg
│   ├── paper.jpeg
│   ├── scissors.jpeg
│   ├── vs.jpeg
│   └── bg.jpeg
│
├── sounds/                # Sound effects
│   ├── win.wav
│   ├── lose.wav
│   └── draw.wav
│
├── runs/                  # Auto-generated prediction files
│
└── README.md              # Project documentation

## 🛠️ How to Run the Project

### Prerequisites
Make sure Python 3.9 or above is installed.

Install the required libraries:
```bash
pip install opencv-python mediapipe pygame
### Run the Game
```bash
python main.py