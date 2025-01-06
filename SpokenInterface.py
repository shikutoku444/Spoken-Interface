import speech_recognition as sr
import webbrowser
import os
import pywhatkit
import urllib.parse
import psutil  # Library to handle system processes
import pyautogui  # Library to simulate keyboard shortcuts
import datetime
import random
import time  # To add delays if needed

# Speech Recognition Function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        speak_text("Waiting for your command.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak_text("Sorry, I didn't understand. Could you please repeat?")
            return None
        except sr.RequestError:
            speak_text("Sorry, my speech service is currently down.")
            return None
        except sr.WaitTimeoutError:
            speak_text("Listening timed out. Please try again.")
            return None

# Text-to-Speech Function using macOS say command
def speak_text(text):
    safe_text = text.replace("'", "\\'").replace('"', '\\"')
    os.system(f'say "{safe_text}"')

# Function to get the current time
def get_current_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    time_responses = [
        f"The current time is {now}.",
        f"It's {now}. Don't let time fly away",
        f"Right now, it's {now} ."
    ]
    return random.choice(time_responses)

# Function to open applications and websites
def open_application(command):
    if "open youtube" in command.lower():
        speak_text("Opening YouTube for you. Enjoy exploring!")
        webbrowser.open("https://www.youtube.com")
    elif "play" in command.lower() and "youtube" in command.lower():
        song = command.lower().replace("play", "").replace("youtube", "").strip()
        if song:
            speak_text(f"Let's listen to {song} on YouTube. Enjoy the music!")
            pywhatkit.playonyt(song)
        else:
            speak_text("Which song would you like me to play?")
    elif "open gazebo" in command.lower():
        speak_text("Opening Gazebo simulation environment")
        webbrowser.open("https://gazebosim.org/home")
    elif "open chatgpt" in command.lower():
        speak_text("Opening ChatGPT. Happy learning!")
        webbrowser.open("https://chat.openai.com")
    elif "webots" in command.lower():
        speak_text("Opening Webots. Let's look around this simulation environment?")
        os.system("open -a Webots")
    elif "matlab" in command.lower():
        speak_text("Opening MATLAB. Let's see the MATLAB AI assistant?")
        os.system("open -a MATLAB")
    else:
        speak_text("I'm not sure how to open that application or website, sorry!")

# Function to bring YouTube window to the front
def focus_youtube():
    for proc in psutil.process_iter():
        if proc.name() in ["Google Chrome", "firefox", "Microsoft Edge", "Safari"]:
            for cmdline in proc.cmdline():
                if "youtube" in cmdline.lower():
                    if proc.name() == "Google Chrome":
                        os.system("open -a 'Google Chrome'")
                    elif proc.name() == "firefox":
                        os.system("open -a 'firefox'")
                    elif proc.name() == "Microsoft Edge":
                        os.system("open -a 'Microsoft Edge'")
                    elif proc.name() == "Safari":
                        os.system("open -a 'Safari'")
                    return True
    return False

# Function to control YouTube playback
def control_youtube(command):
    if focus_youtube():
        if "pause youtube" in command.lower():
            speak_text("Pausing YouTube playback.")
            pyautogui.press("k")  # 'k' is the shortcut key to play/pause on YouTube
        elif "play youtube" in command.lower():
            speak_text("Resuming YouTube playback.")
            pyautogui.press("k")  # 'k' is the shortcut key to play/pause on YouTube
        elif "next youtube" in command.lower():
            speak_text("Skipping to the next video on YouTube.")
            pyautogui.press("shift+n")  # 'Shift+N' is the shortcut key to play the next video on YouTube
    else:
        speak_text("No active YouTube window found.")

# Function to close YouTube browser tabs
def close_youtube():
    for proc in psutil.process_iter():
        if proc.name() in ["Google Chrome", "firefox", "Microsoft Edge", "Safari"]:
            if "youtube" in proc.cmdline().lower():
                proc.terminate()
    speak_text("YouTube tabs have been closed.")

# Function to close all browser tabs
def close_browsers():
    for proc in psutil.process_iter():
        if proc.name() in ["Google Chrome", "firefox", "Microsoft Edge", "Safari"]:
            proc.terminate()
    speak_text("All browser tabs have been closed.")

# Function to handle the intro and listening
def intro():
    intros = [
        "Hi there! I'm Nini, your AI assistant. How can I help you today?",
        "Hello! I'm Nini, ready to assist you. What would you like to do?"
    ]
    speak_text(random.choice(intros))

def listen_and_respond():
    while True:
        print("Waiting for wake word...")
        command = recognize_speech()
        if command and "nini" in command.lower():
            print("Wake word detected!")
            intro()
            time.sleep(1)  # Add a short delay before processing the next command
            command = recognize_speech()
            if command:
                process_command(command)

def process_command(command):
    greetings = ["hi", "hello", "hey"]
    if any(greeting in command.lower() for greeting in greetings):
        speak_text("Hello! I'm Nini, your AI assistant. How can I help you today?")
    elif "how are you" in command.lower():
        responses = [
            "I'm doing great! How can I assist you today?",
            "I'm happy and ready to help! How are you?",
            "Good, thank you! What can I help you with?"
        ]
        speak_text(random.choice(responses))
    elif "time" in command.lower():
        current_time = get_current_time()
        speak_text(current_time)
    elif "thank you" in command.lower():
        thank_responses = [
            "You're welcome! Happy to help.",
            "No problem at all!",
            "Anytime! Glad I could be useful."
        ]
        speak_text(random.choice(thank_responses))
    elif "exit" in command.lower():
        speak_text("Goodbye! Have a great day!")
        os._exit(0)
    elif "stop youtube" in command.lower():
        close_youtube()
    elif any(playback in command.lower() for playback in ["pause youtube", "play youtube", "next youtube"]):
        control_youtube(command)
    else:
        open_application(command)

if __name__ == "__main__":
    listen_and_respond()
