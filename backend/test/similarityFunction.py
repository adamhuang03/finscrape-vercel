import nltk
from nltk.corpus import wordnet

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

def generate_related_words(phrase):
    # Tokenize the phrase
    tokens = nltk.word_tokenize(phrase)
    
    related_words = []

    for token in tokens:
        # Get synonyms for each word
        synonyms = wordnet.synsets(token)
        for syn in synonyms:
            for lemma in syn.lemmas():
                related_words.append(lemma.name())
    
    # Remove duplicates and sort the list
    related_words = sorted(set(related_words))
    
    return related_words


if __name__ == '__main__':
    # Example usage
    # phrase = "machine learning"
    phrase = "Raised or someone invested more than 50 million into the company" 
    related_words = generate_related_words(phrase)
    print(related_words)
