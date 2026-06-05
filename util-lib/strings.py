"""String helper functions."""


def slugify(text):
    """Convert a string into a URL-friendly slug.

    Lowercases the text, replaces runs of non-alphanumeric characters with
    single hyphens, and strips leading/trailing hyphens.

    >>> slugify("Hello, World!")
    'hello-world'
    """
    result = []
    prev_hyphen = False
    for char in text.lower():
        if char.isalnum():
            result.append(char)
            prev_hyphen = False
        elif not prev_hyphen:
            result.append("-")
            prev_hyphen = True
    return "".join(result).strip("-")


def truncate(text, length, suffix="..."):
    """Truncate text to at most ``length`` characters.

    If the text is longer than ``length``, it is cut and ``suffix`` is
    appended so the total length does not exceed ``length``.

    >>> truncate("hello world", 8)
    'hello...'
    """
    if length < 0:
        raise ValueError("length must be non-negative")
    if len(text) <= length:
        return text
    if length <= len(suffix):
        return suffix[:length]
    return text[: length - len(suffix)] + suffix


def title_case(text):
    """Capitalize the first letter of each word, lowercasing the rest.

    Words are split on whitespace and rejoined with single spaces.

    >>> title_case("the QUICK brown fox")
    'The Quick Brown Fox'
    """
    return " ".join(word.capitalize() for word in text.split())
