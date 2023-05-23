import time
import json
import traceback
import threading
from threading import Thread

from client import CommunicationClient
import messages

def main():
    global socket_client

    while True:
        try:
            socket_client = CommunicationClient(port=12002, host_ip='127.0.0.1')
            break
        except Exception as e:
            print(e)
            traceback.print_exc()
            time.sleep(0.1)

    sendAlwaysThread = Thread(
            target=sendAlways,
            args=(),
            daemon=True)
    sendAlwaysThread.start()

    while True:
        message = json.loads(socket_client.readline())
        message_type = self.__get_message_type(message)
        print(message_type)

def sendAlways():
    global socket_client

    sequenceID = 0
    while True:
        time.sleep(1)
        if sequenceID < 100:
            sequenceID = sequenceID + 1
        else:
            sequenceID = 0

        messages.heartbeat['heartbeat']['data']['sequenceID'] = sequenceID
        socket_client.sendline(messages.heartbeat)

if __name__ == '__main__':
    main()
