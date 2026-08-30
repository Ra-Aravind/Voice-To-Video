import speech_recognition as sr
import json
import os

# -----------------------------
# Configuration
# -----------------------------
OUTPUT_FILE = r".\input\prompt.json"

recognizer = sr.Recognizer()

print("=" * 50)
print("        VOICE TO TEXT")
print("=" * 50)

with sr.Microphone() as source:
    print("\n🎤 Speak your video prompt...")
    print("Listening...")

    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)

    print("\n📝 You said:")
    print(text)

    # Create JSON data
    data = {
        "prompt": text
    }

    # Save JSON
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("\n✅ Text saved to:")
    print(os.path.abspath(OUTPUT_FILE))

except sr.UnknownValueError:
    print("\n❌ Sorry, I could not understand you.")

except sr.RequestError as e:
    print("\n❌ Could not connect to Google Speech Recognition.")
    print(e)