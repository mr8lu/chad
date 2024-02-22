import subprocess


def send_text(msg, chat_room):
    script = f'''
    tell application "Messages"
    set chatFound to false
    set chatNameToFind to "{chat_room}"
    set myMessage to "Chad: {msg}"

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
    result = subprocess.run(["osascript", '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return True
    else:
        return False
