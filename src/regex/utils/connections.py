import socket


def can_connect(hostname: str):  # pragma: no cover
    # adapted from https://stackoverflow.com/a/28752285
    hostname, port = hostname.split(":")
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, int(port)), 2)
        s.close()
        return True
    except Exception:
        return False
