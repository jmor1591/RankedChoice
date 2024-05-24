from itertools import permutations
from typing import List

def generate_permutations(candidates: List[str]) -> List[List[str]]:
    return [list(perm) for perm in permutations(candidates)]

# Example usage:
if __name__ == "__main__":
    candidates = ["Alice", "Bob", "Charlie"]
    permutations_list = generate_permutations(candidates)
    print(permutations_list)