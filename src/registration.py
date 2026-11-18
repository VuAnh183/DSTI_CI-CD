"""User registration: validates username, email and display name from CLI input."""

import re

BANNED_WORDS = {"admin", "root", "moderator", "mod", "null"}

DISPLAY_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def is_banned(word: str) -> bool:
    """True if word is in the banned list (case-insensitive)."""
    return word.lower() in BANNED_WORDS


def validate_username(username: str) -> bool:
    """Not empty, no spaces, not a banned word."""
    if not username:
        return False
    if " " in username:
        return False
    if is_banned(username):
        return False
    return True


def validate_email(email: str) -> bool:
    """Contains '@' and '.'."""
    return "@" in email and "." in email


def validate_display_name(display_name: str) -> bool:
    """3-20 chars, only letters/digits/underscore, starts with a letter, not banned."""
    if not 3 <= len(display_name) <= 20:
        return False
    if not DISPLAY_NAME_RE.match(display_name):
        return False
    if is_banned(display_name):
        return False
    return True


def resolve_display_name(display_name: str, username: str) -> str:
    """If display name is left empty, default to the username."""
    return display_name if display_name else username


def register(username: str, email: str, display_name: str = "") -> dict:
    """Validate all fields and return the user, or raise ValueError listing the problems."""
    display_name = resolve_display_name(display_name, username)

    errors = []
    if not validate_username(username):
        errors.append("Invalid username")
    if not validate_email(email):
        errors.append("Invalid email")
    if not validate_display_name(display_name):
        errors.append("Invalid display name")

    if errors:
        raise ValueError("; ".join(errors))

    return {"username": username, "email": email, "display_name": display_name}


def main():
    username = input("Username: ")
    email = input("Email: ")
    display_name = input("Display name (leave empty to use username): ")
    try:
        user = register(username, email, display_name)
        print(f"Registered: {user}")
    except ValueError as e:
        print(f"Registration failed: {e}")


if __name__ == "__main__": # pragma: no cover
    main()