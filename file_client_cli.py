import socket
import json
import base64
import logging
import os

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received="" #empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received.strip())
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False

def remote_upload(filepath=""):
    try:
        filename=filepath.split('/')[-1]
        with open(f"{filepath}",'rb') as fp:
            isifile = base64.b64encode(fp.read()).decode()
        command_str=f"UPLOAD {filename} {isifile}"
        hasil=send_command(command_str)
        if hasil and hasil['status']=='OK':
            print(f"File {filename} berhasil diupload")
        else:
            print("File gagal dikirim")
    except Exception as e:
        logging.warning(f"Error uploading file: {str(e)}")
        return False

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status']=='OK':
        print(f"File {filename} berhasil dihapus\n")
        return True
    else:
        print("Gagal menghapus file\n")
        return False

def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {filename} berhasil didapatkan\n")
        return True
    else:
        print("Gagal")
        return False

def main():
    while True:
        print("\nCommandList: LIST, GET <filename>, UPLOAD <filepath>, DELETE <filename>, EXIT")
        command = input("Enter command: ").strip().split(maxsplit=1)
        cmd = command[0].upper()
        
        if cmd == "LIST":
            remote_list()
        elif cmd == "GET" and len(command) > 1:
            remote_get(command[1])
        elif cmd == "UPLOAD" and len(command) > 1:
            remote_upload(command[1])
        elif cmd == "DELETE" and len(command) > 1:
            remote_delete(command[1])
        elif cmd == "EXIT":
            break
        else:
            print("Invalid command or missing filename/filepath.")

if __name__=='__main__':
    server_address=('172.16.16.101',8889)
    main()
