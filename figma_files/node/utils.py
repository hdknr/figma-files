import re


def to_snake(src: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", src).upper()
