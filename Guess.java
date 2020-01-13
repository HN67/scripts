import java.util.Scanner;

public class Guess {
	
	// Create static Scanner object
	public static final Scanner reader = new Scanner(System.in);

	// Execution entry
	public static void main(String[] args) {
	
		// Create goal integer
		// TODO change to random int
		int goal = 5;

		// Test program
		System.out.println("Try to determine the number 1-10");
		
		// Define input variable
		String input;
		int guess = -1;

		// Create int to track attempts
		int attempts = 0;

		while (guess != goal) {
			// Increment attempt counter
			attempts += 1;
			// Get input using scanner
			input = reader.nextLine();
			// Parse input into int
			guess = Integer.parseInt(input);
			// Check input
			if (guess < goal) {
				System.out.println(guess + " is too low");
			} else if (guess > goal) {
				System.out.println(guess + " is too high");
			} else if (guess == goal) {
				System.out.println(guess + " is correct!");
			}
		}	

		// Show attempts
		System.out.println("You guessed the number " + goal + " in " + attempts + " attempts!");

	}

}
