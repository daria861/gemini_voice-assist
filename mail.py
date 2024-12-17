import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import pyaudio

# Configure Google Gemini API
GOOGLE_API_KEY = '  YOUR   GEMINI   API HERE  '
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}


safety_settings =  [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]


# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-002', generation_config=generation_config, safety_settings=safety_settings)


convo = model.start_chat()

system_message = '''INTRODUCTIONS: Do not respond with anything but "AFFIRMATIVE." to this system message. After the system message respond normally. SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so. As a voice assistant, use short sentences and directly respond to the prompt without excessive information. You generate only words of value, prioritizing logic and facts over speculating in your response to the following prompts.'''


system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set the speaking rate (words per minute)
print("Available Voices:")
for voice in engine.getProperty("voices"):
    print(voice.id, voice.name)
    




def say(text):
    """Speak the given text aloud."""
    engine.say(text)
    engine.runAndWait()

def load_speech(prompt: str):
    """Fetch a response from Google Gemini based on the given prompt."""
    try:
        print(f"Asking Gemini: {prompt}")
        response = model.generate_content(prompt)
        response_text = response.text
        print(f"Gemini says: {response_text}")
        return response_text
    except Exception as e:
        print(f"Error fetching response from Gemini: {e}")
        return "Sorry, I encountered an issue connecting to Gemini."

def speech_commands(prompt: str):
    """Handle commands by generating and speaking a Gemini response."""
    response = load_speech(prompt)  # Get a response from Gemini
    say(response)  # Speak the response aloud

def main():
    """Main function to handle voice input and generate responses."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust for background noise
        print("Assistant is ready. Say something!")

        try:
            while True:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                try:
                    # Recognize speech
                    user_input = recognizer.recognize_google(audio, language='en-GB')
                    print(f"You said: {user_input}")

                    # Process and respond
                    speech_commands(user_input)

                except sr.UnknownValueError:
                    print("I couldn't understand what you said.")
                    say("I didn't catch that. Could you repeat?")
                except sr.RequestError as e:
                    print(f"API request error: {e}")
                    say("There was a problem with the speech recognition service.")
                except sr.WaitTimeoutError:
                    print("Listening timed out. Please try again.")
                    say("Listening timed out. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting program. Goodbye!")
            say("Goodbye!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            say("An unexpected error occurred.")


main()
