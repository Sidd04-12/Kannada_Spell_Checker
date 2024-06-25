import wikipediaapi
import json

def list_categories(root_category, lang='kn', max_level=2):
    user_agent = 'Kannada-spell-checker/1.0 (sidddelta@gmail.com)'
    wiki = wikipediaapi.Wikipedia(language=lang, user_agent=user_agent)
    
    root_cat = wiki.page("Category:" + root_category)
    categories = []

    def get_categories(category, level=0):
        if level > max_level:
            return
        for c in category.categorymembers.values():
            if c.ns == wikipediaapi.Namespace.CATEGORY:
                categories.append(c.title)
                get_categories(c, level + 1)

    if root_cat.exists():
        get_categories(root_cat)
    else:
        print(f"Category '{root_category}' does not exist.")

    return categories

# Try with more generic root categories
root_categories = ["ವರ್ಗ:ಅವಳಿಕರಣ", "ವರ್ಗ:ಅ", "ವರ್ಗ:ಕನ್ನಡ"]

all_categories = []
for root in root_categories:
    categories = list_categories(root, max_level=2)
    print(f"Categories found under {root}:")
    for category in categories:
        print(category)
    all_categories.extend(categories)

# Save all the categories to a file
with open('kannada_categories.json', 'w', encoding='utf-8') as f:
    json.dump(all_categories, f, ensure_ascii=False, indent=4)
