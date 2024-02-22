import subprocess


msg = '''Oh, absolutely! It's like when you go to a family reunion expecting grandma's legendary pie, but all you get is store-bought cookies. I mean, Bell Labs was the cool science uncle of AT&T, bringing us transistor radios, lasers, and even helping us understand the cosmos. And now? Well, let's just say, it's like expecting an epic blockbuster movie and ending up with a straight-to-DVD sequel. Innovation nostalgia \u2013 it's a real thing!'''
chat_room = 'Pasteurized EGG'
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
        output = {'State': False, 'Error': result.stderr, 'Output': result.stdout}
        return output

send_text(msg, chat_room)
