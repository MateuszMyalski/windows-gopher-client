import socket
import constans as const
import errorHandler
import io

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
        s.setblocking(3)
    except:
        SOCKET_STATUS = "Error while connecting to: " \
            + str(host_ip) + " on port: " + str(port)
        raise Exception(SOCKET_STATUS)

    return s


def getData(connection, command=""):
    """Sends command and receive respond from server."""

    command += const.CRLF
    received = io.BytesIO(b"")

    try:
        SOCKET_STATUS = "Sending command."
        connection.send(command.encode())
        SOCKET_STATUS = "Timeout setted."

        SOCKET_STATUS = "Receiving packets."

        buffer = connection.recv(4096)
        counter = 0
        progressHandler(0)

        while len(buffer) > 0:
            progressHandler(counter % 6)
            counter += 1
            received.write(buffer)
            buffer = connection.recv(4096)

        progressHandler(6)

        received.seek(0, 0)
    except Exception as ex:
        SOCKET_STATUS = "Error while receiving data."
        raise Exception(SOCKET_STATUS + repr(ex))
    finally:
        connection.close()

    return received


def progressHandler(state):
    """Progress bar handler.

    State can eqaual to modulo 6 when finished 6
    """
    pass
