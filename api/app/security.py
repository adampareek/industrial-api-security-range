import ipaddress
import socket
from urllib.parse import urlparse

def host_resolves_private(hostname: str) -> bool:
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(hostname, None)}
    except socket.gaierror:
        return True
    for address in addresses:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return True
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            return True
    return False

def validate_external_url(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False, "Only http and https are allowed."
    if not parsed.hostname:
        return False, "URL must include a hostname."
    if parsed.username or parsed.password:
        return False, "Embedded credentials are not allowed."
    if host_resolves_private(parsed.hostname):
        return False, "Private, loopback, and internal destinations are blocked."
    return True, "ok"
