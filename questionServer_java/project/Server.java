package project;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import org.json.JSONException;
import org.json.JSONObject;



public class Server {
    public static void main(String args[]) throws IOException, JSONException{
    	String function;
    	int PORT = 80;
    	
    	@SuppressWarnings("resource")
    	// creates a server socket 
		ServerSocket server = new ServerSocket(PORT);
    	System.out.println("Waiting for client on port: " + PORT);
    	
    	boolean run = true;
    	while(run) { // keeps server running until termination of the process
    		// accepts new client on that socket
    		Socket client = server.accept();
    		System.out.println("got client on port: " + PORT);
    		
    		// reads and writes to and from the socket using BufferedReader and PrintWriter
    		BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
    		PrintWriter out = new PrintWriter(client.getOutputStream(), true);
    		
    		// reads in the "task" that the testing server requires
    		// "get" = get questions for new student
    		// "{"X": "Y"}" = multichoice answer received 
    		// then calls on getQuestions.java or Checks.java depending on function received
    		// then pushes output specific to function back to the testing server 
    		function = in.readLine();
    		System.out.println("received: " + function);
    		if(function.contains("get")) {
    			getQuestions questions = new getQuestions();
        		JSONObject output = questions.main(args);
        		out.print(output);
        		out.flush();
    		}
    		else {
    			Checks check = new Checks();
        		String output = check.main(function);
        		System.out.println(output);
        		out.print(output);
        		out.flush();
    		}
    		
    		// close of connection with that client
    		client.close();
    		System.out.println("Client disconnected");
    		
    	}
    }
}
