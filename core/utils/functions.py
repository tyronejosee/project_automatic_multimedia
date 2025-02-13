import re

from .exceptions import CommandNotFound


def extract_year(raw_text: str) -> str:
    """
    Extracts a year (4 digits) from a text.

    Args:
        raw_text (str): The input text to search for a year.

    Returns:
        str: The extracted year as a string,
        or "Unknown" if no valid year is found.

    Example:
        >>> extract_year("The event happened in 2025.")
        '2025'

        >>> extract_year("No year mentioned here.")
        'Unknown'
    """
    match: re.Match[str] | None = re.search(r"\b\d{4}\b", raw_text)
    return match.group(0) if match else "Unknown"


def sanitize_filename(filename: str) -> str:
    """
    Replace any invalid Windows filename characters with an underscore.

    Args:
        filename (str): The filename to sanitize.

    Returns:
        str: A sanitized filename with invalid characters
        replaced by underscores.

    Example:
        >>> sanitize_filename("invalid|filename?.txt")
        'invalid_filename_.txt'
    """
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def remove_ansi_escape_codes(log_entry: str) -> str:
    """
    Removes ANSI escape codes (colors) from a string of text.

    Args:
        log_entry (str): The string containing ANSI escape codes.

    Returns:
        str: The string with ANSI escape codes removed.

    Example:
        >>> remove_ansi_escape_codes('\x1b[31mRed\x1b[0m')
        'Red'
    """
    return re.sub(r"\x1b\[[0-9;]*m", "", log_entry)


def get_type_choice(param: str, valid_params: list[str]) -> str:
    """
    Returns the folder type based on the parameter.

    Args:
        param (str): The input parameter that specifies the type.
        valid_params (list[str]): A list of valid parameters.

    Raises:
        CommandNotFound: If `param` is "Unknown".
        ValueError: If `param` is not in `valid_params`.

    Returns:
        str: The corresponding folder type ("Series", "Movies", or "unknown").
    """
    if param == "Unknown":
        raise CommandNotFound("Usage 'cli.py <command> <param>'")
    if param not in valid_params:
        raise ValueError(f"Invalid type choice '{param}'")
    type_choice: str = {
        "series": "Series",
        "movies": "Movies",
    }.get(param, "unknown")
    return type_choice
