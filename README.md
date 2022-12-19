# Pong online

Pong multiplayer on the terminal using an API made with node js. The API is [here](https://github.com/LipezJ/ApiPong).

### libraries to install
* **For terminal handling**.
  > _pip install curses / pip install windows-curses_
* **For the API**.
  > _pip install socketio_
* **To listen to the movement keys**.
  > _pip install pytimedinput_
  > > For this library I make some changes so that it does not print the value of the keys when they are pressed.
  > > The changes I made are here: [ pytimedinput ](https://github.com/WereCatf/pytimedinput/pull/3/commits/899882bb03070d35239a96541fb60966bf84c401).
  > > - The file you have to change is located in "C:\Users\ *username*\AppData\Local\Programs\Python\Python311\Lib\site-packages\pytimedinput", all you have to do is replace it with the file called pytimedinput.py with the file that is [here](https://github.com/LipezJ/pytimedinput/blob/patch-1/pytimedinput/pytimedinput.py).

## How to use
The first thing to do is to download the Python files of the host and the guest, the first one manages the game and the other one only receives it.

1. First we run the pong-guest.py file and enter the URL of where we have mounted the server or api service and the name of the "party" (which is the json object that is stored with the information of the game).

2. Then we execute the pong-host.py file and do the same procedure of the URL and the party name, this will start the game, which will end when the score of one of the two players reaches 10.

3. Finally, to play, player 1 (host) moves with the "w d" keys up and down respectively, player 2 (guest) with the "k m" keys in the same way.

4. to exit the game use the "q" key.

_It should be noted that the execution of the files must be done inside the console or terminal since the **curses** library works by superimposing another terminal or console on top of ours._
