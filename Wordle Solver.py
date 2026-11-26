import urllib.request
from collections import Counter

URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"

def load_words():
    print("loading Wordle dictionary...")

    with urllib.request.urlopen(URL) as response:
        data = response.read().decode("utf-8")

    return sorted(set(
        word.strip().upper()
        for word in data.splitlines()
        if len(word.strip()) == 5 and word.strip().isalpha()
    ))


def get_feedback(guess, answer):
    result = ["X"] * 5
    remaining = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "G"
            remaining[i] = None

    for i in range(5):
        if result[i] == "X" and guess[i] in remaining:
            result[i] = "Y"
            remaining[remaining.index(guess[i])] = None

    return "".join(result)


def suggest_word(words):
    if not words:
        return None

    frequencies = Counter(
        letter
        for word in words
        for letter in set(word)
    )

    return max(
        words,
        key=lambda word: sum(frequencies[c] for c in set(word))
    )


def solve():
    words = load_words()

    print(f"Loaded {len(words)} valid words!")
    print("\n=== WORDLE SOLVER ===")
    print("G = Green | Y = Yellow | X = Grey")
    print("Type QUIT to stop.")

    while len(words) > 1:

        print(f"\n{len(words)} possible words remaining")
        print(f"Suggested guess: {suggest_word(words)}")

        guess = input("\nEnter your guess: ").upper()

        if guess == "QUIT":
            break

        if len(guess) != 5 or not guess.isalpha():
            print("Enter a valid 5-letter word.")
            continue

        if guess not in words:
            print("That word isn't in the loaded dictionary.")
            continue

        feedback = input(
            "Enter the colours (e.g. GYXGX): "
        ).upper()

        if len(feedback) != 5 or any(
            c not in "GYX" for c in feedback
        ):
            print("Invalid colour pattern.")
            continue

        remaining = [
            word for word in words
            if get_feedback(guess, word) == feedback
        ]

        if not remaining:
            print("No matching words found. Check your colours.")
            continue

        words = remaining
        print("\nPossible words:")
        print(", ".join(words))

    if len(words) == 1:
        print(f"\nANSWER: {words[0]}")

    elif len(words) == 0:
        print("\nNo possible answers remain.")
    else:
        print(f"\nRemaining words: {', '.join(words)}")
if __name__ == "__main__":
    solve()
