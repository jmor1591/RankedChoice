from typing import List, Dict, Optional
import random
import heapq

##TODO:
# Fix time complexities
# Fix test cases (start with changing eliminate candidate and/or run election so that if eliminate candidate list is equal
# to remaining candidate list/set? then run_election will return the eliminated candidate list.)
class Candidate:
    def __init__(self, name: str):
        self.name: str = name
        self.vote_count: int = 0

    def increment_vote(self, n: int = 1) -> None:
        self.vote_count += n

    def decrement_vote(self, n: int = 1) -> None:
        self.vote_count -= n
        
    def __repr__(self) -> str:
        return f"{self.vote_count}"

class Ballot:
    def __init__(self, preferences: List[str]):
        seen = set() #creates set so that duplicates can be identified in O(1) time
        self.preferences: List[str] = [x for x in preferences if not (x in seen or seen.add(x))] #preferences in order with no duplicates
        self.topp_choice: str = preferences[0] if preferences else None
    
    def top_choice(self, eliminated: set, candidates: set, k: int = 0) -> Optional[str]:
        """
        Returns the top valid choice from the ballot's preference list and removes any invalid choices from the list.

        This method iterates through the ballot's preferences, removing any candidates that have been eliminated 
        or are not in the list of valid candidates. It returns the k-th valid choice (0 for the top choice, 
        1 for the second choice, etc.) from the updated preferences list.

        Args:
            eliminated (set): A set of eliminated candidate names.
            candidates (set): A set of valid candidate names.
            k (int, optional): The index of the valid choice to return (0 for top choice, 1 for second choice, etc.). Defaults to 0.

        Returns:
            Optional[str]: The k-th valid candidate name from the updated preferences list, or None if no valid choice is found.
        """
        count = 0
        index = 0
        while index < len(self.preferences):
            if self.preferences[index] in eliminated or self.preferences[index] not in candidates:
                # Remove the eliminated candidate from the preferences list
                self.preferences.pop(index)
                # Do not increment index, as we need to check the new candidate at this index
            elif count == k: #if we want the top choice then k=0, if we want the second choice then k=1
                return self.preferences[index]
            else:
                count += 1
                index += 1
        return None
        
        def __repr__(self) -> str:
            return f"Ballot({self.preferences})"
        
        def __eq__(self, other):
            if isinstance(other, Ballot):
                return self.preferences == other.preferences
            return False
        
        def __hash__(self):
            return hash(tuple(self.preferences))
        
