import json
from collections import Counter
import re

# Load the corpus
with open('kannada_corpus.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

# Create a frequency dictionary
word_freq = Counter(words)

# Function to preprocess and clean a word
def preprocess_word(word):
    return re.sub(r'[^ಀ-೿a-zA-Z]', '', word).lower()

# Function to get words with a given edit distance
def edits1(word):
    letters = 'ಅಆಇಈಉಊಋಎಏಐಒಓಔಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲವಶಷಸಹಳಕ್ಷ'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

# Function to generate candidate corrections
def candidates(word):
    return (known([word]) or known(edits1(word)) or [word])

# Function to filter known words
def known(words):
    return set(w for w in words if w in word_freq)

# Function to correct a word
def correct(word):
    word = preprocess_word(word)
    return max(candidates(word), key=word_freq.get)

# Test the spell checker
test_words = ["ಕನ್ನಡ","ಕನಡಾ", "ಅಭಿನಂದನೆ","ಅಭಿನಂದನೆ", "ಪದಗಳು","ಪಾದಗಳು"]  # Add some test words
for word in test_words:
    print(f"{word} -> {correct(word)}")
