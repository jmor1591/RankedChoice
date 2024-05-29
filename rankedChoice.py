from typing import List, Dict, Optional
import heapq

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
        while self.current_index < len(self.preferences) and self.preferences[self.current_index] in eliminated:
            self.current_index += 1
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
        for ballot in self.ballots:
            top_choice = ballot.top_choice(self.eliminated)
            if top_choice in self.candidates:
                self.candidates[top_choice].increment_vote()

    def find_winner(self, total_votes: int) -> Optional[str]:
        for candidate in self.candidates.values():
            if candidate.vote_count > total_votes / 2:
                return candidate.name
        return None

    def eliminate_candidate(self) -> List[str]:
        if not self.candidates:
            return []

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