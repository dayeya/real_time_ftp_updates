import os
import sys
import pickle
from pathlib import Path
from typing import Callable, Tuple, Generator
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

def sys_append_modules() -> None:
    """
    Appends all importent modules into sys_path.
    :returns: None.  
    """
    parent = './..'
    module = os.path.abspath(os.path.join(os.path.dirname(__file__), parent))
    sys.path.append(module)

sys_append_modules()
from command import FTPCommand, CommandError

type IP = str
type PORT = int
type Command = str
type Address = Tuple[IP, PORT]

def create_new_thread(func: Callable, *args: Tuple[object]) -> Thread:
    return Thread(target=func, args=args, name=f'{func.__name__}-{args[1][0]}:{args[1][1]} Thread')

def setup_socket(sock: socket, addr: Tuple[str, int]) -> None:
    sock.bind(addr)
    sock.listen()
    print(f'FTP server is up at: {addr[0]}:{addr[1]}')

def send_ack(sock: socket) -> None: 
    sock.send(b'ACK')

def download_file(sock: socket, file_size: int) -> bytes:
    print(file_size)
    total_bytes = bytearray()
    while len(total_bytes) < file_size:
        chunk = sock.recv(1024)
        total_bytes.extend(chunk)
    return bytes(total_bytes)

def put(client: socket, cmd: FTPCommand) -> None:
    file_name = cmd.args
    send_ack(client)
    file_size = client.recv(4096).decode('utf-8').split('|')[1]
    send_ack(client)
    file_data = download_file(client, int(file_size)).decode('utf-8')
    os.chdir('ftp_server/main')
    with open(file_name, 'w') as f:
        f.write(file_data)

def main_list() -> Generator:
    main_dir = os.listdir(Path('ftp_server/main'))
    for entry in main_dir:
        entry_path = os.path.abspath(os.path.join('ftp_server/main', entry))
        entry_type = 'FILE' if os.path.isfile(entry_path) else 'DIR'
        yield f'<{entry_type}> {os.path.basename(entry)}, <SIZE> {os.path.getsize(entry_path)}'
        
def ls(client: socket) -> None:
    for entry in iter(main_list()):
        client.send(entry.encode('utf-8'))
    client.send(b'EOF')

def handle_command(client: socket, cmd: FTPCommand) -> None:
    if cmd.is_ls():
        ls(client)
    if cmd.is_put():
        put(client, cmd)
    
def handle_client(client: socket, addr: Address) -> None:
    print(f'Handling {addr[0]}:{addr[1]}')
    while True:
        try:
            cmd = pickle.loads(client.recv(4096))
        except ConnectionResetError as e:
            break
        if not isinstance(cmd, FTPCommand) or not cmd:
             break
        handle_command(client, cmd)
        
    print(f"Closing connection with {addr[0]}:{addr[1]}")
    client.close()

def main() -> None:
    sock = socket(AF_INET, SOCK_STREAM)
    setup_socket(sock, ('0.0.0.0', 50000))
    
    # Create main dir.
    Path('ftp_server/main').mkdir(parents=True, exist_ok=True)
    
    while True:
        client, addr = sock.accept()
        t: Thread = create_new_thread(handle_client, client, addr)
        t.start()
    
if __name__ == '__main__':
    main()