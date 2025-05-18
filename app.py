import random
from typing import List, Dict, Set
from collections import Counter
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class WordleSolver:
    def __init__(self, word_list: List[str]):
        self.word_list = [word.lower() for word in word_list if len(word) == 5]
        self.possible_words = set(self.word_list)
        self.letter_frequencies = self._calculate_letter_frequencies()
        
    def _calculate_letter_frequencies(self) -> Dict[str, float]:
        """Calculate the frequency of each letter in the word list."""
        all_letters = ''.join(self.word_list)
        letter_counts = Counter(all_letters)
        total_letters = len(all_letters)
        return {letter: count/total_letters for letter, count in letter_counts.items()}
    
    def _word_score(self, word: str) -> float:
        """Calculate a score for a word based on letter frequencies."""
        return sum(self.letter_frequencies.get(letter, 0) for letter in set(word))
    
    def get_best_guess(self) -> str:
        """Get the best word to guess based on current information."""
        if not self.possible_words:
            return ""
        return max(self.possible_words, key=self._word_score)
    
    def update_with_feedback(self, guess: str, feedback: List[str]):
        """
        Update possible words based on feedback from a guess.
        feedback should be a list of 5 strings: 'green', 'yellow', or 'gray'
        """
        new_possible_words = set()
        
        for word in self.possible_words:
            if self._is_word_possible(word, guess, feedback):
                new_possible_words.add(word)
        
        self.possible_words = new_possible_words
        # Update letter frequencies based on remaining possible words
        self.letter_frequencies = self._calculate_letter_frequencies()
    
    def _is_word_possible(self, word: str, guess: str, feedback: List[str]) -> bool:
        """Check if a word is possible given the guess and feedback."""
        # Create a copy of the word to track used letters
        word_chars = list(word)
        
        # First pass: check green letters (correct position)
        for i, (g_char, f) in enumerate(zip(guess, feedback)):
            if f == 'green':
                if word[i] != g_char:
                    return False
                word_chars[i] = None  # Mark this position as used
        
        # Second pass: check yellow letters (wrong position)
        for i, (g_char, f) in enumerate(zip(guess, feedback)):
            if f == 'yellow':
                if g_char not in word_chars:
                    return False
                # Find the first occurrence of the letter that isn't in a green position
                for j, w_char in enumerate(word_chars):
                    if w_char == g_char:
                        word_chars[j] = None
                        break
        
        # Third pass: check gray letters (not in word)
        for i, (g_char, f) in enumerate(zip(guess, feedback)):
            if f == 'gray':
                if g_char in word_chars:
                    return False
        
        return True

def load_word_list(filename: str) -> List[str]:
    """Load a list of words from a file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

# Initialize the solver
try:
    word_list = load_word_list('words.txt')
    solver = WordleSolver(word_list)
except FileNotFoundError:
    print("Error: words.txt file not found. Please provide a word list file.")
    solver = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_guess', methods=['GET'])
def get_guess():
    if not solver:
        return jsonify({'error': 'Word list not loaded'}), 500
    guess = solver.get_best_guess()
    return jsonify({'guess': guess.upper()})

@app.route('/update_feedback', methods=['POST'])
def update_feedback():
    if not solver:
        return jsonify({'error': 'Word list not loaded'}), 500
    
    data = request.get_json()
    guess = data.get('guess', '').lower()
    feedback = data.get('feedback', [])
    
    if len(feedback) != 5 or not all(f in ['green', 'yellow', 'gray'] for f in feedback):
        return jsonify({'error': 'Invalid feedback'}), 400
    
    solver.update_with_feedback(guess, feedback)
    return jsonify({
        'remaining_words': len(solver.possible_words),
        'next_guess': solver.get_best_guess().upper()
    })

if __name__ == "__main__":
    app.run(debug=True)
