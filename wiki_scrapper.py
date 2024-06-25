# import wikipediaapi

# def scrape_wikipedia_articles(category, lang='kn', max_articles=10):
#     user_agent = 'Kannada-spell-checker/1.0 (sidddelta@gmail.com)'
#     wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
#     cat = wiki.page("Category:" + category)
#     articles = []

#     def get_categorymembers(categorymembers, level=0, max_level=1):
#         nonlocal articles
#         for c in categorymembers.values():
#             if len(articles) >= max_articles:
#                 break
#             if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
#                 get_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)
#             elif c.ns == wikipediaapi.Namespace.MAIN:
#                 articles.append(c.text)

#     if not cat.exists():
#         print(f"Category '{category}' does not exist in the {lang} Wikipedia.")
#         return []

#     get_categorymembers(cat.categorymembers)
#     return articles[:max_articles]

# articles = scrape_wikipedia_articles("Kannada_language", max_articles=10)
# print("Number of articles fetched:", len(articles))

import wikipediaapi
import re
import json

def scrape_wikipedia_articles(category, lang='kn'):
    user_agent = 'Kannada-spell-checker/1.0 (sidddelta@gmail.com)'
    wiki = wikipediaapi.Wikipedia(language=lang, user_agent=user_agent)
    cat = wiki.page("Category:" + category)

    articles = []

    def get_categorymembers(categorymembers, level=0, max_level=4):
        for c in categorymembers.values():
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)
            elif c.ns == wikipediaapi.Namespace.MAIN:
                articles.append(c.text)

    if cat.exists():
        get_categorymembers(cat.categorymembers)
    else:
        print(f"Category '{category}' does not exist.")

    return articles

def preprocess(text):
    text = re.sub(r'[^ಀ-೿a-zA-Z\s]', '', text)
    text = text.lower()
    return text

def tokenize(text):
    return text.split()

# Scrape articles
articles = scrape_wikipedia_articles("ಕನ್ನಡ_ಭಾಷೆ")  # Use the correct Kannada category name
print("Number of articles:", len(articles))

# Combine all collected text
corpus = " ".join(articles)

# Preprocess the text
cleaned_corpus = preprocess(corpus)
print(cleaned_corpus[:1000])  # Print the first 1000 characters

# Tokenize the text
tokens = tokenize(cleaned_corpus)
print(tokens[:50])  # Print the first 50 tokens

# Save the corpus
with open('kannada_corpus.json', 'w', encoding='utf-8') as f:
    json.dump(tokens, f, ensure_ascii=False, indent=4)
