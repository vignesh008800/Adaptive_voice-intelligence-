import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slower speaking rate for elderly
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice, can change to [0] for male

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good morning! How can I help you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon! What would you like to do?")
    else:
        speak("Good evening! How can I assist you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""

def handle_query(query):
    if "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "your name" in query:
        speak("I am your assistant, here to help you.")
    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "thank you" in query or "thanks" in query:
        speak("You're welcome! I'm always here to help.")
    elif "stop" in query or "exit" in query:
        speak("Goodbye! Take care.")
        return False
    else:
        speak("Sorry, I can't help with that yet.")
    return True

# ----------- MAIN FUNCTION -----------
if __name__ == "__main__":
    wish_user()
    while True:
        query = take_command()
        if not query:
            continue
        if not handle_query(query):
            break
