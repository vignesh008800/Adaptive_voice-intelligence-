import speech_recognition as sr
import pyttsx3
import time

# Simulated appliance states
appliances = {
    "light": False,
    "fan": False,
    "tv": False
}

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except:
            speak("Sorry, I didn't catch that.")
            return ""

def control_appliance(command):
    global appliances

    for device in appliances.keys():
        if f"turn on {device}" in command or f"switch on {device}" in command:
            if not appliances[device]:
                appliances[device] = True
                speak(f"{device.capitalize()} turned on.")
            else:
                speak(f"{device.capitalize()} is already on.")
            return
        elif f"turn off {device}" in command or f"switch off {device}" in command:
            if appliances[device]:
                appliances[device] = False
                speak(f"{device.capitalize()} turned off.")
            else:
                speak(f"{device.capitalize()} is already off.")
            return

    if "status" in command:
        for dev, state in appliances.items():
            speak(f"{dev.capitalize()} is {'on' if state else 'off'}.")
        return

    if "exit" in command or "stop" in command:
        speak("Goodbye! Shutting down the home assistant.")
        return False

    speak("I didn't understand the command.")
    return True

# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":
    speak("Welcome! I am your home assistant.")
    speak("You can say commands like 'Turn on the light' or 'Switch off the fan'.")
    speak("Say 'status' to check appliances, or 'exit' to stop.")

    while True:
        command = listen()
        if not command:
            continue
        should_continue = control_appliance(command)
        if should_continue is False:
            break
        time.sleep(1)
    
