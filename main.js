    import java.io.BufferedReader;
    import java.io.IOException;
    import java.io.InputStreamReader;
    
    public class RunFlaskApp {
    
        public static void main(String[] args) {
            try {
                // Command to run Flask application
                String command = "python -m flask run --app board --debug";
    
                // Execute the command
                Process process = Runtime.getRuntime().exec(command);
    
                // Read the output of the command
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
    
                // Wait for the process to complete
                process.waitFor();
    
                // Close the reader
                reader.close();
    
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
