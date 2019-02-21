import constans as const

HISTORY_LIST = []


def back(tk_adress_field, action):
    """Modify the adress field and process the execution of the adress."""

    try:
        current_index = HISTORY_LIST.index(tk_adress_field.get())
    except ValueError:
        current_index = len(HISTORY_LIST)
        if current_index == 0:
            action()
            return 0

    tk_adress_field.delete(0, "end")
    tk_adress_field.insert(0, HISTORY_LIST[current_index - 1])
    HISTORY_LIST.pop(-1)

    action()


def add(url):
    """Append url site in history"""

    if not len(HISTORY_LIST) <= const.MAX_HISTORY_LIST:
        HISTORY_LIST.pop(0)

    if not len(HISTORY_LIST) == 0:
        if not HISTORY_LIST[-1] == url:
            HISTORY_LIST.append(url)
    else:
        HISTORY_LIST.append(url)
