
import socket
import struct
import time
import os

def checksum(data):
    total = 0

    for i in range(0, len(data) - 1, 2):
        total += (data[i] << 8) + data[i + 1]

    if len(data) % 2:
        total += data[-1] << 8

    total = (total >> 16) + (total & 0xffff)
    total += total >> 16

    return ~total & 0xffff


def ping(destination):
    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_RAW,
            socket.IPPROTO_ICMP
        )

        # ICMP Echo Request
        header = struct.pack(
            "!BBHHH",
            8, 0, 0, 1, 1
        )

        data = b"Hello ICMP from Python"

        chksum = checksum(header + data)

        header = struct.pack(
            "!BBHHH",
            8, 0, chksum, 1, 1
        )

        packet = header + data

        print("Mengirim ICMP Ping ke", destination)

        for i in range(4):
            start = time.time()

            sock.sendto(packet, (destination, 0))

            response, address = sock.recvfrom(1024)

            end = time.time()

            print(
                f"Reply from {address[0]} "
                f"time={(end-start)*1000:.2f} ms"
            )

            time.sleep(1)

        sock.close()

    except Exception as e:
        print("Error:", e)


ping("8.8.8.8")
