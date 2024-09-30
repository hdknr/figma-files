import re


def sanitize_id(id_str):
    sanitized = re.sub(r"[^A-Za-z0-9]", "_", id_str)
    return sanitized
