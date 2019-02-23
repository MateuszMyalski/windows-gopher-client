from urllib.parse import urlparse
import socketManagement as conn
import tkHyperlinkManager
import constans as const


def linkClick(link_type, link_name, domain, adress, port):
    """Describe how programm will behave after clicked on link."""
    raise Exception("Fail while executing callback.")


def parseMenuItem(line):
    """Parse menu item.

    Return:
        If valid menu item:
            (tuple) [0] - link type
                    [1] - link name
                    [2] - adress
                    [3] - domain
                    [4] - port
        Else:
            (str)
    """

    # Slice the line
    menu_item = line.replace("\r\n", "")
    menu_item = line.strip(" ")
    menu_item_details = []
    menu_item_details.append(menu_item[0:1])
    menu_item = menu_item[1:]
    menu_item_details += menu_item.split(const.TAB)

    # Valid menu item consist 5 elements
    # type:name:adress:domain:port
    if len(menu_item_details) != 5:
        return line

    return (menu_item_details[0],
            menu_item_details[1],
            menu_item_details[2],
            menu_item_details[3],
            menu_item_details[4].replace("\r\n", "")
            )


def parseLine(line, hyperlink_manager):
    """Parse line in gopher standards.

    Return :
        (tuple) [0] - parsed line
                [1] - tag
    """

    parsed_line = line.decode(const.DECODING_STANDARD)
    tag = ""

    if not line:
        parsed_line = 'Problem while displaying line.'
        tag = "error"
        return "", tag

    # END OF PAGE
    if parsed_line.replace(const.CRLF, "") == '.':
        return "", tag

    # I don`t why I get it sometimes.
    parsed_line = parsed_line.replace("error.host", "")
    parsed_line = parsed_line.replace("null.host", "")

    # International message
    if parsed_line.startswith("i") and parsed_line.endswith("1" + const.CRLF):
        parsed_line = parsed_line[1:]
        parsed_line = parsed_line[:-3]
        parsed_line += const.CRLF
        tag = "international"
        return const.TAB + parsed_line, tag

    # Special line - menu item
    if parsed_line.startswith(tuple(const.TYPENAME.keys())):
        parsed_line = parseMenuItem(parsed_line)

        if type(parsed_line) == tuple:
            link_details = [
                parsed_line[0],  # link type
                parsed_line[1],  # link name
                parsed_line[2],  # link adress
                parsed_line[3],  # link domain
                parsed_line[4]   # link port
            ]
            tag = hyperlink_manager.add(linkClick, link_details)
            parsed_line = const.TYPENAME[parsed_line[0]] \
                + const.TAB + parsed_line[1] + const.CRLF
            return parsed_line, tag

    return parsed_line, tag


def go(tk_adress_field, tk_browser_field):
    """Run the connection."""

    # Prepare information about connection
    parsed_url = urlparse(tk_adress_field.get())
    scheme = parsed_url.scheme
    hostname = parsed_url.hostname
    adress = parsed_url.path
    port = parsed_url.port
    query = parsed_url.query

    # When is not link process to Veronica
    if hostname is None:
        hostname = "gopher.floodgap.com"
        adress = "v2/vs"
        port = 70
        query = tk_adress_field.get()

    # When URL have arguments add needed TAB
    if query:
        query = const.TAB + query

    # Prepare browser screen for new data
    hyperlink_manager = tkHyperlinkManager.HyperlinkManager(
        tk_browser_field,
        downloadFile)
    tk_browser_field.config(state="normal")
    tk_browser_field.delete('1.0', "end")

    # Establish connection and receive data
    connection = conn.openConnection(hostname, port)
    page_source = conn.getData(connection, adress + query)

    # DEBUG
    # import os
    # os.system('cls')

    # Parse received data
    for line in page_source.readlines():
        # print(line)
        parsed_line = parseLine(line, hyperlink_manager)
        tk_browser_field.insert("insert", parsed_line[0], parsed_line[1])
    tk_browser_field.config(state="disabled")


def downloadFile(url, name):
    """Download the file and save on disc."""

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    hostname = parsed_url.hostname
    adress = parsed_url.path
    port = parsed_url.port
    query = parsed_url.query

    # Establish connection and receive data
    connection = conn.openConnection(hostname, port)
    file_source = conn.getData(connection, adress + query)

    # Save received data
    with open(name, "wb") as file:
        for line in file_source:
            file.write(line)

    return 1
