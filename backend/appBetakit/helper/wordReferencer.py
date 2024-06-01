# From similarityFunctionNew2.py
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def get_wordnet_pos(treebank_tag):
    """Convert treebank POS tags to WordNet POS tags."""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def generate_related_words(phrase):
    # Tokenize the phrase
    tokens = word_tokenize(phrase)
    stop_words = set(stopwords.words('english'))
    
    # Filter out stop words and non-alphabetic tokens
    filtered_tokens = [token for token in tokens if token.isalpha() and token.lower() not in stop_words]

    # Part-of-speech tagging
    pos_tags = pos_tag(filtered_tokens)
    
    related_words = []

    for token, pos in pos_tags:
        wn_pos = get_wordnet_pos(pos) or wordnet.NOUN
        # Get synonyms for each word based on its POS tag
        synonyms = wordnet.synsets(token, pos=wn_pos)
        for syn in synonyms:
            for lemma in syn.lemmas():
                # Replace underscores with spaces
                related_words.append(lemma.name().replace('_', ' '))
                
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
