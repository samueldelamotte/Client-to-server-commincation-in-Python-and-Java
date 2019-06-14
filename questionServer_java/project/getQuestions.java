package project;

import java.io.*;
import java.util.*;
import org.json.*;

public class getQuestions
{

    public JSONObject main(String[] args) {
        
        //generate a set of 10 random numbers from 1 to 15.
        List<Integer> rando = QuestionSet();
        
        JSONObject x = new JSONObject();

        //Questions and options referring to those numbers
        x = GetQ(rando); 
        
        return x;
    }   

    /**
    * Returns a list random numbers from 1 to however many rows there are in the QuestionSheet.csv. 
    * No duplicates
    **/
    public static List<Integer> QuestionSet() {

        List<Integer> shuffledList = new ArrayList<Integer>();
        int size = 0;

        //Reading the QuestionSheet.csv to figure out how many questions there are
        try {
            FileReader fr;
            fr = new FileReader("QuestionSheet.csv");
            
            LineNumberReader sizeFinder = new LineNumberReader(fr);
            
            //Store the number of questions into "size"
            while(sizeFinder.readLine() != null) {
                size++;
            }    

            //Shuffle all the numbers (no duplicates)
            List<Integer> jumble = new ArrayList<Integer>();

            for(int i = 0; i < size; i++) {
                jumble.add(i+1);
            }

            Collections.shuffle(jumble);

            //Only take 10 of those shuffled numbers and return it.
            for(int count = 0; count < 10; count++){
                int temp = jumble.get(count);
                shuffledList.add(temp);
            }
            
            sizeFinder.close();
        }

        catch (IOException e) {
            e.printStackTrace();
        }

        return shuffledList;
        
    }

    /**
    * Returns a String containing all 10 questions and options from 
    * the random numbers generated above.
    **/
    public static JSONObject GetQ(List<Integer> rando) {

        List<String> data = new ArrayList<String>();
        List<String> Q = new ArrayList<String>();
        List<String> A = new ArrayList<String>();
        List<String> B = new ArrayList<String>();
        List<String> C = new ArrayList<String>();
        List<String> D = new ArrayList<String>();

        JSONObject jsonObject = new JSONObject();
        
        //Scanning the csv file to get the data.
        try {
            FileReader fr = new FileReader("QuestionSheet.csv");
            BufferedReader br = new BufferedReader(fr);

            //Storing all Questions in List<String> Q
            //Storing all Option 1 in List<String> A
            //Storing all Option 2 in List<String> B
            //Storing all Option 3 in List<String> C
            //Storing all Option 4 in List<String> D

            String line;

            while((line = br.readLine()) != null) {

                String[] splitBy = line.split(",");

                data = Arrays.asList(splitBy);

                String q = data.get(1);
                String a = data.get(2);
                String b = data.get(3);
                String c = data.get(4);
                String d = data.get(5);

                Q.add(q);
                A.add(a);
                B.add(b);
                C.add(c);
                D.add(d); 
            }

            //Looping through Q,A,B,C,D and storing only the 
            //10 questions and options into a String.
            for(int i :rando) {
                
            	List<String> QS = new ArrayList<String>();
            	
                String q = Q.get(i-1);
                String a = A.get(i-1);
                String b = B.get(i-1);
                String c = C.get(i-1);
                String d = D.get(i-1);

                String x = Integer.toString(i);

                //storing values (q,a,b,c,d) into an array
                QS.add(q);
                QS.add(a);
                QS.add(b);
                QS.add(c);
                QS.add(d);
                
                //Storing the array under the Question ID
                jsonObject.put(x,QS);
            }
            
            
            br.close();
        }

        catch (IOException | JSONException e) {
            e.printStackTrace();
        }

        return jsonObject;
    }

  }