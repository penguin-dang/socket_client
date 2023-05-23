import socket
import time
import json
from queue import Queue
from threading import Thread

class CommunicationClient():
    def __init__(self, port=12002, host_ip='127.0.0.1'):

        self.port = port
        self.host_ip = host_ip
        self.__communicat_queue = Queue()
        self.__init_socket(port = self.port, host_ip = self.host_ip)

        self.__communicate_thread = Thread(
                target = self.__communicate,
                args=())
        self.__communicate_thread.daemon = True
        self.__communicate_thread.start()

    def __init_socket(self, host_ip, port):
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print('Socket error: %s' % err)
        # connecting to the server
        try:
            self.socket_client.connect((host_ip, port))
            print ("the socket has successfully connected")
        except:
            pass

    def readline(self):
        return self.__communicat_queue.get()

    def isHasNewData(self):
        return not self.__communicat_queue.empty()

    def __handle_connection_receive_data(self, data_line):
        self.__communicat_queue.put(data_line)

    def sendline(self, data):
        try:
            data = self.__json_output(data)
            self.__sendline_socket(data)
        except:
            print('not connected socketserver, wait msg')
            self.__init_socket(self.host_ip, self.port)

    def __readline_socket(self):
        data = self.conn.recv(1)

        data= data.decode()
        if data != "\n":
            self.__data_line += data
            return None
        else:
            ret = self.__data_line
            self.__data_line = ''
            return ret

    def __sendline_socket(self, data):
        data = str(data)+"\r\n" #"\r\n" : end of line
        encoded_data = data.encode('utf-8')
        print(encoded_data)
        self.socket_client.send(encoded_data)

    def __json_output(self, send_string={}):
        data_json = json.dumps(send_string) 
        return data_json

    def __receiveAlways(self):
        message = ''
        while True:
            try:
                data = self.socket_client.recv(1024).decode()
                data = json.loads(data) #str to dict
                self.__handle_received_message_callback(data)
            except:
                pass

    def __handle_connection(self):
        while True:
            try:
                data_line = self.__readline_socket()
                if data_line != None:
                    self.__handle_connection_receive_data(data_line)
            except:
                pass


    def __communicate(self):
        while True:
            print("Receving data")
            self.__handle_connection()

            print("Done reiceive data")
            time.sleep(0.1)
