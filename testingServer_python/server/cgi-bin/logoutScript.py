#!/usr/bin/env python3
"""
- cgitb used for error traceback, presented in the html page.
"""
import cgitb
cgitb.enable()


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: REDIRECT TO LOGOUT.HTML AND SET COOKIE TO NOTHING (ENDS STUDENT SESSION)
# RETURNS: NOTHING
def redirect_logout():
    redirectURL = "https://localhost:443/logout.html"
    print('Set-Cookie: ')
    print('Content - type: text / html\r\n\r\n')
    print('<html>')
    print('<head>')
    print('<meta http-equiv="refresh" content="0;url=' + str(redirectURL) + '" />')
    print('</head>')
    print('</html>')


# ---------------------------------------------------------------------------------------------------------------------
redirect_logout()