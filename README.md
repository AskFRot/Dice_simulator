# Dice Simulation Project

This project simulates d20 dice rolls with advantage and disadvantage, i.e., reaching a target number when rolling two dice, with the following conditions:
Advantage (i.e. two dice and as long as one is greater than or equal to the target it succeeds).
Disadvantage (i.e. two dice and as long as one is less than the target it fails).
I have also included a standard roll (i.e., a normal roll with one die) in the plots and tables produced.

The script includes two simulations, as well as a script for calculating the actual distribution of the probabilities.
This is because I wanted to take another shot at the simulation. Instead of creating the bins for disadvantage and advantage at the same time and using a while loop, so I wanted to rewrite it all. Furthermore, the previous method was a struggle to get properly working at first, and I was iterating through the results quite unefficient before I cleaned it up a bit. However, it isnt as flexible as I'd like. Where I to add another variable, like more dice, I'd have rewrite the entierty, and it only does d20s.

## Solutions:
- **Subpar Solution**: The initial version of the code used a `while True` loop and `index()` to calculate the cumulative distribution.
- **Improved Solution**: More efficient and flexible, using function calls to simulate a given number of dice rolls. Easier to extend to different dice or conditions.

## Installation:
Install dependencies:

```bash
pip install numpy pandas matplotlib
