#!/usr/bin/env python3
"""
- cgi used for grabbing information put into html form.
- cgitb used for error traceback, presented in the html page.
- csv used to read data from csv files local to the server.
- os used for scanning directory for student information file
- socket used to communicate between this server and the java server
- json used as the form of communication between the two servers
"""
import os
import csv
import socket
import json
import cgi
import cgitb
cgitb.enable()


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: SCANS BROWSER FOR WEBSITE COOKIE SO WE CAN TRACK THE USER
# RETURNS: A COOKIE OF STUDENT ID OR NOTHING IF STUDENT HAS NOT LOGGED IN
def find_cookie():
    if 'HTTP_COOKIE' in os.environ:
        cookie = os.environ['HTTP_COOKIE']  # cookie is stored in os environment
        return cookie
    else:
        return None


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: READS IN STUDENT DATA FILE FOR MANIPULATION
# RETURNS: LIST OF DATA
def read_csv_as_list(student):
    with open('../data/%s.csv' % student, 'r', newline='') as infile:
        reader = csv.reader(infile)
        arr = list(reader)
        infile.close()
        return arr


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: CREATES CONNECTION WITH JAVA SERVER, GETS APPROPRIATE QUESTIONS/OPTIONS FOR STUDENT
# RETURNS: JSON DATA STRING
def get_questions():
    HOST = 'localhost'
    PORT = 80
    getQuestions = "get"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket (SOCK_STREAM means a TCP socket)
    sock.connect((HOST, PORT))                                # Connect to server and send data
    sock.sendall((getQuestions + '\n').encode('utf-8'))
    questions = sock.recv(2048)                               # Receive data from the server and shut down
    questions = questions.decode('utf-8')
    questions = json.loads(questions)
    sock.close()
    return questions


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: POPULATES STUDENT DATA FILE WITH APPROPRIATE QUESTIONS/OPTIONS FOR STUDENT
# RETURNS: POPULATED DATA LIST
def insert_questions(questions, arr):
    keys = list(questions.keys())
    x = 0
    i = 4
    while x < 10:
        arr[i] = questions[keys[x]]
        arr[i].append(str(keys[x]))
        x += 1
        i += 1
    return arr


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: WRITES MANIPULATED STUDENT DATA LIST TO A NEW CSV FILE, OVERWRITING PREVIOUS FILE
# RETURNS: NOTHING
def write_to_csv(studentID, arr):
    with open('../data/%s.csv' % studentID, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(arr)
    outfile.close()


# ---------------------------------------------------------------------------------------------------------------------
# DESCRIPTION: GENERATES DYNAMIC HTML WITH QUESTIONS SPECIFIC TO STUDENT, REDIRECTS TO LOGOUT AND MARKING SCRIPTS
# RETURNS: NOTHING
def generate_multichoice_html(student, arr):
    form = cgi.FieldStorage()  # get current question
    qID = int(form.getvalue('qID'))
    if -1 < qID < 10:
        print('Content - type: text / html\r\n\r\n')
        print('<html>')
        print('<form id="f1" action="logOutScript.py" method="post"></form>')
        print('<form id="f2" action="testScript.py?qID=%s" method="post"></form>' % (qID + 1))
        print('<form id="f3" action="testScript.py?qID=%s" method="post"></form>' % (qID - 1))
        print('<form id="f4" action="markingScript.py?qID=%s&sID=%s&setID=%s" method="post"></form>'
              % (qID, student, arr[qID+4][5]))
        print('<body>')
        print('<h1> Logged in as: Student %s </h1>' % arr[0][0])
        print('<input type="submit" form="f1" value="log out"/></form>')
        print('<center>')
        if qID > 0:
            print('<input type="submit" form="f3" value="previous"/>')
        if qID < 9:
            print('<input type="submit" form="f2" value="next"/>')
        print('<br>')
        print('<legend><p style="font-size:20px; font-weight: bold"> %s) %s </p></legend>' % (qID+1, arr[qID+4][0]))
        if int(arr[15][qID]) == 0 and arr[14][qID] != "3":  # tracking how many attempts and print
            print('<p>Attempts left for this question: %s</p>' % (3-int(arr[14][qID])))
        elif arr[15][qID] in ["1", "2", "3"]:  # prompts that let the user know they got it wrong or correct
            print('<p>CORRECT! (on attempt: %s)</p>' % (int(arr[14][qID])))
        else:
            print('<p>WRONG! (no more attempts)</p>')
        print('<fieldset>')
        print('<input type="radio" form="f4" id="A" name="MultiChoice" value="1" onclick="if(this.checked){check()}"> '
              'A: %s' % arr[qID+4][1])
        print('<br>')
        print('<input type="radio" form="f4" id="B" name="MultiChoice" value="2" onclick="if(this.checked){check()}"> '
              'B: %s' % arr[qID+4][2])
        print('<br>')
        print('<input type="radio" form="f4" id="C" name="MultiChoice" value="3" onclick="if(this.checked){check()}"> '
              'C: %s' % arr[qID+4][3])
        print('<br>')
        print('<input type="radio" form="f4" id="D" name="MultiChoice" value="4" onclick="if(this.checked){check()}"> '
              'D: %s' % arr[qID+4][4])
        print('<br>')
        print('<h2> Total mark: %s%s </h2>' % (arr[3][0], arr[3][1]))
        print('</fieldset>')
        print('<br>')
        if int(arr[15][qID]) == 0 and arr[14][qID] != "3":  # only allow submission if more attempts left or not correct
            print('<input type="submit" form="f4" value="submit question for marking"/>')
        print('</center></body>')
        print('</html>')


# ---------------------------------------------------------------------------------------------------------------------
ID = find_cookie()                                      # FINDS STUDENTS ID FROM COOKIE
data = read_csv_as_list(ID)                             # READS IN CSV FILE FOR THAT STUDENT
if data[4][0] == '-':                                   # IF QUESTIONS HAVE NOT BEEN RETRIEVED THEN:
    questions = get_questions()                             # GETS QUESTIONS FOR THAT STUDENT
    newData = insert_questions(questions, data)             # PUTS QUESTIONS INTO DATA LIST
    generate_multichoice_html(ID, newData)                  # GENERATES DYNAMIC HTML
    write_to_csv(ID, newData)                               # WRITE NEW DATA TO NEW FILE
else:                                                   # OTHERWISE:
    generate_multichoice_html(ID, data)                     # GENERATES DYNAMIC HTML
    write_to_csv(ID, data)                                  # WRITE NEW DATA TO NEW FILE
