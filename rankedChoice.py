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
        self.current_top_choice: Optional[str] = preferences[0] if preferences else None

    def remove_candidate(self, candidate_name: str) -> None:
        if candidate_name in self.preferences:
            self.preferences.remove(candidate_name)

    def top_choice(self, eliminated: List[str]) -> Optional[str]:
        i = 0
        while i < len(self.preferences):
            if self.preferences[i] not in eliminated:
                self.current_top_choice = self.preferences[i]
                return self.preferences[i]
            else:
                self.remove_candidate(self.preferences[i])  # Remove the eliminated preference
                i -= 1  # Decrement the index to recheck the current position after removing an element
            i += 1  # Move to the next preference
        return None

class Election:
    def __init__(self, candidate_names: List[str]):
        self.candidates: Dict[str, Candidate] = {name: Candidate(name) for name in candidate_names}
        self.ballots: List[Ballot] = []
        self.lost: List[str] = []

    def add_ballot(self, preferences: List[str]) -> None:
        ballot = Ballot(preferences)
        self.ballots.append(ballot)
        # Increment vote count for the initial top choice
        if ballot.current_top_choice in self.candidates:
            self.candidates[ballot.current_top_choice].increment_vote()

    #optimized so that iterates minimally
    def count_votes(self) -> None:
        # Only update votes for ballots whose top choice was eliminated
        for ballot in self.ballots:
            current_top_choice = ballot.current_top_choice
            new_top_choice = ballot.top_choice(self.lost)
            if current_top_choice != new_top_choice:
                if new_top_choice in self.candidates:
                    self.candidates[new_top_choice].increment_vote()
                ##ballot.current_top_choice = new_top_choice #redundant

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
                eliminated_candidates.append(candidate_name)
        self.lost.extend(eliminated_candidates)
        return eliminated_candidates

    def run_election(self) -> str:
        total_votes = len(self.ballots)
        i = 0
        while i < 100:
            self.count_votes()
            winner = self.find_winner(total_votes)
            if winner:
                return winner

            eliminated_candidates = self.eliminate_candidate()
            if not eliminated_candidates:
                break  # No candidates left to eliminate
            i += 1

        return "No winner"

# Example usage
if __name__ == "__main__":
    candidate_names = ["Alice", "Bob", "Charlie"]
    election = Election(candidate_names)
    election.add_ballot(["Charlie", "Alice", "Bob"])
    election.add_ballot(["Bob", "Alice", "Charlie"])
    """
    election.add_ballot(["Alice", "Bob", "Charlie"])
    election.add_ballot(["Alice", "Bob", "Charlie"])
    election.add_ballot(["Charlie", "Bob", "Alice"])
    """

    winner = election.run_election()
    print(f"The winner is: {winner}")
