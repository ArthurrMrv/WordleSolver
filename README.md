# Wordle Solver

## Overview

This Python script provides a solver for the game Wordle. Wordle is a word puzzle game where players try to guess a hidden word by submitting guesses, and receiving feedback on the correctness of their guesses.

This solver script aims to efficiently guess the hidden word by analyzing feedback from previous guesses and narrowing down the possibilities based on the given constraints.

## Features

- **WordleSolver Class**: Defines a WordleSolver class that encapsulates the logic for analyzing feedback and generating the next guess.
- **Play Function**: Includes a function `playOnce` to play the game once, providing the hidden word and optionally the starting word.
- **Evaluation Function**: Provides a function `evaluateModel` to evaluate the performance of the solver by playing the game multiple times.

## Requirements

- Python 3.x
- pandas library

## Usage

1. **Clone the Repository**: Clone this repository to your local machine.

   ```bash
   git clone https://github.com/ArthurrMrv/WordleSolver.git
   ```

2. **Install Dependencies**: Install the required dependencies using pip.

   ```bash
   pip install pandas
   ```

3. **Run the Script**: Run the script and start playing Wordle!

   ```bash
   python wordle_solver.py
   ```

4. **Optional Configuration**: You can configure the solver by modifying the parameters in the `WordleSolver` class constructor or by passing arguments to the `playOnce` or `evaluateModel` functions.

## Example Usage

```python
# Import the WordleSolver class and utility functions
from wordle_solver import WordleSolver, playOnce, evaluateModel

# Create a WordleSolver object
solver = WordleSolver()

# Play the game once
playOnce(wordToFind="apple")

# Evaluate the solver's performance
score = evaluateModel(iters=100, wordToFind="banana")
print("Average score:", score)
```

## Contributing

Contributions are welcome! If you'd like to improve the solver or add new features, feel free to submit a pull request.
