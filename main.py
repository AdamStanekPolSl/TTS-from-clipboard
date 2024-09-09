# This is sample app, that read (text to speech) every new text that come to clipboard

import pyttsx3
import pyperclip
import time
import psutil
import keyboard
import sys
import os


debugging = True


def debugPrint(text):
    if debugging:
        print(text)

def getProcess(processName):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == processName:
            debugPrint(f"Found process: {processName} (PID: {proc.info['pid']})")
            return proc
    debugPrint(f"Process {processName} not found.")
    return None        

def freezeProcess(proc):
    time.sleep(0.3)
    try:    
        debugPrint(f"Freezing process: {proc.info['name']} (PID: {proc.info['pid']})")
        proc.suspend()  # Suspend (freeze) the process
    except:
        debugPrint(f'Cannot freeze proccess.')

def unfreezeProcess(proc):
    try:
        debugPrint(f"Unfreezing process: {proc.name()} (PID: {proc.pid})")
        proc.resume()  # Resume (unfreeze) the process
    except:
        debugPrint(f'Cannot unfreeze proccess.')

# refactor needed
def onHotKeyUnfreeze(proc):
    if proc.status() == 'stopped':
        unfreezeProcess(proc)
    else:
        keyboard.press_and_release('esc')

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


def monitorClipboard(gameProcess):
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

            unfreezeProcess(gameProcess)

        time.sleep(1)



if __name__ == '__main__':
    gameProc=getProcess(os.path.relpath(sys.argv[1], os.path.dirname(os.path.abspath(__file__))))
    keyboard.add_hotkey('shift+win+t', lambda: freezeProcess(gameProc))
    keyboard.add_hotkey('esc', lambda: unfreezeProcess(gameProc), suppress=False)

    engine = pyttsx3.init()
    engine.setProperty('voice', 'pl')
    engine.setProperty('rate', 170)

    monitorClipboard(gameProc)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
