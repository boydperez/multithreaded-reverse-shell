import socket
import time


class Server:
    """
    Creates a socket and sets up the server.
    """
    HOST: str
    PORT: int
    sock: socket

    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    def create_socket(self):
        """
        Create a socket object and bind the address.

        Returns:
            None
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.HOST, self.PORT))
            print(f'[Server bound successfully] \nINET: {self.HOST}')
        except socket.error as e:
            print(f'[ERROR: Server Binding error]')
            print('Retrying...')
            time.sleep(3)
            self.create_socket()

    def server_listen(self, max_conn):
        """
        Listen for incoming connections.

        Parameters:
            max_conn (int): Max number of client connections allowed

        Returns:
            None
        """
        try:
            self.sock.listen()
            print(f'[Listening on port {self.PORT}]')
        except socket.error as e:
            print(f'[ERROR: Could\'nt listen on port {self.PORT}]')
            print('Retrying...')
            time.sleep(3)
            self.server_listen(max_conn)
        except KeyboardInterrupt:
            # TODO: Using KeyboardInterrupt
            print('Shutting down server...')

    def accept_conn(self):
        """
        Accepts client connection object from the socket.accept() method.

        Returns:
            tuple: A tuple of connection object and address tuple
        """
        conn, address = self.sock.accept()
        return conn, address

    def kill_server(self):
        print("[Shutting down server]")
        # self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()


if __name__ == '__main__':
    # Test server
    s = Server('127.0.0.1', 55555)
    s.create_socket()
    s.server_listen(5)
    s.accept_conn()
    s.kill_server()
