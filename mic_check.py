import speech_recognition as sr 

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

    return response

if __name__ == '__main__': 
    r = sr.Recognizer()
    m = sr.Microphone()
    print(mic_check(r, m))