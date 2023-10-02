import hashlib


def generate_short_url(long_url):
    """
        generate short url from origin url using md5 protocol
    """
    hash_object = hashlib.md5(long_url.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

