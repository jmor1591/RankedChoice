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
        
    def __repr__(self) -> str:
        return f"{self.name}: {self.vote_count}"

class Ballot:
    def __init__(self, preferences: List[str]):
        self.preferences: List[str] = preferences if preferences else None
        self.topp_choice: str = preferences[0] if preferences else None
    
    def top_choice(self, eliminated: set, candidates: set, k: int = 0) -> Optional[str]:
        count = 0
        index = 0
        while index < len(self.preferences):
            if self.preferences[index] in eliminated or self.preferences[index] not in candidates:
                # Remove the eliminated candidate from the preferences list
                self.preferences.pop(index)
                # Do not increment index, as we need to check the new candidate at this index
            elif count == k:
                return self.preferences[index]
            else:
                count += 1
                index += 1
        return None
        
        def __repr__(self) -> str:
            return f"Ballot({self.preferences})"
        
class Election:
    def __init__(self, candidate_names: List[str]):
        self.candidates: Dict[str, Candidate] = {name: Candidate(name) for name in candidate_names}
        self.ballots: List[Ballot] = []
        self.eliminated: set = set()

    def add_ballot(self, preferences: List[str]) -> None:
        if preferences:
            ballot = Ballot(preferences)
            self.ballots.append(ballot)
            top_choice = ballot.top_choice(self.eliminated,self.candidates)
            #print(top_choice) #debugging
            #initial vote
            if top_choice in self.candidates:
                self.candidates[top_choice].increment_vote()

    def count_votes(self, k: int = 0) -> None:
        """
        Counts the votes by looking at each top choice and adds. Redistributes votes
        if top choice of the ballot is in eliminated/got eliminated.
        """
        for ballot in self.ballots:
            if ballot.topp_choice in self.eliminated or k > 0:
                ballot.topp_choice = ballot.top_choice(self.eliminated, self.candidates, k)
                if ballot.topp_choice is not None:
                    self.candidates[ballot.topp_choice].increment_vote()

    def find_winner(self, total_votes: int) -> Optional[str]:
        for candidate in self.candidates.values():
            #print(candidate.vote_count) #debugging
            if candidate.vote_count > total_votes / 2:
                return candidate.name
        return None

    def find_candidates_with_min_votes(self) -> List[str]:
        if not self.candidates:
            return []

        min_votes = min(candidate.vote_count for candidate in self.candidates.values())
        candidates_with_min_votes = [candidate_name for candidate_name, candidate in self.candidates.items() if candidate.vote_count == min_votes]
        return candidates_with_min_votes

    def eliminate_candidates(self, candidates_to_eliminate: List[str]) -> None:
        for candidate_name in candidates_to_eliminate:
            if candidate_name in self.candidates:
                del self.candidates[candidate_name]
                self.eliminated.add(candidate_name)
    
    def run_election(self) -> str:
        total_votes = len(self.ballots)
        if not self.ballots:
            return "No winner"

        k = 0
        max_k = k
        while True:
            max_k = max(max_k, k)
            # Debugging print statements
            print(f"\nCount Votes with k={k}")
            self.count_votes(k)
            print(f"Candidates after counting votes: {self.candidates}")

            winner = self.find_winner(total_votes * (2 ** max_k))
            if winner:
                return winner

            candidates_to_eliminate = self.find_candidates_with_min_votes()
            remaining_candidates = set(self.candidates.keys())

            print(f"Remaining candidates: {remaining_candidates}")
            print(f"Candidates to eliminate: {candidates_to_eliminate}")

            if set(candidates_to_eliminate) == remaining_candidates:
                if k < len(self.candidates) - 1:
                    k += 1
                else:
                    break
            else:
                self.eliminate_candidates(candidates_to_eliminate)
                print(f"End Remaining candidates: {set(self.candidates.keys())}")
                k = 0

            if not self.candidates:
                break

        remaining_candidates = set(self.candidates.keys())
        if remaining_candidates:
            return ", ".join(remaining_candidates)
        return "No winner"

"""  
# Example usage
if __name__ == "__main__":
    candidate_names = ["Alice", "Bob", "Charlie", "Evan"]
    election = Election(candidate_names)
    election.add_ballot(["Alice", "Bob", "Charlie", "Evan"])
    election.add_ballot(["Bob", "Alice", "Charlie", "Evan"])
    election.add_ballot(["Charlie", "Bob", "Alice", "Evan"])
    election.add_ballot(["Evan", "Alice", "Charlie", "Bob"])
    election.add_ballot(["Bob", "Charlie", "Alice", "Evan"])
    election.add_ballot(["Alice", "Charlie", "Bob", "Evan"])

    winner = election.run_election()
    print(f"The winner is: {winner}")
"""