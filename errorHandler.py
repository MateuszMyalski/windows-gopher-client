def handle(ex, tk_browser_field):
    """Handle errors."""
    tk_browser_field.delete("1.0", "end")
    tk_browser_field.insert(
        "insert",
        "Error handled as:\n\t" + repr(ex.args[0]).title(),
        "error"
    )
    return 0