class Election:
    def __init__(self, candidate_names: List[str]):
        self.candidates: Dict[str, Candidate] = {name: Candidate(name) for name in candidate_names}
        self.ballots: Dict[Ballot, int] = {}
        self.eliminated: set = set()

    def add_ballot(self, preferences: List[str]) -> None:
        """
        Adds a ballot with the given preferences to the election.

        This method creates a Ballot object from the provided list of candidate preferences,
        adds it to the collection of ballots, and increments the vote count for the top-choice
        candidate if they have not been eliminated.

        Args:
            preferences (List[str]): A list of candidate names in order of preference.
        """
        if preferences:
            ballot = Ballot(preferences)
            top_choice = ballot.top_choice(self.eliminated,self.candidates)
            if ballot in self.ballots:
                self.ballots[ballot] += 1
            else:
                self.ballots[ballot] = 1
            #print(top_choice) #debugging
            #initial vote
            if top_choice in self.candidates:
                self.candidates[top_choice].increment_vote()

    def count_votes(self, k: int = 0) -> None:
        """
        Counts the votes for the current round of the election, redistributing votes if necessary.

        This method iterates through all ballots and counts the votes for the candidates based on the top valid 
        choice from each ballot. If the top choice of a ballot is eliminated or if k > 0 (indicating a re-evaluation 
        of choices), it finds the next valid choice and counts the vote for that candidate. Votes are incremented 
        by the count of identical ballots.

        Args:
            k (int, optional): The index of the valid choice to consider if the top choice is eliminated or 
                            if a re-evaluation is needed (0 for top choice, 1 for second choice, etc.). Defaults to 0.
        """
        for ballot, count in self.ballots.items():
            if ballot.topp_choice in self.eliminated or k > 0:
                ballot.topp_choice = ballot.top_choice(self.eliminated, self.candidates, k)
                if ballot.topp_choice is not None:
                    self.candidates[ballot.topp_choice].increment_vote(count)

    def find_winner(self, total_votes: int) -> Optional[str]:
        """
        Determines if there is a candidate who has received more than half of the total votes.

        This method iterates through all candidates and checks if any candidate has a vote count
        greater than half of the total votes cast. If such a candidate is found, their name is
        returned as the winner.

        Args:
            total_votes (int): The total number of votes cast in the election.

        Returns:
            Optional[str]: The name of the winning candidate if one is found, otherwise None.
        """
        for candidate in self.candidates.values():
            #print(candidate.vote_count) #debugging
            if candidate.vote_count > total_votes / 2:
                return candidate.name
        return None

    def find_candidates_with_min_votes(self) -> List[str]:
        """
        Finds the candidates with the minimum number of votes.

        This method determines the minimum number of votes among all candidates 
        and returns a list of candidate names who received that minimum number 
        of votes. If there are no candidates, an empty list is returned.

        Returns:
            List[str]: A list of candidate names with the minimum number of votes.
        """
        if not self.candidates:
            return []

        min_votes = min(candidate.vote_count for candidate in self.candidates.values())
        candidates_with_min_votes = [candidate_name for candidate_name, candidate in self.candidates.items() if candidate.vote_count == min_votes]
        return candidates_with_min_votes

    def eliminate_candidates(self, candidates_to_eliminate: List[str]) -> None:
        """
        Eliminates the specified candidates from the election.

        This method removes the specified candidates from the list of candidates 
        and adds their names to the set of eliminated candidates. If a candidate 
        to eliminate is not present in the list of candidates, it is ignored.

        Args:
            candidates_to_eliminate (List[str]): A list of candidate names to eliminate.
        """
        for candidate_name in candidates_to_eliminate:
            if candidate_name in self.candidates:
                del self.candidates[candidate_name]
                self.eliminated.add(candidate_name)
    
    def run_election(self) -> str:
        """
        Executes the election process and determines the winner.

        This method runs the election process until a winner is determined or 
        no winner can be found. It iterates through each round of the election, 
        counting votes, eliminating candidates with the minimum votes, and 
        adjusting the parameters for the next round if necessary. If a winner 
        is found, their name is returned as the winner. If there are remaining 
        candidates with votes, their names are joined and returned. If there 
        are no candidates or ballots, it returns "No winner".

        Returns:
            str: The name(s) of the winner(s) if found, or "No winner" if no winner 
                can be determined.
        """
        total_votes = len(self.ballots)
        if not self.ballots:
            return "No winner"

        k = 0
        max_k = k
        while True:
            max_k = max(max_k, k)
            # Debugging print statements
            #print(f"\nCount Votes with k={k}") #debugging
            self.count_votes(k)
            #print(f"Candidates after counting votes: {self.candidates}") #debugging

            winner = self.find_winner(total_votes * (2 ** max_k))
            if winner:
                return winner

            candidates_to_eliminate = self.find_candidates_with_min_votes()
            remaining_candidates = set(self.candidates.keys())

            #print(f"Remaining candidates: {remaining_candidates}") #debugging
            #print(f"Candidates to eliminate: {candidates_to_eliminate}") #debugging

            if set(candidates_to_eliminate) == remaining_candidates:
                if k < len(self.candidates) - 1:
                    k += 1
                else:
                    break
            else:
                self.eliminate_candidates(candidates_to_eliminate)
                #print(f"End Remaining candidates: {set(self.candidates.keys())}") #debugging
                k = 0

            if not self.candidates:
                break

        remaining_candidates = set(self.candidates.keys())
        if remaining_candidates:
            return ", ".join(remaining_candidates)
        return "No winner"


# Example usage
if __name__ == "__main__":
    candidate_names = ["Candidate" + str(i) for i in range(1, 6)]  # 100 candidates
    election = Election(candidate_names)
    for _ in range(1000):  # 1000 ballots
        preferences = random.sample(candidate_names, len(candidate_names))
        election.add_ballot(preferences)

    winner = election.run_election()
    print(f"The winner is: {winner}")