import subprocess


def send_imessage(contact, message):
    script = f'''tell application "Messages" to send "{message}" to buddy "{contact}" of (service 1 whose service type is iMessage)'''
    subprocess.run(["osascript", "-e", script])


# send_imessage('chat311459657259427244', 'good morning, this is Chad@alpha-release')


def last_5(input):
    script = f'''
    tell application "Messages"
    set chatFound to false
    set chatNameToFind to "Pasteurized EGG"
    set myMessage to "Chad: {input}"

    repeat with aChat in every chat
        if name of aChat is chatNameToFind then
            set chatFound to true
            send myMessage to aChat
            exit repeat
        end if
    end repeat

    if not chatFound then
        display dialog "Chat named '" & chatNameToFind & "' not found."
    end if
    end tell
'''
    subprocess.run(["osascript", '-e', scriptNew])

text = '''Chad: Did I break the egg again?'''
last_5(text)
