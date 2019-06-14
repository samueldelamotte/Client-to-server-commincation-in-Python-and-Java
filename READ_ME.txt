TESTING SERVER (ON WINDOWS):
--> REQUIREMENTS:
	- MUST HAVE PORT 443 FORWARDED FOR HTTPS CONNECTION
	- MUST HAVE PORT 80 FORWARDED FOR SOCKET CONNECTION BETWEEN TESTING AND QUESTION SERVER
	- MUST HAVE PYTHON 3.6 AS THE INTERPRETER
--> TO RUN:
	1) OPEN CMD
	2) CHANGE DIRECTORY TO "C:\\...\final\testingServer_python\server"
	3) ENTER COMMAND; 	py server.py
	4) TO QUIT; 		CTRL+C


--------------------------------------------------------------------------------------------------
QUESTION SERVER (ON WINDOWS):
--> REQUIREMENTS:
	- MUST HAVE JDK 10.0.1 INSTALLED
	- MUST HAVE JRE 10.0.1 INSTALLED
--> TO COMPILE:
	1) OPEN CMD
	2) CHANGE DIRECTORY TO "C:\\...\final\questionServer_java\project"
	3) ENTER COMMAND; 	javac -cp gson.jar;json.jar;. Server.java getQuestions.java Checks.java
--> TO RUN:
	1) OPEN CMD
	2) CHANGE DIRECTORY TO "C:\\...\final\questionServer_java"
	3) ENTER COMMAND; 	java -cp project\gson.jar;project\json.jar;. project.Server 
	4) TO QUIT; 		CTRL+C
--------------------------------------------------------------------------------------------------
CONNECT THROUGH BROWSER:
	1) GO TO --> https://localhost:443
	2) USERNAME: studentOne
	3) PASSWORD: password1
