from typing import List, Dict, Optional

class Candidate:
    def __init__(self, name: str):
        self.name: str = name
        self.vote_count: int = 0

    def increment_vote(self) -> None:
        self.vote_count += 1

    def decrement_vote(self) -> None:
        self.vote_count -= 1

class Ballot:
    def __init__(self, preferences: List[str]):
        self.preferences: List[str] = preferences
        self.current_index: int = 0

    def top_choice(self, eliminated: set) -> Optional[str]:
        # Skip over eliminated candidates in the ballot preferences
        while self.current_index < len(self.preferences) and self.preferences[self.current_index] in eliminated:
            self.current_index += 1
        # Return the first non-eliminated candidate or None if all are eliminated
        return self.preferences[self.current_index] if self.current_index < len(self.preferences) else None

class Election:
    def __init__(self, candidate_names: List[str]):
        self.candidates: Dict[str, Candidate] = {name: Candidate(name) for name in candidate_names}
        self.ballots: List[Ballot] = []
        self.eliminated: set = set()

    def add_ballot(self, preferences: List[str]) -> None:
        ballot = Ballot(preferences)
        self.ballots.append(ballot)
        top_choice = ballot.top_choice(self.eliminated)
        if top_choice in self.candidates:
            self.candidates[top_choice].increment_vote()

    def count_votes(self) -> None:
        # Reset vote counts
        for candidate in self.candidates.values():
            candidate.vote_count = 0
        # Count votes for current top choices on each ballot
        for ballot in self.ballots:
            top_choice = ballot.top_choice(self.eliminated)
            if top_choice in self.candidates:
                self.candidates[top_choice].increment_vote()

    def find_winner(self, total_votes: int) -> Optional[str]:
        # Check if any candidate has more than half of the total votes
        for candidate in self.candidates.values():
            if candidate.vote_count > total_votes / 2:
                return candidate.name
        return None

    def eliminate_candidate(self) -> List[str]:
        if not self.candidates:
            return []
        # Find the candidate(s) with the fewest votes
        min_votes = min(candidate.vote_count for candidate in self.candidates.values())
        eliminated_candidates = []
        for candidate_name, candidate in list(self.candidates.items()):
            if candidate.vote_count == min_votes:
                del self.candidates[candidate_name]
                self.eliminated.add(candidate_name)
                eliminated_candidates.append(candidate_name)
        return eliminated_candidates

    def run_election(self) -> str:
        total_votes = len(self.ballots)
        # Iterate up to the number of candidates to eliminate one candidate per round
        for _ in range(len(self.candidates)):
            self.count_votes()
            winner = self.find_winner(total_votes)
            if winner:
                return winner
            eliminated_candidates = self.eliminate_candidate()
            if not eliminated_candidates:
                break  # No candidates left to eliminate
        return "No winner"

# Example usage
if __name__ == "__main__":
    candidate_names = ["Alice", "Bob", "Charlie"]
    election = Election(candidate_names)
    election.add_ballot(["Charlie", "Alice", "Bob"])
    election.add_ballot(["Bob", "Alice", "Charlie"])
    election.add_ballot(["Alice", "Bob", "Charlie"])
    election.add_ballot(["Alice", "Bob", "Charlie"])
    election.add_ballot(["Charlie", "Bob", "Alice"])

    winner = election.run_election()
    print(f"The winner is: {winner}")