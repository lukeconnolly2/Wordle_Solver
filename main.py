import collections
import queue
import list_of_words

class Wordle_words:
    words = list_of_words.words
    used_letters = []
    current_used_letters = []

    def add_letters(self, letters: list):
        self.used_letters = self.used_letters + letters
        self.current_used_letters = letters

    def num_of_non_black_letters(self):
        num = 0
        for letter in self.current_used_letters:
            if letter.colour == "BLACK":
                continue
            num += 1
        return num

    def remove_all_words_with_character(self, character: str):
        self.words = [word for word in self.words if character not in word]

    def remove_all_words_with_character_not_in_correct_position(self, character: str, position: int):
        self.words = [word for word in self.words if word[position] == character]

    def remove_all_words_without_character(self, character: str):
        self.words = [word for word in self.words if character in word]

    def remove_all_words_with_character_in_wrong_position(self, character: str, position: int):
        self.words = [word for word in self.words if word[position] != character]

    def most_common_letters(self):
        string_of_all_words = "".join(self.words)
        most_common_letters = collections.Counter(string_of_all_words).most_common()
        for i in range(self.num_of_non_black_letters()):
            most_common_letters.pop(0)
        return most_common_letters

    def best_word_choice(self):
        dictionary_of_most_common_letters = dict(self.most_common_letters())
        pq = queue.PriorityQueue()

        for word in self.words:
            score = 0
            used_letters = set()
            for letter in word:
                if dictionary_of_most_common_letters.get(letter) == None:
                    continue
                if used_letters.__contains__(letter):
                    continue
                used_letters.add(letter)
                score += dictionary_of_most_common_letters.get(letter)
            pq.put((-1 * score, word))
        top_word = pq.get()
        if top_word[0] == -1:
            return "Down to luck"
        return f"Best guess is: {top_word[1]}"


class Letter:
    character = None
    possible_positions = [True, True, True, True, True]
    colour = None

    def __init__(self, character):
        self.character = character.lower().strip()

    def yellow_position(self, position):
        self.possible_positions[position] = False
        self.colour = "YELLOW"

    def green_position(self, position):
        self.reset_possible_positions()
        self.colour = "GREEN"
        self.possible_positions[position] = True

    def reset_possible_positions(self):
        self.colour = "BLACK"
        self.possible_positions = [False, False, False, False, False]


def main():
    possible_words = Wordle_words()

    while True:
        letters = user_input()
        possible_words.add_letters(letters)

        remove_impossible_words(letters, possible_words)
        print(f"Possible words: {possible_words.words}" )
        print(possible_words.best_word_choice())


def remove_impossible_words(letters: list, possible_words: Wordle_words):
    for letter, i in zip(letters, range(5)):
        # Black letters
        if letter.colour == "BLACK":
            possible_words.remove_all_words_with_character(letter.character)
        # Green letters
        elif letter.colour == "GREEN":
            possible_words.remove_all_words_with_character_not_in_correct_position(letter.character, i)

        elif letter.colour == "YELLOW":
            possible_words.remove_all_words_without_character(letter.character)
            possible_words.remove_all_words_with_character_in_wrong_position(letter.character, i)
        else:
            raise Exception
    return


def user_input():
    while True:
        guess = [*input("Enter your guess: ")]
        if len(guess) == 5:
            break
        print("Invalid Guess!")

    while True:
        colours = [*input("Enter the colours of the letters: (B/Y/G) eg. BYYGB: ").upper()]
        if len(colours) == 5:
            break
        print("Invalid colours")

    letters = []
    for (i, letter, colour) in zip(range(5), guess, colours):
        l = Letter(letter)
        if colour == "B":
            l.reset_possible_positions()
        if colour == "Y":
            l.yellow_position(i)
        if colour == "G":
            l.green_position(i)

        letters.append(l)

    return letters


if __name__ == '__main__':
    main()
