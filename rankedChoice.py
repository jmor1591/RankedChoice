from typing import List, Dict, Optional

class Candidate:
    def __init__(self, name: str):
        self.name: str = name
        self.vote_count: int = 0

    def increment_vote(self) -> None:
        self.vote_count += 1

    def reset_vote_count(self) -> None:
        self.vote_count = 0


class Ballot:
    def __init__(self, preferences: List[str]):
        self.preferences: List[str] = preferences

    def remove_candidate(self, candidate_name: str) -> None:
        if candidate_name in self.preferences:
            self.preferences.remove(candidate_name)

    def top_choice(self, eliminated: List[str]) -> Optional[str]:
        for preference in self.preferences:
            if preference not in eliminated:
                return preference
        return None


class Election:
    def __init__(self, candidate_names: List[str]):
        self.candidates: Dict[str, Candidate] = {name: Candidate(name) for name in candidate_names}
        self.ballots: List[Ballot] = []
        self.lost: List[str] = []

    def add_ballot(self, preferences: List[str]) -> None:
        ballot = Ballot(preferences)
        self.ballots.append(ballot)

    def count_votes(self) -> None:
        # Reset the vote counts for all candidates before counting votes
        for candidate in self.candidates.values():
            candidate.reset_vote_count()

        # Count the votes for each ballot's top choice
        for ballot in self.ballots:
            top_choice = ballot.top_choice(self.lost)
            if top_choice and top_choice in self.candidates:
                self.candidates[top_choice].increment_vote()

    def find_winner(self, total_votes: int) -> Optional[str]:
        for candidate in self.candidates.values():
            if candidate.vote_count > total_votes / 2:
                return candidate.name
        return None

    def eliminate_candidate(self) -> List[str]:
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
        while True:
            self.count_votes()
            winner = self.find_winner(total_votes)
            if winner:
                return winner

            eliminated_candidates = self.eliminate_candidate()
            if not eliminated_candidates:
                break  # In case of a tie or all candidates being eliminated

# Example usage
if __name__ == "__main__":
    candidate_names = ["Alice", "Bob", "Charlie"]
    election = Election(candidate_names)
    election.add_ballot(["Charlie", "Alice", "Bob"])
    election.add_ballot(["Bob", "Alice", "Charlie"])
    election.add_ballot(["Charlie", "Bob", "Alice"])

    winner = election.run_election()
    print(f"The winner is: {winner}")