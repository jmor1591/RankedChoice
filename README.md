# Ranked Choice Voting Program
# Overview
This program simulates a ranked choice voting system, allowing users to create an election with multiple candidates and ballots. The program then determines the winner(s) of the election based on the ranked choice voting algorithm.

Key Features
Ranked Choice Voting Algorithm: The program implements a simple ranked choice voting algorithm, where the candidate with the fewest votes is eliminated in each round.
Flexible Election Creation: Users can create an election with multiple candidates and ballots, allowing for a wide range of scenarios to be tested.
Efficient Vote Counting: The program uses a efficient vote counting system, allowing for fast and accurate results.
Unit Testing: The program includes a suite of unit tests to ensure correct functionality and catch any bugs.
Technical Details
Programming Language: Python 3.8 or later
Libraries: random and heapq libraries (included with Python)
Data Structures: The program uses dictionaries and lists to store candidate and ballot data.

# Create a list of candidate names
candidate_names = ["Candidate1", "Candidate2", "Candidate3"]

# Create a list of ballots
ballots = [
    ["Candidate1", "Candidate2", "Candidate3"],
    ["Candidate2", "Candidate3", "Candidate1"],
    ["Candidate3", "Candidate1", "Candidate2"]
]

# Create an instance of the Election class
election = Election(candidate_names)

# Add ballots to the election
for ballot in ballots:
    election.add_ballot(ballot)

# Run the election
winner = election.run_election()
print(f"The winner is: {winner}")
Benefits
Improved Efficiency: The program's efficient vote counting system allows for fast and accurate results.
Increased Flexibility: The program's flexible election creation system allows for a wide range of scenarios to be tested.
Enhanced Accuracy: The program's unit testing system ensures correct functionality and catches any bugs.
Future Development
Improved Algorithm: The program's ranked choice voting algorithm could be improved to handle more complex scenarios.
Additional Features: The program could be expanded to include additional features, such as support for multiple voting systems or advanced analytics.
Conclusion
This program demonstrates a simple ranked choice voting system, allowing users to create an election with multiple candidates and ballots. The program's efficient vote counting system and flexible election creation system make it a useful tool for testing and analyzing ranked choice voting scenarios.
