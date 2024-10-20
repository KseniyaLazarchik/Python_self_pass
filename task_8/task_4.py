# Functions for task 2
import random
import string
from collections import defaultdict
import csv
import string
import os

# Functions for task 3
def number_of_whitespace_characters(text):
    """Count number of whitespace character in text"""

    if type(text) is str:
        whitespace_count = sum(1 for char in text if char.isspace())
        print(f"Number of whitespace character is {whitespace_count}.")
    else:
        print("Text is not a string.")
    pass


def create_new_sentence(text):
    """Create new sentence"""

    # Empty list
    last_words = []

    # Take the last word from sentence
    sentences_split = text.split('. ')
    for sentence in sentences_split:
        words = sentence.split()
        if words:
            last_words.append(words[-1])

    # Create the new sentence from the last words and capitalize it
    sentence_new = ' '.join(last_words).capitalize()
    return sentence_new


def text_normalize(text):
    """Normalize the text: handle case normalization and fix extra spaces."""

    if isinstance(text, str):
        # Replace newlines with spaces, fix extra spaces, and normalize to lowercase
        text_normal = text.replace('\n', ' ').replace('  ', ' ').lower()

        # Split sentences by period followed by a space
        sentences_split = text_normal.split('. ')

        # Capitalize the first word of each sentence
        sentences = [sentence.strip().capitalize() for sentence in sentences_split]

        # Join the sentences back together
        text_normal = '. '.join(sentences)

        return text_normal
    else:
        print("Input is not a valid string.")
        return None

def new_text_with_sentence(text):
    text_with_sentence = text_normalize(text) + create_new_sentence(text)
    return text_with_sentence


def fix_misspelling(text):
    """Fix the misspelling 'iz' with the correct 'is'."""

    # First normalize the text using text_normalize
    normalized_text = text_normalize(text)

    # List of replacements to correct "iz" to "is"
    replacements = [
        (' iz ', ' is '),
        ('“iz”', '“is”'),
        ('"iz"', '"is"')
    ]

    # Apply replacements for each case of misspelling
    result = normalized_text
    for old, new in replacements:
        result = result.replace(old, new)

    return result

def generate_word_count_csv(text, file_path='word_count.csv'):
    """Generate CSV with word counts."""
    words = text.lower().split()  # Split words and normalize to lowercase
    word_count = {}

    # Count each word
    for word in words:
        word = word.strip(string.punctuation)  # Remove punctuation around words
        if word:
            word_count[word] = word_count.get(word, 0) + 1

    # Write to CSV
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Count'])
        # Append word counts
        for word, count in word_count.items():
            writer.writerow([word, count])


def generate_letter_count_csv(text, file_path='letter_count.csv'):
    """Generate CSV with letter counts, uppercase counts, and percentage of uppercase."""
    letter_count = {letter: 0 for letter in string.ascii_lowercase}
    uppercase_count = {letter: 0 for letter in string.ascii_uppercase}

    # Count total letters and uppercase letters
    total_letters = 0
    for char in text:
        if char.isalpha():
            total_letters += 1
            lowercase_char = char.lower()
            letter_count[lowercase_char] += 1
            if char.isupper():
                uppercase_count[char] += 1


    # Write to CSV
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Letter', 'Count All', 'Count Uppercase', 'Percentage Uppercase'])

        # Write letter stats
        for letter in string.ascii_lowercase:
            count_all = letter_count[letter]
            count_uppercase = uppercase_count[letter.upper()]
            percentage = (count_uppercase / count_all * 100) if count_all > 0 else 0
            writer.writerow([letter, count_all, count_uppercase, f'{percentage:.2f}%'])