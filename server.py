"""
Rendezvous server
"""

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ADDRESS = ("localhost", 5678)
s.bind(ADDRESS)
print("[*] Listening with UDP on", ADDRESS)


peer_addresses: dict[tuple[str, int]] = []


def main():
    while True:
        try:
            data, address = s.recvfrom(128)
            data = data.decode()
            print("[*] Recieved", f"'{data}'", "from", str(address))
            if data == "hello":
                print("[!] Recieved hello message from", str(address))
                peer_addresses.append(address)

            if len(peer_addresses) == 2:
                print("[!] 2 Clients waiting for connection. \
Exchaning address information.")
                s.sendto(peer_addresses[0][0].encode() + b"\00" +
                         str(peer_addresses[0][1]).encode(),
                         peer_addresses[1])

                s.sendto(peer_addresses[1][0].encode() + b"\00" +
                         str(peer_addresses[1][1]).encode(),
                         peer_addresses[0])
                peer_addresses.clear()

        except KeyboardInterrupt:
            print("[*] Keyboard interrupt. Quitting.")
            exit()


main()
