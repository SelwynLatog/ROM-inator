## ROM-inator

# ROM-inator is a computer vision–based workout engine that tracks reps, form, and fatigue in real time. Not just rep counting — 

it measures concentric & eccentric durations, form integrity, and fatigue per rep and set. 
Think of it as a workout logger that actually understands effort… and yells at you when you perform shitty reps.

Built by a fitness and exercise science nerd who happens to program, and is just tired of manual workout logging and shitty fitness apps.

What It Does

ROM-inator uses webcam or video input via MediaPipe pose detection to give you:

Rep counting — full reps only, via a cycle-based state machine
Concentric & eccentric timing — per rep, per set
Form validation — torso lean, tempo, depth
Fatigue profiling — detects slowdown and eccentric collapse
Session logging — saved to JSON with per-rep and per-set breakdown
Audio feedback — optional “angry trainer in your pocket”

# Supported Movements

| Exercise | Camera Position          | Notes                    |
| -------- | ------------------------ | ------------------------ |
| Squat    | Portrait, front-facing   | Knee angle tracking      |
| Push-up  | Landscape, side-on floor | Elbow & body alignment   |
| Pull-up  | Portrait, front-facing   | Bar calibration required |

# Requirements
Python 3.10+
MediaPipe
OpenCV
pygame

# Installation

git clone https://github.com/SelwynLatog/ROM-inator

cd ROM-inator

python -m venv venv

venv\Scripts\activate        # Windows

source venv/bin/activate     # Mac/Linux

pip install mediapipe opencv-python pygame


# Model
Download the MediaPipe pose landmarker model and place it here:
src/pose_landmarker.task

# Run
python main.py

Sample Outputs:

<img width="1558" height="1048" alt="image" src="https://github.com/user-attachments/assets/cf503a5f-a447-4b95-86f9-a4f5206d0f50" />


<img width="614" height="718" alt="image" src="https://github.com/user-attachments/assets/5c7ad5ff-3b25-4660-8697-cda653d6927c" />


<img width="1472" height="1022" alt="image" src="https://github.com/user-attachments/assets/ddaf06ba-56ba-4a50-9dc5-8ae228539a5f" />


<img width="560" height="360" alt="image" src="https://github.com/user-attachments/assets/c061e894-f155-47e6-8bc2-093791a29218" />


sample of shitty crossfit butterfly pull ups purposely being flagged for swaying like a monkey

<img width="1413" height="1027" alt="image" src="https://github.com/user-attachments/assets/6cb0c8be-d076-4739-8ffb-ffd5417afdc6" />

<img width="576" height="448" alt="image" src="https://github.com/user-attachments/assets/dffea0f0-6ba1-416d-843a-46af5dee4bfe" />

<img width="1679" height="926" alt="image" src="https://github.com/user-attachments/assets/e9f25884-8252-4c46-8786-508272da7ece" />


<img width="597" height="459" alt="image" src="https://github.com/user-attachments/assets/f8c38034-e229-4d22-b90e-4634dda2fe83" />

# Roadmap (V2)
Mobile deployment — portrait/landscape auto-detect, touch UI

*Auto exercise maker — record 5 demo reps, engine sets thresholds automatically

*Per-user calibration — adjust for body type & limb length

*Training style modes — strength, hypertrophy, endurance

*Session history UI — charts, effort trends, set comparisons

*MORE EXERCISES! HELL YEAH

# Goal: A fitness app that understands your effort. Not a fucking shitty app with pre hardcoded workouts.

Built With

Python

MediaPipe — pose landmark detection

OpenCV — video processing & display

pygame — audio feedback

Mobile app wip so I can actually take it on my workouts. Coming soon...(hopefully)
