from typing import List, Dict, Optional
import heapq

##TODO:
# Fix time complexities
# Fix test cases (start with changing eliminate candidate and/or run election so that if eliminate candidate list is equal
# to remaining candidate list/set? then run_election will return the eliminated candidate list.)
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
        self.topp_choice: str = preferences[0] if preferences else None

    def top_choice(self, eliminated: set) -> Optional[str]:
        # Loop through the preferences and remove any eliminated candidates
        while self.current_index < len(self.preferences):
            if self.preferences[self.current_index] in eliminated:
                # Remove the eliminated candidate from the preferences list
                self.preferences.pop(self.current_index)
            else:
                # Return the first non-eliminated candidate
                return self.preferences[self.current_index]
        # Return None if all candidates are eliminated
        return None
    
    def top_choice(self, eliminated: set, k: int = 0) -> Optional[str]:
        count = 0
        index = 0
        while index < len(self.preferences):
            if self.preferences[index] in eliminated:
                # Remove the eliminated candidate from the preferences list
                self.preferences.pop(index)
                # Do not increment index, as we need to check the new candidate at this index
            elif count == k:
                return self.preferences[index]
            else:
                count += 1
                index += 1
        return None
        
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

    def count_votes(self, k: int = 0) -> None:
        for ballot in self.ballots:
            old_top = ballot.topp_choice
            new_choice = ballot.top_choice(self.eliminated,k)
            if old_top != new_choice and new_choice in self.candidates:
                self.candidates[new_choice].increment_vote()

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
    
    """
    def run_election(self) -> str:
        total_votes = len(self.ballots)
        if not self.ballots:
            return "No winner"
        for _ in range(len(self.candidates)):
            self.count_votes()
            winner = self.find_winner(total_votes)
            if winner:
                return winner
            eliminated_candidates = self.eliminate_candidate()
            remaining_candidates = set(self.candidates.keys())
            #print("Eliminated candidates:", eliminated_candidates) #debugging
            #print("Remaining candidates:", remaining_candidates) #debugging
            if not eliminated_candidates:
                break  # No candidates left to eliminate
            if not remaining_candidates:  # Check if there are no remaining candidates
                return ", ".join(eliminated_candidates)  # Return tied candidates as winners
        return "No winner"
    """
    def run_election(self) -> str:
        total_votes = len(self.ballots)
        if not self.ballots:  # Check if there are any ballots
            return "No winner"
        for _ in range(len(self.candidates)):
            self.count_votes()
            winner = self.find_winner(total_votes)
            if winner:
                return winner
            eliminated_candidates = self.eliminate_candidate()
            remaining_candidates = set(self.candidates.keys())
            print("Eliminated candidates:", eliminated_candidates)  # Debugging print statement
            print("Remaining candidates:", remaining_candidates)  # Debugging print statement
            if not eliminated_candidates:
                break  # No candidates left to eliminate
            if not remaining_candidates:  # Check if there are no remaining candidates
                if eliminated_candidates:
                    print("No remaining candidates. Returning tied candidates as winners.")  # Debugging print statement
                    return ", ".join(eliminated_candidates)  # Return tied candidates as winners
        return "No winner"
  
"""  
# Example usage
if __name__ == "__main__":
    candidate_names = ["Alice", "Bob", "Charlie"]
    election = Election(candidate_names)
    election.add_ballot([])
    election.add_ballot([])
    election.add_ballot(["Charlie, Alice"])

    winner = election.run_election()
    print(f"The winner is: {winner}")

"""