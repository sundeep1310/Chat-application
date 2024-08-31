#server.py
import socket
import threading
from tkinter import filedialog
import os

HOST = '127.0.0.1'
PORT = 4321
LISTENER_LIMIT = 5
active_clients = []

def listen_for_messages(client, username):
    while True:
        try:
            header = client.recv(2048)
            if header:
                if header.startswith(b"!file"):
                    process_file_message(client, username, header)
                else:
                    message = header.decode('utf-8')
                    final_msg = f"{username}~{message}"
                    send_messages_to_all(final_msg)
            else:
                print(f"The message sent from client {username} is empty")
                break
        except (ConnectionResetError, BrokenPipeError):
            print(f"Connection reset by client {username}")
            active_clients.remove((username, client))
            client.close()
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def process_file_message(client, username, header):
    try:
        parts = header.split(b"~", 3)
        if len(parts) == 4:
            _, file_name, file_size, file_extension = parts
            file_size = int(file_size)

            save_path = filedialog.asksaveasfilename(defaultextension=file_extension.decode(), filetypes=[("All Files", "*.*")])

            if save_path:
                with open(save_path, 'wb') as file:
                    bytes_received = 0
                    while bytes_received < file_size:
                        chunk = client.recv(2048)
                        if not chunk:
                            break
                        file.write(chunk)
                        bytes_received += len(chunk)
                print(f"File {file_name.decode()} from {username} saved as {save_path}")
                prompt_message = f"SERVER~{username} sent a file: {file_name.decode()}"
                send_messages_to_all(prompt_message)
            else:
                print("File transfer canceled by the user")
        else:
            print("Invalid file message format")
    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection reset by client {username} during file transfer")
        client.close()
    except Exception as e:
        print(f"Error receiving file: {e}")

def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
