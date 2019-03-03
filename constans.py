DEFAULT_ADRESS = r"gopher://gopher.floodgap.com:70"
DEFAULT_GEOMETRY = "980x800"
DEFAULT_WINDOW_TITLE = "Gopher client"
FILENAME_CHAR_WHITELIST = "qwertyuiopasdfghjklzxcvbnm|1234567890._"
DECODING_STANDARD = "UTF-8"

TAB = "\t"
CRLF = "\r\n"

TYPENAME = {'0': '<TEXT>',
            '1': '<DIR>',
            '2': '<CSO>',
            '3': '<ERROR>',
            '4': '<BINHEX>',
            '5': '<DOS>',
            '6': '<UUENCODE>',
            '7': '<SEARCH>',
            '8': '<TELNET>',
            '9': '<BINARY>',
            '+': '<REDUNDANT>',
            'I': '<IMAGE>',
            'd': '<DOCUMENT>',
            's': '<SOUND>',
            'h': '<HTML>',
            'g': '<GIF>',
            'i': '',
            }

MAX_HISTORY_LIST = 20


# STYLES ----------------------------------------------------------------------
FONT = "fixedsys"
FONT_SIZE = 9
DARK_SCHEME = "dark"
LIGHT_SCHEME = "light"

COLOR_SCHEME = {
    "dark": {
        "font_color": "white",
        "hyperlink_color": "green",
        "international_message_color": "yellow",
        "error_color": "red",
        "background_color": "black",
        "select_background_color": "gray",
        "find_background": "chocolate3"
    },

    "light": {
        "font_color": "black",
        "hyperlink_color": "blue",
        "international_message_color": "red",
        "error_color": "red",
        "background_color": "white",
        "find_background": "plum1",
        "select_background_color": "orange"
    }
}
