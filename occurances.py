import nltk
import re
import matplotlib.pyplot as plt

# Open the file with character names
with open('characters.txt', 'r', encoding='utf-8') as f:
    characters = [line.lower().strip().split(',') for line in f]

# Initialize a dictionary to store character counts
character_counts = {character_list[0]: 0 for character_list in characters}

# Open the second file
with open('count_of_monte_cristo.txt', 'r', encoding='utf-8') as f:
    # Read the entire file content
    text = f.read().lower()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)

# For each sentence, check if any of the aliases are in the sentence
for sentence in sentences:
    for character_list in characters:
        if any(alias in sentence for alias in character_list):
            character_counts[character_list[0]] += 1

# Print the counts
for character, count in character_counts.items():
    print(f'{character}: {count}')

# Generate a bar chart
plt.bar(character_counts.keys(), character_counts.values())
plt.xlabel('Character')
plt.ylabel('Count')
plt.title('Character Counts')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust subplot parameters to give specified padding
plt.savefig('character_counts.png')  # Save the figure as a .png file
plt.show()  # Display the figure