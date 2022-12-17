# Pong online

Pong multiplayer on the terminal using an API made with node js. The API is located at https://github.com/LipezJ/ApiPong.

### libraries to install
* **For terminal handling**.
  > _pip install curses_
* **For the API**.
  > _pip install socketio_
* **To listen to the movement keys**.
  > _pip install pytimedinput_
  > > For this library I make some changes so that it does not print the value of the keys when they are pressed, although it is optional I recommend it for aesthetics.
  > > The changes I made are here: https://github.com/WereCatf/pytimedinput/pull/3/commits/899882bb03070d35239a96541fb60966bf84c401

## How to use
The first thing to do is to download the Python files of the host and the guest, the first one manages the game and the other one only receives it.

1. First we run the pong-guest.py file and enter the URL of where we have mounted the server or api service and the name of the "party" (which is the json object that is stored with the information of the game), by default there is a party created called "python".

2. Then we execute the pong-host.py file and do the same procedure of the URL and the party name, this will start the game, which will end when the score of one of the two players reaches 10.

_It should be noted that the execution of the files must be done inside the console or terminal since the **curses** library works by superimposing another terminal or console on top of ours._
