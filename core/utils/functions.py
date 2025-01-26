import re


def extract_year(raw_text: str) -> str:
    """
    Extracts a year (4 digits) from a text.
    """
    match: re.Match[str] | None = re.search(r"\b\d{4}\b", raw_text)
    return match.group(0) if match else "Unknown"


def sanitize_filename(filename: str) -> str:
    """
    Replace any invalid Windows filename characters with an underscore.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def remove_ansi_escape_codes(log_entry: str) -> str:
    """
    Removes ANSI escape codes (colors) from a string of text.
    """
    return re.sub(r"\x1b\[[0-9;]*m", "", log_entry)
