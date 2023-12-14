# Real-Time FTP updates
This project aims to develop a simple FTP client via CLI and a simple FTP server with an integrated UI using Flask.
To simplify real-time updates with Flask.

# Description
The FTP server supports the following commands:
  * ls - lists all entries at the main dir level.
  * get <file_name> or * - sends <file_name> to the client, all if * is present.
  * put <file_name> - uploaded <file_name> to the server.
  * cat <file_name> - displays the content of the file. (A bit sketchy).

# Updates
The FTP server will notify the UI with real-time updates of the application's statistics using SocketIO.

# Authors
Daniel Sapojnikov 2023, work in progress...
