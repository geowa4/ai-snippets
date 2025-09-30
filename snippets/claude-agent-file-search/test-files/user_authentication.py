"""User authentication module."""

import hashlib
from typing import Optional


class UserAuthenticator:
    """Handles user login and password verification."""

    def __init__(self) -> None:
        """Initialize the authenticator with an empty user database."""
        self.users: dict[str, str] = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with hashed password."""
        if username in self.users:
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = password_hash
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Verify user credentials."""
        if username not in self.users:
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.users[username] == password_hash

    def get_user(self, username: str) -> Optional[str]:
        """Get user information if exists."""
        return username if username in self.users else None
