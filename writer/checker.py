import time
import re
from collections import Counter

class SimpleChecker:
    def __init__(self):
        # A small list of common words. In a real application, you'd want a more comprehensive list.
        self.words = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'])
        self.word_counts = Counter(self.words)

    def correct_spelling(self, word):
        if word.lower() in self.words:
            return word
        # Simple spell correction
        return min(self.words, key=lambda w: self._edit_distance(word, w))

    def _edit_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def check_grammar(self, sentence):
        # Very basic grammar rules
        words = sentence.split()
        corrections = []
        for i, word in enumerate(words):
            # Check for repeated words
            if i > 0 and word.lower() == words[i-1].lower():
                corrections.append((i, f"Repeated word: {word}"))
            # Check for "a" vs "an"
            if word.lower() == 'a' and i < len(words) - 1:
                if words[i+1][0].lower() in 'aeiou':
                    corrections.append((i, f"'a' should be 'an' before '{words[i+1]}'"))
        return corrections

    def correct_text(self, text):
        sentences = re.split('([.!?] *)', text)
        corrected_sentences = []
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            words = sentence.split()
            corrected_words = [self.correct_spelling(word) for word in words]
            corrected_sentence = ' '.join(corrected_words)
            grammar_corrections = self.check_grammar(corrected_sentence)
            for j, correction in grammar_corrections:
                print(f"Grammar suggestion: {correction}")
            if i + 1 < len(sentences):
                corrected_sentences.append(corrected_sentence + sentences[i+1])
            else:
                corrected_sentences.append(corrected_sentence)
        return ''.join(corrected_sentences)

def test_simple_checker(text):
    checker = SimpleChecker()
    start_time = time.time()
    corrected = checker.correct_text(text)
    end_time = time.time()
    return corrected, end_time - start_time

def show_corrections(original, corrected):
    print("Original : ", original)
    print("Corrected: ", corrected)
    print("Changes  : ", end="")
    for orig, corr in zip(original.split(), corrected.split()):
        if orig != corr:
            print(f"{orig}->{corr} ", end="")
    print("\n")

def main():
    test_text = "This is a smple text with som mispeled words. It also has grammer mistakes and runing words. I am am writing a book."
    
    print("Testing Simple checker:")
    result, duration = test_simple_checker(test_text)
    show_corrections(test_text, result)
    print(f"Time taken: {duration:.4f} seconds")

if __name__ == "__main__":
    main()