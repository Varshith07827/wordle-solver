# Wordle Solver

A Python-based Wordle solver that helps you find the optimal word to guess based on feedback from previous attempts.

## Features

- Suggests optimal words based on letter frequency analysis
- Updates possible words based on feedback (green, yellow, gray)
- Command-line interface for easy interaction
- Efficient word filtering algorithm

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wordle-solver.git
cd wordle-solver
```

2. Make sure you have Python 3.6+ installed

3. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Run the solver:
```bash
python app.py
```

## Usage

1. The program will suggest a word to guess
2. Enter the feedback for each letter as:
   - `green` for correct letter in correct position
   - `yellow` for correct letter in wrong position
   - `gray` for letter not in the word
3. Example feedback: `green yellow gray gray gray`
4. The program will update its suggestions based on your feedback
5. Type 'quit' to exit the program

## Requirements

- Python 3.6+
- A word list file (words.txt) containing 5-letter words

## License

MIT License 