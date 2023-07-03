# This is sample app, that read (text to speech) every new text that come to clipboard

import pyttsx3
import pyperclip
import time


debugging = False


def debugPrint(text):
    if debugging:
        print(text)


def removeNewlines(text):
    debugPrint("Text is cutted for lines.")
    lines = list(filter(None, text.split('\n')))
    debugPrint(lines)
    toReturn = []
    i = 0

    while len(lines)-1 > i:
        debugPrint(f'i = {i}')

        if lines[i+1][0].islower():
            debugPrint(f'Line {lines[i+1]} starts with lowercase. Newline persisted.')
            toReturn.append(lines[i].rstrip())
        else:
            debugPrint(f'Line {lines[i+1]} starts with uppercase. No newline.')
            toReturn.append(lines[i])

        i += 1

    toReturn.append(lines[i])
    finalText = ' '.join(toReturn)
    debugPrint(f'This is final text:\n{finalText}')

    return finalText


def tts(text):
    print("Hello from TTS function. Starting the speech...")

    toSay = removeNewlines(text)
    engine.say(toSay)
    engine.runAndWait()


def monitorClipboard():
    oldText = pyperclip.paste()
    debugPrint(f"Old text is:\n{oldText}")

    while True:
        text = pyperclip.paste()
        debugPrint(f"New text is:\n{text}")

        if text != oldText:
            debugPrint("New text differs. It will be said...")
            tts(text)
            oldText = text
            debugPrint(f"Now the old text is:\n{oldText}")

        time.sleep(1)



if __name__ == '__main__':
    engine = pyttsx3.init()
    engine.setProperty('voice', 'pl')
    engine.setProperty('rate', 170)

    monitorClipboard()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
