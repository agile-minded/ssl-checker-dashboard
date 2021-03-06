#!/usr/bin/env python3

import ssl
import socket
from datetime import datetime


def expiration_datetime(hostname):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    conn.settimeout(3.0)
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # Parse the string from the certificate into a Python datetime object
    return datetime.strptime(ssl_info['notAfter'], r'%b %d %H:%M:%S %Y %Z')


def days_before_expiration(hostname):
    try:
        # How many days until SSL certificate will be expired
        days_before = (expiration_datetime(hostname) - datetime.now()).days
        return (hostname, days_before)
    except Exception as e:
        print('Exception in SSL expiration date checks: ',
              e, '| hostname: ', hostname)
        return (hostname, str(e)[0:40] + ' ...')
