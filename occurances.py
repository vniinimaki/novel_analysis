import nltk
import re

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
