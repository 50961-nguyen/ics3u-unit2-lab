# Unit 2 Lab: Halloween Candy Crawl Edition

## Description

In this lab, you will create a Python program that simulates a Halloween trick-or-treat candy crawl at Celebration Square. You will use `for` loops, `while` loops, variables, and conditionals to track houses visited, collect candy, and calculate prizes.

This lab assesses your understanding of loops and how they work with variables and conditions.

Choose one of three challenge tiers: Bronze, Silver, or Gold. Each tier builds on the previous one.

Make sure you inclulde IPO comments, header comments with your name, and some general comments to explain the conditionals/loops in your code (1-2 sentences). 

You do not need to write IPO for each tier - just include it once in your code and organize your code based on order of the tier.

## Submission Instructions

Submit your Python file as `unit1_lab_tier.py` (for example, `unit1_lab_gold.py`) via GitHub.

## Bronze Tier — Max Grade of 70%

### Tasks

- Use `print()` to greet the user:
  - `Welcome to the Celebration Square Halloween Candy Crawl!`
- Use `input()` to ask for the user's name and how many houses they visited trick-or-treating (as an integer).
- Print a message using those variables.
- Use a `for` loop to celebrate visiting each house:
  - For every house except the last, print `House X visited! Keep going!`.
  - For the last house, print `House X visited! Happy Halloween!`.

### Sample Output

```text
Welcome to the Celebration Square Halloween Candy Crawl!
Enter your name: Alex
Enter the amount of houses you visited today: 3
Great job Alex! Let's celebrate each house you visited!
House 1 visited! Keep going!
House 2 visited! Keep going!
House 3 visited! Happy Halloween!
```

## Silver Tier — Max Grade of 85%

### Tasks

- Complete all Bronze tasks.
- Print `\nTime to log your candy bag!`.
- Ask the user to enter each candy type one at a time and type `done` when finished (case-sensitive).
- Use a `while` loop with the sentinel value `done` to collect candy types. Keep a counter for total candies and chocolate candies.
- Inside the loop:
  - If the candy is `chocolate`(case-sensitive), print `A chocolate treat! What a classic!` and add to the chocolate count.
  - Otherwise, print `A {candy} treat added to your bag!`. Add to candy count.
- After the loop, print a candy bag summary:
  - Total candies collected: X
  - Chocolate candies: X
- Use a conditional:
  - If the chocolate count is greater than 0, print `Amazing, {name}! You collected some chocolate!`.
  - Otherwise, print `No chocolate this time, {name}. Keep trick-or-treating!`.

### Sample Output for Silver

```text
Welcome to the Celebration Square Halloween Candy Crawl!
Enter your name: Alex
Enter the amount of houses you visited today: 3
Great job Alex! Let's celebrate each house you visited!
House 1 visited! Keep going!
House 2 visited! Keep going!
House 3 visited! Happy Halloween!

Time to log your candy bag!
Enter each candy type (or 'done' to finish): gummy
A gummy treat added to your bag!
Enter each candy type (or 'done' to finish): chocolate
A chocolate treat! What a classic!
Enter each candy type (or 'done' to finish): done
Total candies: 2
Chocolate candies: 1
Amazing, Alex! You collected some chocolate!
```

## Gold Tier — Max Grade of 100%
**Note:** You are on your own for programming the Gold conditions!

### Tasks

- Complete all Bronze and Silver tasks.
- Modify the loop from Silver tier to track points. Capitalized words are now valid inputs, including the sentinel value.
- Update the inside of the loop:
  - First, validate the input by only accepting `chocolate`, `gummy`, or `lollipop`. Keep asking the user for input until they type one of those three options.
  - If the candy is `chocolate`, print `A chocolate treat! What a classic!`, add to the chocolate count, and increase the points by 10.
  - If the candy is `gummy`, print `A gummy treat! Spooky and chewy!`, add to the gummy count, and increase the points by 5.
  - If the candy is `lollipop`, print `A lollipop! A sweet Halloween classic!`, add to the lollipop count, and increase the points by 1.
- After the loop, print:
  - Haunted Candy Bag Summary:
  - Total candies: X
  - Chocolate candies: X
  - Gummy candies: X
  - Lollipops: X
  - Your total score: X points
- Print the prize tier based on total score:
  - Less than 10: `Better luck next time!`
  - 11–15: `Candy Corn winner!`
  - 16–20: `Haunted Basket winner!`
  - 21 or more: `Halloween Candy Champion!`

### Sample Output for Gold

```text
Welcome to the Celebration Square Halloween Candy Crawl!
Enter your name: Alex
Enter the amount of houses you visited today: 3
Great job Alex! Let's celebrate each house you visited!
House 1 visited! Keep going!
House 2 visited! Keep going!
House 3 visited! Happy Halloween!

Time to log your candy bag!
Enter each candy type (or 'done' to finish): chocolate
A chocolate treat! What a classic!
Enter each candy type (or 'done' to finish): gummy
A gummy treat! Spooky and chewy!
Enter each candy type (or 'done' to finish): blue
Invalid input.
Enter each candy type (or 'done' to finish): lollipop
A lollipop! A sweet Halloween classic!
Enter each candy type (or 'done' to finish): done
Total candies: 3
Chocolate candies: 1
Gummy candies: 1
Lollipops: 1
Total score: 16
Amazing, Alex! You collected some chocolate!
Haunted Basket winner!
```
