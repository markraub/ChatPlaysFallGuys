import socket
import time
import keyboard
import operator

client_id = ''
oauth = ''
server = 'irc.chat.twitch.tv'
port = 6667
nickname = ''
channel = ''
sock = socket.socket()





class ScoreBoard:
    def __init__(self, Scores, winner, inputs):
        self.Scores = Scores
        self.winner = winner
        self.inputs = inputs
    def reset_score(self):
        self.Scores = {
    'w':[],
    'a':[],
    's':[],
    'd':[],
    'space':[],
    'ctrl':[],
    'shift':[],
    'esc':[],
    }

Scores = ScoreBoard(
    {
    'w':[],
    'a':[],
    's':[],
    'd':[],
    'space':[],
    'ctrl':[],
    'shift':[],
    'esc':[],
    },
    "",
    [],
    )

class Timer:
    def __init__(self, start, now):
        self.start = start
        self.now = now

def get_message(resp):
    user = resp[0]
    message = resp[1]
    if "w" == message.lower() or "forward" in message.lower():
        Scores.Scores['w'].append(user)
        
    elif "a" == message.lower() or "left" in message.lower():
        Scores.Scores['a'].append(user)
        
    elif "s" == message.lower() or "back" in message.lower():
        Scores.Scores['s'].append(user)
        
    elif "d" == message.lower() or "right" in message.lower():
        Scores.Scores['d'].append(user)
        
    elif "shift" == message.lower() or "grab" in message.lower():
        Scores.Scores['shift'].append(user)
        
    elif "space" == message.lower() or "jump" in message.lower() or " " == message.lower():
        Scores.Scores['space'].append(user)
        
    elif "ctrl" == message.lower() or "dive" in message.lower():
        Scores.Scores['ctrl'].append(user)
    
    elif "esc" == message.lower() or "menu" in message.lower():
        Scores.Scores['esc'].append(user)
        
    elif "quit" == message.lower():
        sock.close()
        exit()
    else:
        print(user + ": " + message)
        print("CURRENT SCORE:")
        for each in Scores.Scores:
            print(each + " - " + str(len(Scores.Scores[each])))



def setup():
    sock.connect((server, port))
    sock.send(f'PASS {oauth}\n'.encode('utf-8'))
    sock.send(f'NICK {nickname}\n'.encode('utf-8'))
    sock.send(f'JOIN {channel}\n'.encode('utf-8'))
    timer = Timer(time.time(), time.time())

    resp = sock.recv(2048).decode('utf-8')
    print(resp)
    resp = sock.recv(2048).decode('utf-8')
    print(resp)
    
    
    while True:

        resp = sock.recv(2048).decode('utf-8')
        get_message((resp.split("!")[0][1:], resp.split()[-1][1:]))

        if time.time() >= timer.start + 1:
            Scores.winner = max(Scores.Scores.items(), key=operator.itemgetter(1))[0]
            for each in Scores.Scores:
                print(each + " - " + str(Scores.Scores[each]))
            
            print(Scores.winner)
            Scores.reset_score()
            print(Scores.winner + " is the winner!")         

        else:
            print("No new winner, repeating last command")
            timer.time = time.time()
        
        command_fallguy(Scores.winner)


def command_fallguy(command):
    if command == "space" or command == "esc" or command == "ctrl":
        time.sleep(.05)
        keyboard.press(command)
        time.sleep(.1)
        keyboard.release(command)

    elif command == "shift":
        keyboard.press(command)
        time.sleep(1)
        keyboard.release(command)
        keyboard.press(command)
        time.sleep(1)
        keyboard.release(command)
    else:
        for each in range(0, 9):
            time.sleep(.05)
            keyboard.press(command)
            time.sleep(.1)
            keyboard.release(command)




if __name__ == "__main__":
    setup()