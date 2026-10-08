import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
AUTH_DB = BASE_DIR / "auth_users.db"


def _connect():
    conn = sqlite3.connect(AUTH_DB)
    conn.row_factory = sqlite3.Row
    return conn


def _hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000
    ).hex()
    return salt, digest


def _verify(password, salt, stored_hash):
    _, digest = _hash_password(password, salt)
    return secrets.compare_digest(digest, stored_hash)


def init_auth_db():
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin','recruiter','user')),
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    # Create demo accounts only when they do not already exist.
    demo_accounts = [
        ("admin", "admin@smart-hiring.local", "Admin@123", "admin"),
        ("recruiter", "recruiter@smart-hiring.local", "Recruiter@123", "recruiter"),
        ("user", "user@smart-hiring.local", "User@123", "user"),
    ]
    for username, email, password, role in demo_accounts:
        row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if row is None:
            salt, password_hash = _hash_password(password)
            conn.execute(
                "INSERT INTO users(username,email,password_hash,salt,role,created_at) VALUES(?,?,?,?,?,?)",
                (username, email, password_hash, salt, role, datetime.now().isoformat(timespec="seconds")),
            )
    conn.commit()
    conn.close()


def get_all_users():
    init_auth_db()
    conn = _connect()
    rows = conn.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user(login):
    init_auth_db()
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM users WHERE lower(username)=lower(?) OR lower(email)=lower(?)",
        (login, login),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def login_user(login, password, role):
    user = get_user(login)
    if not user or user["role"] != role.lower():
        return None
    if not _verify(password, user["salt"], user["password_hash"]):
        return None
    user.pop("password_hash", None)
    user.pop("salt", None)
    return user


def register_user(username, email, password, role, confirm_password):
    init_auth_db()
    username = username.strip()
    email = email.strip().lower()
    role = role.lower().strip()

    if not username or not email or not password:
        return False, "Please fill in all account fields.", None
    if role not in {"user", "recruiter"}:
        return False, "Only User and Recruiter accounts can be created here.", None
    if len(username) < 3:
        return False, "Username must contain at least 3 characters.", None
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Please enter a valid email address.", None
    if len(password) < 6:
        return False, "Password must contain at least 6 characters.", None
    if password != confirm_password:
        return False, "Passwords do not match.", None

    salt, password_hash = _hash_password(password)
    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO users(username,email,password_hash,salt,role,created_at) VALUES(?,?,?,?,?,?)",
            (username, email, password_hash, salt, role, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username or email already exists.", None
    conn.close()
    return True, "Account created successfully.", get_user(username)


init_auth_db()
