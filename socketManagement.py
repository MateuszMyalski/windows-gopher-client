import socket
import constans as const
import errorHandler

SOCKET_STATUS = ""


def openConnection(domain, port):
    """Open connection with domain on port."""

    # Restrict only gopher protocole on port 70
    if not port == 70:
        SOCKET_STATUS = "Invalid port: " + str(port)
        raise Exception(SOCKET_STATUS)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SOCKET_STATUS = "Resolving host by name."
        host_ip = socket.gethostbyname(domain)
    except socket.gaierror:
        SOCKET_STATUS = "Error resolving host by name."
        raise Exception(SOCKET_STATUS)

    try:
        SOCKET_STATUS = "Connecting to: " + \
            str(host_ip) + " on port: " + str(port)
        s.connect((host_ip, port))
        s.setblocking(0)
    except:
        SOCKET_STATUS = "Error while connecting to: " \
            + str(host_ip) + " on port: " + str(port)
        raise Exception(SOCKET_STATUS)

    return s


def getData(connection, command=""):
    """Sends command and receive respond from server."""

    command += const.CRLF
    received = None
    try:
        SOCKET_STATUS = "Sending command."
        connection.send(command.encode())
        SOCKET_STATUS = "Timeout setted."
        connection.settimeout(2)
        SOCKET_STATUS = "Receiving packets."
        received = connection.makefile("rb")
    except:
        SOCKET_STATUS = "Error while receiving data."
        raise Exception(SOCKET_STATUS)
    finally:
        connection.close()

    return received
