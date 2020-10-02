import socket
from _thread import *
import pickle
from game import Game

server = '192.168.1.124'
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server, port))

s.listen()

print("Server started. Waiting for a connection...")

connected = set()
games = {}
idCount = 0

def ThreadedClient(conn, p, gameId):

    global idCount

    conn.send(str.encode(str(p)))

    reply = ""

    while True:

        data = conn.recv(4096).decode()

        if gameId in games:

            game = games[gameId]

            if not data:
                break

            else:
                if data == "reset":

                    game.ResetChoices()

                elif data != "get":

                    game.Play(p, data)

                conn.sendall(pickle.dumps(game))

        else:
            break

    print("Lost Connection...")
    try:
        del games[gameId]
        print("Closing Game...", gameId)
    except:
        pass

    idCount -= 1

    conn.close()


while True:

    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2  # will give a new id every 2 player that connects

    if idCount % 2 == 1:
        # if there is one solo player, will create a new game

        games[gameId] = Game(gameId)
        print("Creating a new game...")

    else:

        games[gameId].ready = True

        p = 1

    start_new_thread(ThreadedClient, (conn, p, gameId))
