#client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import os

HOST = '127.0.0.1'
PORT = 4321

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to the server")
        add_message("[CLIENT] Successfully connected to the server")
    except Exception as e:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}: {e}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(f"{username_textbox.get()}~{message}".encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def send_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                file_size = len(file_data)
                _, file_extension = os.path.splitext(file_name)
                client.sendall(f"!file~{file_name}~{file_size}~{file_extension}".encode())
                client.sendall(file_data)  # Send the file data in binary form
                add_message(f"[CLIENT] File '{file_name}' has been sent.")
        except Exception as e:
            print(f"Error sending file: {e}")
            messagebox.showerror("File Error", f"Error sending file: {e}")
    else:
        add_message("File selection canceled by the user")

def logout():
    client.sendall("!logout".encode())
    client.close()
    root.destroy()

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=10)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

file_button = tk.Button(bottom_frame, text="Send File", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_file)
file_button.pack(side=tk.LEFT, padx=10)

logout_button = tk.Button(bottom_frame, text="Logout", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=logout)
logout_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                if message.startswith("!file"):
                    handle_received_file(message)
                else:
                    username, content = message.split('~', 1)
                    add_message(f"[{username}] {content}")
            else:
                messagebox.showerror("Error", "Message received from the server is empty")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
        
def handle_received_file(message):
    parts = message.split("~", 3)
    if len(parts) == 4:
        _, file_name, file_size, file_data = parts
        file_size = int(file_size)

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])

        if save_path:
            with open(save_path, 'wb') as file:
                file.write(bytes(file_data, 'utf-8'))  # Convert the string to bytes
            add_message(f"File received: {file_name} saved as {save_path}")
        else:
            add_message("File transfer canceled by the user")
    else:
        add_message("Invalid file message format")




def main():
    root.mainloop()

if __name__ == '__main__':
    main()
