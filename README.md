# Peer2Peer Messaging

#### protocol

1. Server opens udp punchole
2. Server waits for message that says `hello`
3. Server saves address of message sender
4. If there is only 1 connection the server waits for a second one (_goto 1_)
5. The server exchanges the clients' ip addresses with each other and sends them the `ready` message to indicate they are ready to message
6. The clients open a tcp listening port
7. Clients send messages over tcp which are then printed
