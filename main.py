from logging.config import stopListening

import speech_recognition
from commands import Status

speech = ""
statusManager = Status()
def listnerCallback(recognizer, audio):
    global speech
    try:
        statusManager.state = "Parsing"
        audio = recognizer.recognize_sphinx(audio)
        speech = audio
    except speech_recognition.UnknownValueError:
        print("Sorry, could not understand audio")
    except speech_recognition.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))


rec = speech_recognition.Recognizer()
mic = speech_recognition.Microphone()

with mic as source:
    rec.adjust_for_ambient_noise(source)

stop = rec.listen_in_background(mic, listnerCallback)
stopRunning = False

if __name__ == "__main__":
    try:
        while statusManager.running:
            if speech:
                if "exit" in speech:
                    statusManager.state = "Exiting"
                    statusManager.running = False
                if "assistant" in speech and statusManager.running and not( "stop" in speech or "cancel" in speech):
                    statusManager.detectCommands(speech)
                speech = ""
    except KeyboardInterrupt:
        stopRunning = True
    stop()






