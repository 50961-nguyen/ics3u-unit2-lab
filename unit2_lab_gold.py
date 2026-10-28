"""
author: SOL
date: Oct 28, 2026
Unit 2 Lab
"""

print("Welcome to the Celebration Square Halloween Candy Crawl!")

# input
name = input("Enter your name: ")
houses = int(input("Enter the amount of houses you visited today: "))
gummy = 0
chocolate = 0
lollipop = 0
score = 0

# Processing
print(f"Great job {name}! Let's celebrate each house you visited!")

# for bronze, use the for loop to print the amount of houses visited
for i in range(1, houses):
    print(f"House {i} visited! Keep going!")
print(f"House {houses} visited! Happy Halloween!")

print("\nTime to log your candy bag!")

candy = input("Enter each candy type (or 'done' to finish): ").lower()

# While loop used to track candy type and score
while candy != "done":
    # validation loop to confirm inputs
    while candy != "chocolate" and candy != "lollipop" and candy != "gummy":
        print("Invalid input.")
        candy = input("Enter each candy type (or 'done' to finish): ").lower()

    if candy == "chocolate":
        print("A chocolate treat! What a classic!")
        chocolate += 1
        score += 10

    elif candy == "gummy":
        print("A gummy treat! Spooky and chewy!")
        gummy += 1
        score += 5
    
    else: 
        print("A lollipop! A sweet Halloween classic!")
        lollipop += 1
        score += 1
    
    candy = input("Enter each candy type (or 'done' to finish): ").lower()

# Outputs
print(f"Total candies: {lollipop+ gummy+chocolate}")
print(f"Chocolate candies: {chocolate}")
print(f"Gummy candies: {gummy}")
print(f"Lollipops: {lollipop}")
print(f"Total score: {score}")

# for bronze: print message based on number of chocolates
if chocolate >= 1:
    print(f"Amazing, {name}! You collected some chocolate!")
else: 
    print(f"No chocolate this time, {name}. Keep trick-or-treating!")

# for gold: prints message based on score
if score >= 21:
    print("Halloween Candy Champion!")
elif 16 <= score <= 20:
    print("Haunted Basket winner")
elif 11 <= score <= 15:
    print("Candy Corn Winner!")
else: 
    print("Better luck next time!")