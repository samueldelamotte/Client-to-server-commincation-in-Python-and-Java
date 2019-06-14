#!/usr/bin/env python3
"""
- cgi used for grabbing information put into html form.
- cgitb used for error traceback, presented in the html page.
- csv used to read data from csv files local to the server.
- os used for scanning directory for student information file
"""
import os
import cgi
import cgitb
import csv
cgitb.enable()
data = []                                   # KEEP TRACK OF DATA LIST


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: SCAN STUDENT DATA FILES TO FIND IF CORRECT USERNAME OR PASSWORD
# RETURNS: >0 IF USER/PASS IS CORRECT
def check_std_files():
    fileExtension = '.csv'
    nmbrOfStudents = 0
    for root, dirs, files in os.walk('../data'):                      # walks the cwd and returns list called files.
        for filename in files:
            if fileExtension in filename:
                nmbrOfStudents += 1

    x = 1
    count = 0
    while count < nmbrOfStudents:
        with open('../data/%s.csv' % x, 'r', newline='') as csvFile:  # reads in file by file and stores in list 'data'
            reader = csv.reader(csvFile)
            stdInfo = list(reader)
            csvFile.close()
        data.append(stdInfo)
        count += 1
        x += 1

    stdID = 0
    while stdID < nmbrOfStudents:
        if usrName == data[stdID][1][0] and pWord == data[stdID][2][0]:  # test username and pass of each sublist
            stdID += 1
            return stdID
        stdID += 1
    return 0


# ---------------------------------------------------------------------------------------------------------------------
form = cgi.FieldStorage()                   # STORE DATA FROM FORM
usrName = form.getvalue('username')         # GET USERNAME
pWord = form.getvalue('password')           # GET PASSWORD
stdID = check_std_files()                   # SCAN STUDENT DATA FILES FOR CORRECT USERNAME/PASSWORD
if stdID != 0:                              # IF LOGIN SUCCESS, REDIRECT TO STARTTEST.HTML
    redirectURL = "https://localhost:443/startTest.html"
    print('Set-Cookie: %s' % stdID)
    print('Content - type: text / html\r\n\r\n')
    print('<html>')
    print('<head>')
    print('<meta http-equiv="refresh" content="0;url=' + str(redirectURL) + '" />')
    print('</head>')
    print('</html>')
else:                                        # IF LOGIN FAIL, REDIRECT TO TRYAGAIN.HTML
    redirectURL = "https://localhost:443/tryAgain.html"
    print('Content - type: text / html\r\n\r\n')
    print('<html>')
    print('<head>')
    print('<meta http-equiv="refresh" content="0;url=' + str(redirectURL) + '" />')
    print('</head>')
    print('</html>')
