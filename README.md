# Peer2Peer Messaging

---
#### How to run
1. Download the repository with: `git clone https://github.com/yutytuty/Rendezvous-Server.git`
2. Change the `ADDR` constant at the top of the `server.py` and the `RENDEZVOUS` constant at the top of `client.py` to your desired address, although running on localhost works out of the box.
3. Run the server with `python3 server.py`
4. Run both clients with `python3 client.py`
5. When both clients are connected, a chat window will open up in the terminal and messaging will work.
---
#### protocol

1. Server opens udp punchole
2. Server waits for message that says `hello`
3. Server saves address of message sender
4. If there is only 1 connection the server waits for a second one (_goto 1_)
5. The server exchanges the clients' ip addresses with each other and sends them the `ready` message to indicate they are ready to message
6. The clients open a tcp listening port
7. Clients send messages over udp which are then printed
