import pandas as pd
import string

# Import Keyword Data
countries = pd.read_csv('Data/places.csv')
names = pd.read_csv('Data/names.csv')
names['Names'] = names['Names'].str.lower()
names['Names'] = names['Names'].str.capitalize()
concepts = pd.read_csv('Data/concept_nouns.csv')
concepts['Nouns'].str.capitalize()
organizations = pd.read_csv('Data/organizations.csv')
products = pd.read_csv('Data/products.csv')
products.dropna(inplace=True)

# String Punctuation
table = str.maketrans({key: None for key in string.punctuation})
table_edited = string.punctuation.replace("'",'')

# Categorize Function
def category(text):
    # Split Sindex Entry in to list
    check = text.split()
    temp = list()
    # Remove Punctuation
    for s in check:
        s = ''.join(ch for ch in s if ch not in table_edited)
        temp.append(s)
    check = temp

    # Category Dictionary ['Organization','Person','Place','Product','Concept']
    categories = {'Organization':0,'Person':0,'Place':0,'Product':0,'Concept':0}

    # Trailing Word Rule
    trail = check[-1]
    for x in range(0,2,1):
        check.append(trail)
    
    # Concept Rule
    if (len(text) > 40):
        categories['Concept'] += 5

    # Head Noun Rule
    if('of' in check):
        try:
            pos = check.index('of')
            for _ in range(0,5,1):
                check.append(check[pos-1])
        except:
            pass
        
    if('Of' in check):
        try:
            pos = check.index('Of')
            for _ in range(0,4,1):
                check.append(check[pos-1])
        except:
            pass
    
    # Check Organizations
    for word in check:
        if(len(organizations[organizations['Organizations'].str.contains(word)]) > 0):
            categories['Organization'] += 1
    
    # Check Names
    for word in check:
        if(len(names[names['Names'].str.contains(word)]) > 0):
            categories['Person'] += 1
    
    # Check Places
    for word in check:
        if(len(countries[countries['Places'].str.contains(word)]) > 0):
            categories['Place'] += 1
            
    # Check Products
    for word in check:
        if(len(products[products['Products'].str.contains(word)]) > 0):
            categories['Place'] += 2

    # Check Concepts
    for word in check:
         if(len(concepts[concepts['Nouns'].str.contains(word)]) > 0):
                categories['Concept'] += 1
    
    result = max(categories, key=categories.get)
    
    return result