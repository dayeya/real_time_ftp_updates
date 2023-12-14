#
# Client side - CLI program to interact with the FTP server.
#

import os
import sys
import pickle
import subprocess
from pathlib import Path
from typing import Tuple
from errors import SocketConnectionError
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

type ExecRes = Tuple[bytes, bytes]

type IP = str
type PORT = int
type Command = str
type Address = Tuple[IP, PORT]

def display_help() -> None:
    help = """Available command:
        \n- h: displays help message.
        \n- ls <num> : displays num files, else displays all.
        \n- cat <file_name>: Displays the file content.
        \n- get <file_name | first N files>: Downloads all by using 'get *' 
        \n- put: Opens a file dialog and uploads the file to the server.
    """
    print(help)
    
def run_command(cmd) -> ExecRes:
    '''
    function to execute a command using windows cmd
    gets: str, a command to execute
    returns: command output
    '''
    return subprocess.Popen(cmd,
            shell = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE).communicate()

def open_dialog() -> str:
    batch_script = 'open_dialog.bat'
    chosen_file = run_command(batch_script)[0].decode('utf-8').strip()
    return chosen_file

def send_syn_file(sock: socket, file: str) -> bytes:
    """
    Sends FTPCommand(cmd=put, args=file), starting the download process at the server.
    """
    put_syn = pickle.dumps(FTPCommand(f'put {file}'))
    sock.send(put_syn)
    ack = sock.recv(4096)
    if not ack:
        print('Server didnt accept the upload.')
    return ack

def send_file_size(sock: socket, file_size: int) -> bytes:
    """
    Sends file_size.
    """
    print(file_size)
    f_syn = f'file_size|{file_size}'.encode('utf-8')
    sock.send(f_syn)
    ack = sock.recv(4096)
    if not ack:
        print('Server didnt accept the upload.')
    return ack
    
def upload_file(sock: socket, file: str) -> int:
    _ = send_syn_file(sock, os.path.basename(file))
    _ = send_file_size(sock, os.path.getsize(file))
    bytes_sent = 0
    with open(file, 'rb') as f:
        while (chunk := f.read(1024)) != b'':
            bytes_sent += sock.send(chunk)
    assert bytes_sent == os.path.getsize(file)
    return bytes_sent

def ls(sock: socket, req: FTPCommand) -> None:
    sock.send(pickle.dumps(req))
    while (entry := sock.recv(4096).decode('utf-8')) != 'EOF':
        print(entry)

def exec_cmd(sock: socket, req: FTPCommand) -> None:
    if req.is_help():
        display_help()
        return
    
    if req.is_ls():
        ls(sock, req)
    
    if req.is_put():
        file = open_dialog()
        bytes_sent = upload_file(sock, file)
        print(f'You`ve successfuly uploaded {bytes_sent} bytes of {os.path.basename(file)}')
        return
    
def main(addr=('127.0.0.1', 50000)) -> None:
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(addr)
    except SocketConnectionError as e:
        print(f'[!] .connect({addr}) failed, FTP server is closed.')
    
    while True:
        io = str(input('execute >> '))
        request = FTPCommand(io)
        if not request:
            continue
        
        # Execute the command.
        exec_cmd(sock, request)
    
if __name__ == '__main__':
    main()