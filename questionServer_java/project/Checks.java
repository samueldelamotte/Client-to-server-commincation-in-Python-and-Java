package project;

import java.io.*;
import java.util.*;
import org.json.*;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;


public class Checks {

    /**
    * Returns a String containing "true" or "false".
    **/
    public String main(String submitted) throws JSONException {

        //Goes through the GetAnswer() method which returns the AnswerSheet
        List<String> content = new ArrayList<String>();
        content = GetAnswers();
        
        //Goes through the Checking() method which returns "true" or "false".
        //Checking takes in the AnswerSheet and the submitted answer from the student.
        String checked = null;
        checked = Checking(content, submitted); 
        
        return checked;
        
    }   

    /**
    * Returns a String containing all 10 questions and options from 
    * the random numbers generated above.
    **/
    public static List<String> GetAnswers() {


        List<String> data = new ArrayList<String>();
        List<String> AS = new ArrayList<String>();

        //Scanning the csv file to get the contents of AnswerSheet.csv
        try {
            FileReader fr = new FileReader("AnswerSheet.csv");
            BufferedReader br = new BufferedReader(fr);

            //Storing all answers in 'List<String> AS'
            String line;

            while((line = br.readLine()) != null) {

                String[] splitBy = line.split(",");

                data = Arrays.asList(splitBy);

                String ans = data.get(1); //refers to the second column of the list.

                AS.add(ans); 
            }
            
            br.close();
        }

        catch (IOException e) {
            e.printStackTrace();
        }

        return AS;
    }

    /**
    * To check if the input is correct or not. Returning true or false.
    **/
    public static String Checking(List<String> Answers, String temp) {
    	
    	int ID = 0;
    	String ANS = null;
    	
    	String check = null;
    	String result = null;
    	
    	Gson GB = new GsonBuilder().create();
        
    	//reading in the file and storing the Question ID as int and Answer as String.
        try {
            JSONObject jobj = new JSONObject(temp);
            @SuppressWarnings("unchecked")
			Iterator<String> keys = jobj.keys();
            String str_Name=keys.next();
            String value = jobj.optString(str_Name);
            
            ID = Integer.parseInt(str_Name);
            ANS = value;

            // Comparing the submitted input and the answer.
            String Actual = Answers.get(ID - 1);
            
            if(Actual.equals(ANS)) {
            	check = "true";
            }
            else {
            	check = "false";
            }
            
            result = GB.toJson(check);

        } catch(Exception e) {
            e.printStackTrace();
        }
        
        return result;
    }

}
