#input: list of ballots
#output: winning candidate


#count first choice votes for each candidate

#check if any candidate has more than half the votes

#if no candidate has more than half, then you remove the candidate with least amount of votes

#redistribute the votes by removing the eliminated candidate and count new first choice votes

#display that candidates ranking

#continue process until winner is found

from typing import List, Dict, Optional

class Candidate:
    def __init__(self, name: str):
        self.name: str = name
        self.vote_count: int = 0

    def increment_vote(self) -> None:
        self.vote_count += 1

class Ballot:
    def __init__(self,preferences: List[str]):
        self.preferences: List[str] = preferences
    
    def remove_candidate(self, candidate_name: str) -> None:
        if candidate_name in self.preferences:
            self.preferences.remove(candidate_name)
    
    def top_choice(self, eliminated: List[str]) -> Optional[str]:
        for i, preference in enumerate(self.preferences):
            if preference not in eliminated:
                return preference
            # If the current preference is eliminated, remove it from preferences
            self.remove_candidate(preference)
            # Since we removed an element, adjust the index to prevent skipping elements
            # Subtract 1 from the index to recheck the current position in the updated list
            i -= 1
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
        for ballot in self.ballots:
            top_choice = ballot.top_choice(self.lost)
            if top_choice in self.candidates:
                self.candidates[top_choice].increment_vote()
            else:
                print("Error in count_votes")
    
    def find_winner(self, total_votes: int) -> Optional[str]:
        for candidate in self.candidates.values():
            if candidate.vote_count > total_votes / 2:
                return candidate.name
        return None
    
    """
    Fix the tie-breaking problem
    """
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
        i = 0
        while True and i < 100:
            self.count_votes()
            winner = self.find_winner(len(self.ballots))
            if winner:
                return winner

            #eliminated_candidate = self.eliminate_candidate()
            i += 1

# Example usage
if __name__ == "__main__":
    candidate_names = ["Alice", "Bob", "Charlie"]
    election = Election(candidate_names)
    election.add_ballot(["Charlie", "Bob", "Alice"])
    election.add_ballot(["Bob", "Charlie", "Alice"])
    election.add_ballot(["Bob", "Charlie", "Alice"])
    election.add_ballot(["Alice", "Charlie", "Bob"])
    election.add_ballot(["Charlie", "Bob", "Alice"])
    election.add_ballot(["Charlie", "Bob", "Alice"])

    winner = election.run_election()

    print(f"The winner is: {winner}")
