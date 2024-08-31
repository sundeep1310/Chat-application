Welcome to ChatApp! This real-time chat application, developed as a Distributed Systems project in the 3rd year of college, offers a modern, secure messaging experience with a sleek, responsive design.
🌟 Features

Client-Server Architecture: Built using Python's socket library for network communication.
Graphical User Interface: Developed with tkinter for an intuitive user experience.
Multi-threading: Enables simultaneous handling of multiple client connections.
Real-Time Messaging: Instant communication between connected clients.
File Sharing: Ability to send and receive files between users.
User Authentication: Simple username-based authentication system.
Logout Functionality: Allows users to safely disconnect from the chat.

🛠 Technology Stack

Backend: Python
Frontend: Python with Tkinter
Networking: Socket programming
Concurrency: Threading

🚀 Getting Started
Prerequisites

Python 3.x
Tkinter (usually comes pre-installed with Python)

Installation

Clone the repository:
Copygit clone https://github.com/yourusername/chatapp.git
cd chatapp

No additional installation is required as the project uses Python's standard libraries.

Running the Application

Start the server:
Copypython server.py

Launch the client application:
Copypython client.py

Enter a username and click "Join" to connect to the chat.

💻 Usage

Joining the Chat:

Enter your desired username.
Click the "Join" button to connect to the server.


Sending Messages:

Type your message in the text box at the bottom.
Click "Send" or press Enter to send the message.


Sending Files:

Click the "Send File" button.
Choose the file you want to send from the file dialog.


Receiving Files:

When someone sends a file, you'll be prompted to save it.
Choose the location and name for the received file.


Logging Out:

Click the "Logout" button to safely disconnect from the server.



🔧 Advanced Configuration

The server's host and port can be configured in both client.py and server.py.
Default settings:

Host: 127.0.0.1 (localhost)
Port: 4321