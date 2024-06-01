import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def generate_related_words(phrase):
    # Tokenize the phrase
    tokens = word_tokenize(phrase)
    stop_words = set(stopwords.words('english'))
    
    # Filter out stop words and non-alphabetic tokens
    filtered_tokens = [token for token in tokens if token.isalpha() and token.lower() not in stop_words]

    related_words = []

    for token in filtered_tokens:
        # Get synonyms for each word
        synonyms = wordnet.synsets(token)
        for syn in synonyms:
            for lemma in syn.lemmas():
                related_words.append(lemma.name())
                
        # Add the original word to related words to maintain context
        related_words.append(token)
    
    # Remove duplicates and sort the list
    related_words = sorted(set(related_words))
    
    return related_words


if __name__ == '__main__':
    # Example usage
    # phrase = "machine learning"
    phrase = "Raised or someone invested more than 50 million into the company" 
    related_words = generate_related_words(phrase)
    print(related_words)
