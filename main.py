from openai import OpenAI
import speech_recognition as sr 
#  Run pip install pyAudio 
# pip install SpeechRecognition

def mic_check(r, microphone): 
    # When click to start, start recognising microphone
    with microphone as source: 
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=15, phrase_time_limit=15)
  
    try:
        # Recognize speech using Google Web Speech API
        response = r.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response = "API unavailable"
    except sr.UnknownValueError:
        # Speech was unintelligible
        response = "Unable to recognize speech"

    print(response + "\n")
    check_flirting(response)


def check_flirting(text):
    with open("key.txt") as key_file:
        key = key_file.read()
    
    client = OpenAI(api_key = key)

    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You are handsome Squidward from Spongebob. You are feeling humourous and edgy today, and someone is flirting with you. Respond with a short message of why you think the flirting is goo dor not"},
        {"role": "user", "content": text}
      ]
    )
    answer = completion.choices[0].message.content
    print(answer)


if __name__ == '__main__': 
    r = sr.Recognizer()
    m = sr.Microphone()
    mic_check(r, m)
 

