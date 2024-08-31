# Functions for task 2
import random
import string
from collections import defaultdict


def generate_random_dicts():
    """Generate a list of random number of dictionaries (from 2 to 10)
    with random letters as keys and random numbers (0-100) as values."""

    # Generate a random number of dictionaries (between 2 and 10)
    num_dicts = random.randint(2, 10)

    # Initialize an empty list to hold the dictionaries
    dict_list = []

    for i in range(num_dicts):
        # Generate a random number of keys for each dictionary (between 1 and 5)
        num_keys = random.randint(1, 5)

        # Generate random letters as keys
        keys = random.sample(string.ascii_lowercase, num_keys)

        # Create a dictionary with random keys and random values (0-100)
        random_dict = {key: random.randint(0, 100) for key in keys}

        # Append the generated dictionary to the list
        dict_list.append(random_dict)

    return dict_list


def create_common_dict(dict_list):
    """Create a common dictionary from a list of dictionaries,
    taking the max value if keys are repeated and renaming them appropriately."""

    # Create a dictionary to store the max values and corresponding dictionary index
    merged_dict = defaultdict(lambda: (0, 0))

    # Count of dictionary iterations
    for i, d in enumerate(dict_list, start=1):
        # Go through dictionary items
        for key, value in d.items():
            # If key already exists, compare values
            if value > merged_dict[key][0]:
                merged_dict[key] = (value, i)
            elif key not in merged_dict:
                merged_dict[key] = (value, i)

    # Create the final dictionary with keys renamed according to the rules
    final_dict = {}
    for key, (value, idx) in merged_dict.items():
        new_key = f"{key}_{idx}" if len([d for d in dict_list if key in d]) > 1 else key
        final_dict[new_key] = value

    return final_dict


# Generate a list of random number of dictionaries
print(f"Generated List of Dictionaries: {generate_random_dicts()}")

# Create a common dictionary from a list of dictionaries
print(f"Common Dictionary: {create_common_dict(generate_random_dicts())}")


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
    """Normalize the text"""

    if type(text) is str:
        # Delete extra whitespaces and normalize all letter to lowercase
        text_normal = text.replace('\n', ' ').replace('“', ' “').replace('  ', ' ').lower()

        # Split sentences
        sentences_split = text_normal.split('. ')

        # Capitalize first words in sentences
        sentences = [sentence.strip().capitalize() for sentence in sentences_split]

        # Join sentences
        text_normal = '. '.join(sentences)

        # Add new sentence from create_new_sentence to the text
        text_new = text_normal + create_new_sentence(text)

    else:
        print("Text is not a string.")
        text_new = None

    return text_new


def fix_misspelling():
    """Fix misspelling iz with correct is"""

    # Get the normalized text
    text_new = text_normalize(text)

    # Fix “iz” with correct “is”, when “iz” surrounded by spaces and special characters
    replacements = [
        (' iz ', ' is '),
        ('“iz”', '“is”'),
        ('"iz"', '"is"')
    ]

    # Apply all replacements
    result = text_new
    for old, new in replacements:
        result = result.replace(old, new)

    return result


text = """
 tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces.
"""

# Calculate number of whitespace characters
number_of_whitespace_characters(text)
# Create new sentence
print(create_new_sentence(text))
# Text normalize and add new sentence to text
print(text_normalize(text))
# Fix iz to is
print(fix_misspelling())
