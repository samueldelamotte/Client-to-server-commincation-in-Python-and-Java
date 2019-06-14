#!/usr/bin/env python3
"""
- cgi used for grabbing information put into html form.
- cgitb used for error traceback, presented in the html page.
- csv used to read data from csv files local to the server.
- socket used to communicate between this server and the java server
"""
import csv
import socket
import cgi
import cgitb
cgitb.enable()


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: REDIRECT TO TESTSCRIPT AFTER MARKING HAS COMPLETED
# RETURNS: NOTHING
def redirect(question):
    redirectURL = "https://localhost:443/cgi-bin/testScript.py?qID=%s" % question
    print('Content - type: text / html\r\n\r\n')
    print('<html>')
    print('<head>')
    print('<meta http-equiv="refresh" content="0;url=' + str(redirectURL) + '" />')
    print('</head>')
    print('</html>')


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: UPDATE STUDENT CSV FILE DEPENDING ON IF THEY GOT THE ANSWER CORRECT/WRONG
# RETURNS: NOTHING
def update_csv(student, question, result):
    with open('../data/%s.csv' % student, 'r', newline='') as infile:
        reader = csv.reader(infile)
        arr = list(reader)
    infile.close()

    attempt = int(arr[14][int(question)])
    bestMark = int(arr[15][int(question)])
    if bestMark != 0 or attempt == 3:
        return None
    elif result == 'correct':                           # if correct then check attempt number in csv
        attempt += 1                                    # and update mark accordingly
        arr[14][int(question)] = attempt                # and add new mark to total mark
        if attempt == 1:
            mark = int(arr[3][0])
            mark += 3
            arr[3][0] = mark
            arr[15][int(question)] = 3
        if attempt == 2:
            mark = int(arr[3][0])
            mark += 2
            arr[3][0] = mark
            arr[15][int(question)] = 2
        if attempt == 3:
            mark = int(arr[3][0])
            mark += 1
            arr[3][0] = mark
            arr[15][int(question)] = 1
        with open('../data/%s.csv' % student, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(arr)
        outfile.close()
    else:
        attempt += 1                                   # if wrong then update attempt number
        arr[14][int(question)] = attempt
        with open('../data/%s.csv' % student, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(arr)
        outfile.close()


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: MARK QUESTION BY CONNECTION TO JAVA SERVER, UPDATES ATTEMPTS IN APPROPRIATE STUDENT CSV FILE
# RETURNS: TRUE IF ANSWER WAS CORRECT, FALSE IF IT WAS INCORRECT
def mark_question(sID, qID, setID, answer):
    HOST = 'localhost'
    PORT = 80
    mark = '{"%s": "%s"}' % (setID, answer)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket (SOCK_STREAM means a TCP socket)
    sock.connect((HOST, PORT))                                # Connect to server and send data
    sock.sendall((mark + "\n").encode('utf-8'))
    result = sock.recv(2048)                                  # Receive data from the server and shut down
    result = result.decode('utf-8')
    sock.close()

    if 'true' in result:
        update_csv(sID, qID, 'correct')
    else:
        update_csv(sID, qID, 'wrong')


# ---------------------------------------------------------------------------------------------------------------------
form = cgi.FieldStorage()                           # STORE DATA FROM FORM
sID = form.getvalue('sID')                          # GET USERNAME
qID = form.getvalue('qID')                          # GET QUESTION ID ACCORDING TO LOCAL CSV
setID = form.getvalue('setID')                      # GET QUESTION ID ACCORDING TO QUESTION SERVER
optionSelected = form.getvalue('MultiChoice')       # GET THE MULTI CHOICE VALUE SELECTED
mark_question(sID, qID, setID, optionSelected)      # MARK QUESTION
redirect(qID)                                       # REDIRECT BACK TO QUESTION VIA TESTSCRIPT
