def parse_token(token, lower=True):
    if lower:
        token = token.lower()
    return token.strip()
