import copy
import socket
from _thread import *
import pickle
from game_state import game_state

server = socket.gethostbyname(socket.gethostname())
port = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print(f'Waiting for a connection, Server Started in {server} {port}')

connected = set()
games = {}
idCount = 0


def read_pos(data):
    data = data.split(",")
    return list(map(int, data))


def threaded_client(connection, player, game_id):
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = pickle.loads(connection.recv(4096))

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'get':
                        pass
                    else:

                        data = pickle.loads(data)
                        game[player]['pos'] = data['pos']
                        game[player]['angle'] = int(data['angle'])
                        game[player]['current_gun'] = data['current_gun']
                        game[player]['bullets'] = data['bullets']
                        game[player]['heal_point'] = data['heal_point']

                    connection.sendall(pickle.dumps(game))
            else:
                break
        except EOFError:
            break
    try:
        del games[game_id]
    except KeyError:
        pass

    idCount -= 1
    connection.close()


while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    idCount += 1
    gameID = (idCount - 1) // 2
    if idCount % 2 == 1:
        p = 0
        #  games[gameID] = game_state.copy()
        games[gameID] = copy.deepcopy(game_state)

    else:
        games[gameID]['ready'] = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameID))
