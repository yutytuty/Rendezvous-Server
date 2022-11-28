import curses
import socket
from threading import Thread, Event
from curses import wrapper
from curses.textpad import rectangle
from time import sleep

RENDEZVOUS = ("localhost", 5678)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

connection_established = Event()
ready_for_gui = Event()
send_message_event = Event()
new_messages_event = Event()
clear_text_event = Event()

username = input("username: ")

text = ""
messages: list[str] = []


def initial_connect(target_host: tuple[str, int]) -> tuple[str, int]:
    print("[*] Sending hello to", target_host)
    s.sendto(b"hello", target_host)
    data, _ = s.recvfrom(128)
    host, port = list(map(lambda x: x.decode(), data.split(b"\00")))
    return host, port


def connection_thread(address: tuple[str, int]):
    global text
    global send_message_event

    while not connection_established.is_set():
        print("[*] Sending connection request to " + str(address))
        s.sendto(b"conn", address)
        sleep(1)
    print("[!] Connection established")
    ready_for_gui.set()

    while True:
        if send_message_event.is_set():
            s.sendto(f"{username}> {text}".encode(), address)
            messages.append(f"{username}> {text}")
            new_messages_event.set()
            text = ""
            clear_text_event.set()
            send_message_event = Event()


def listening_thread():
    global messages

    s.recvfrom(1024)
    print("[*] Got connection request")
    connection_established.set()

    while True:
        data, _ = s.recvfrom(2048)
        data = data.decode()
        messages.append(data)
        new_messages_event.set()


def draw_messages(scr: curses.window, messages_arr: list[str]):
    for i, message in enumerate(messages_arr):
        scr.addstr(i + 1, 1, message)


def logic_init():
    host, port = initial_connect(RENDEZVOUS)
    print(f"[*] Got peer address: {host}:{port}")
    peer_address = (host, int(port))
    listener = Thread(target=listening_thread, args=())
    listener.start()
    sender = Thread(target=connection_thread, args=(peer_address,))
    sender.start()


def gui_main(scr: curses.window):
    global text
    global messages
    global new_messages_event
    global clear_text_event

    scr.nodelay(True)
    window_size = (curses.LINES - 1, curses.COLS - 1)

    rectangle(scr, window_size[0] - 3, 0,
              window_size[0] - 1, window_size[1])
    rectangle(scr, 0, 0, window_size[0] - 4, window_size[1])
    scr.addstr(window_size[0] - 2, 2, "")

    while True:
        try:
            key = scr.getch()
        except curses.error:
            key = None

        if 31 < key < 127:
            text += chr(key)
            scr.addstr(window_size[0] - 2, 2, text)
            scr.refresh()
        if key == 127:
            if len(text) > 0:
                text = text[:-1]
        if key == 27:
            break
        if key == 10:
            send_message_event.set()

        if new_messages_event.is_set():
            draw_messages(scr, messages)
            scr.addstr(window_size[0] - 2, 2, "")
            scr.refresh()
            new_messages_event = Event()

        if clear_text_event.is_set():
            scr.addstr(window_size[0] - 2, 2, " " * (window_size[1] - 2))
            scr.addstr(window_size[0] - 2, 2, "")
            clear_text_event = Event()

        # scr.clear()
        # rectangle(scr, window_size[0] - 3, 0,
        #           window_size[0] - 1, window_size[1])
        # draw_messages(scr, messages)
        # rectangle(scr, 0, 0, window_size[0] - 4, window_size[1])
        # scr.addstr(window_size[0] - 2, 2, text)
        # scr.refresh()
        # sleep(0.04)


logic_init()

while not ready_for_gui.is_set():
    pass

sleep(0.5)

wrapper(gui_main)
