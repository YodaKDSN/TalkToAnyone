import tkinter as tk
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

recognizer = sr.Recognizer()
translator = Translator()

# Function for handling the Speak button click event
def speak_user1():
    language_user1 = entry_user1.get()
    print(f"User1 wants to speak in: {language_user1}")
    return language_user1

def speak_user2():
    language_user2 = entry_user2.get()
    print(f"User2 wants to speak in: {language_user2}")
    return language_user2

is_speaking = True

def listen_for_speech(language):
    """
    Listen for speech and return transcribed text.
    Stops if 'is_speaking' becomes False.
    """
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        global is_speaking
        is_speaking = True  # Reset flag to True when starting to listen

        while is_speaking:  # Check if the user is still speaking
                print("Listening for speech... Please speak now.")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language=language)
                print(f"Recognized: {text}")
                if "over" in text.lower():
                    print("Word 'over' detected, stopping the listening.")
                    is_speaking = False  # Stop listening when "over" is heard
                return text  # Return the transcribed text

def translate_text(text, target_lang):
    translated = translator.translate(text, dest=target_lang)
    return translated.text

def speak_text(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("translated_audio.mp3")
    os.system("start translated_audio.mp3")  

def User1_speech():
    language_user1 = speak_user1()  # Get User1's language
    User1_text = listen_for_speech(language=language_user1)
    if User1_text:
        User1_translation = translate_text(User1_text, speak_user2())  # Translate to User2's language
        speak_text(User1_translation, speak_user2())  # Speak the translated text

def User2_speech():
    language_user2 = speak_user2()  # Get User2's language
    User2_text = listen_for_speech(language=language_user2)
    if User2_text:
        User2_translation = translate_text(User2_text, speak_user1())  # Translate to User1's language
        speak_text(User2_translation, speak_user1())  # Speak the translated text    

# Create the main window
root = tk.Tk()
root.title("Language Speak App")

# User1 section
frame_user1 = tk.Frame(root)
frame_user1.pack(pady=10, padx=10, fill="x")

label_user1 = tk.Label(frame_user1, text="User1")
label_user1.grid(row=0, column=0, padx=10, pady=5)

label_language_user1 = tk.Label(frame_user1, text="Language:")
label_language_user1.grid(row=1, column=0, padx=10, pady=5)

entry_user1 = tk.Entry(frame_user1)
entry_user1.grid(row=1, column=1, padx=10, pady=5)

button_enter_user1 = tk.Button(frame_user1, text="Enter", command=speak_user1)
button_enter_user1.grid(row=1, column=2, padx=10, pady=5)

button_speak_user1 = tk.Button(frame_user1, text="Speak", command=User1_speech)
button_speak_user1.grid(row=1, column=3, padx=10, pady=5)

# User2 section
frame_user2 = tk.Frame(root)
frame_user2.pack(pady=10, padx=10, fill="x")

label_user2 = tk.Label(frame_user2, text="User2")
label_user2.grid(row=0, column=0, padx=10, pady=5)

label_language_user2 = tk.Label(frame_user2, text="Language:")
label_language_user2.grid(row=1, column=0, padx=10, pady=5)

entry_user2 = tk.Entry(frame_user2)
entry_user2.grid(row=1, column=1, padx=10, pady=5)

button_enter_user2 = tk.Button(frame_user2, text="Enter", command=speak_user2)
button_enter_user2.grid(row=1, column=2, padx=10, pady=5)

button_speak_user2 = tk.Button(frame_user2, text="Speak", command=User2_speech)
button_speak_user2.grid(row=1, column=3, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()