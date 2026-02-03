import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
import musicLibrary
import requests
# from AppOpener import open, close

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "your api key"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_website(url):
    webbrowser.open(url)

def search(query, platform):
    formatted_query = "+".join(query.lower().split(" ")[1:])
    base_urls = {
        "google": "https://www.google.com/search?q=",
        "youtube": "https://www.youtube.com/results?search_query="
    }
    if platform in base_urls:
        open_website(base_urls[platform] + formatted_query)
    else:
        speak(f"Unknown platform: {platform}")
        speak(f"Would you like to google {platform}, Sir?")

def play_song(song):
    if song in musicLibrary:
        open_website(musicLibrary[song])
    else:
        search(song, "youtube")

def fetch_news():
    """Fetch and speak news headlines."""
    try:
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        response.raise_for_status()
        articles = response.json().get('articles', [])
        for article in articles[:5]:  # Limit to top 5 articles
            print(article['title'])
            speak(article['title'])
    except requests.RequestException as e:
        speak("Failed to fetch news:")
        print(e)

def print_instructions():
    instructions = [
        "1. To activate Jarvis, say 'Jarvis'.",
        "2. Play music by saying 'play' followed by the song name.",
        "3. Open websites. If not recognized, Jarvis can Google it.",
        "4. Search Google or YouTube by saying 'google' or 'youtube' followed by your query.",
        "5. Hear the top 5 news headlines by including 'news' in your command.",
        "6. Exit by saying 'shutdown', 'quit', or 'exit'."
    ]
    print("\nPlease read the instructions for a better experience:")
    for line in instructions:
        print(line)

def listen(timeout=2, phrase_time_limit=2):
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def processCommand(c):
    command = c.lower()
    print(f"\nYou: {c}\n")

    # Define command handlers
    commands = {
        "open google": lambda: open_website("https://www.google.com"),
        "open youtube": lambda: open_website("https://www.youtube.com"),
        "open type racer": lambda: open_website("https://www.typeracer.com"),
        "open nitro type": lambda: open_website("https://www.nitrotype.com"),
        "open chatgpt": lambda: open_website("https://www.chatgpt.com"),
        "open gemini": lambda: open_website("https://www.gemini.google.com"),
        "open gencraft": lambda: open_website("https://www.gencraft.com"),
        "open invideo": lambda: open_website("https://www.invideo.io"),
        "news": fetch_news,
        "shutdown": lambda: (speak("Thanks Sir, Have a nice time ahead!"), sys.exit())
    }

    # Checking the commad
    for key, action in commands.items():
        if command.startswith(key):
            action()
            return

    if command.startswith("google "):
        search(command[7:], "google")
    elif command.startswith("youtube "):
        search(command[8:], "youtube")
    elif command.startswith("play "):
        play_song(command[5:])
    else:
        speak("Command not recognized.")

def main():
    speak("Initializing Jarvis...")
    print_instructions()

    while True:
        recognizer.energy_threshold = 50

        wake_word = listen(timeout=2, phrase_time_limit=1)

        if wake_word == "jarvis":
            print("\nJarvis Activated.\n")
            speak("Ya")

            # Listen for the command
            command = listen()
            if command:
                processCommand(command)

        elif wake_word in ["quit", "exit", "shutdown"]:
            speak("Thanks Sir, Have a nice time ahead!")
            sys.exit()



if __name__ == "__main__":
    recognizer = sr.Recognizer()
    main()
