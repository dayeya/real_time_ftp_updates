# RealTime FTP Updates
This project aims to develop a simple FTP client via CLI and a simple FTP server with an integrated UI using Flask.

# Description
The FTP server supports the following commands:
  * ls - lists all entries at the main dir level.
  * get <file_name> or * - sends <file_name> to the client, all if * is present.
  * put <file_name> - uploaded <file_name> to the server.
  * cat <file_name> - displays the content of the file. (A bit sketchy).

# Updates
The FTP server will notify the UI with real-time updates of the application's statistics.
To obtain such a thing, I used FlaskSocketIO.

# Rational
This simple project was developed to provide the Woof web application firewall with easier real-time updates practice.

# Authors
Daniel Sapojnikov 2023.
