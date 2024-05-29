import unittest
from rankedChoice import *

class TestRankedChoiceVoting(unittest.TestCase):

    def setUp(self):
        # This method will be run before each test. Set up common test data here.
        self.candidate_names = ["Alice", "Bob", "Charlie"]
        self.election = Election(self.candidate_names)

    def test_single_winner(self):
        # Test a simple case with a clear winner
        self.election.add_ballot(["Alice", "Bob", "Charlie"])
        self.election.add_ballot(["Alice", "Charlie", "Bob"])
        self.election.add_ballot(["Charlie", "Bob", "Alice"])
        self.election.add_ballot(["Bob", "Charlie", "Alice"])
        self.election.add_ballot(["Alice", "Charlie", "Bob"])

        winner = self.election.run_election()
        self.assertEqual(winner, "Alice")

    def test_tie_case(self):
        # Test case where there's a tie
        # The next preference of each ballot will be chosen to go through the cycle again,
        # If there are no remaining preferences, then and only then will
        # multiple winners be returned.
        self.election.add_ballot(["Alice", "Bob", "Charlie"])
        self.election.add_ballot(["Bob", "Charlie", "Alice"])
        self.election.add_ballot(["Charlie", "Alice", "Bob"])

        winner = self.election.run_election()
        self.assertEqual(winner, "Alice, Bob, Charlie")

    def test_elimination(self):
        # Test the elimination process
        # Bob will win because the first ballot will have Alice eliminated, then Bob will be given 3 of the 5 votes, letting
        # him win the election
        self.election.add_ballot(["Alice", "Bob", "Charlie"])
        self.election.add_ballot(["Bob", "Alice", "Charlie"])
        self.election.add_ballot(["Charlie", "Bob", "Alice"])
        self.election.add_ballot(["Charlie", "Alice", "Bob"])
        self.election.add_ballot(["Bob", "Charlie", "Alice"])

        winner = self.election.run_election()
        self.assertEqual(winner, "Bob")

    def test_edge_case_empty_ballots(self):
        # Test case with empty ballots
        self.election.add_ballot([])
        self.election.add_ballot([])
        winner = self.election.run_election()
        self.assertEqual(winner, "No winner")

    def test_edge_case_all_candidates_eliminated(self):
        # Test case where all candidates are eliminated, in the event that there is a tie between ALL remaining candidates
        # The next preference on the ballot will be chosen but none of the remaining candidates will be eliminated
        self.election.add_ballot(["Alice", "Bob"])
        self.election.add_ballot(["Bob", "Alice"])
        self.election.add_ballot(["Charlie"])

        winner = self.election.run_election()
        self.assertEqual(winner, "No winner")

    def test_eliminate_least_voted_candidate(self):
        # Test elimination of the least voted candidate. Charlie will be returned
        #because once Alice is eliminated first, her next choice is Charlie, which
        #give charlie 3 of the 5 votes, making him the majority vote
        self.election.add_ballot(["Charlie", "Alice", "Bob"])
        self.election.add_ballot(["Charlie", "Bob", "Alice"])
        self.election.add_ballot(["Alice", "Charlie", "Bob"])
        self.election.add_ballot(["Bob", "Alice", "Charlie"])
        self.election.add_ballot(["Bob", "Charlie", "Alice"])

        winner = self.election.run_election()
        self.assertEqual(winner, "Charlie")

if __name__ == "__main__":
    unittest.main()