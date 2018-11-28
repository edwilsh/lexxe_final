import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
import categorize as c

# Load Data
titles = pd.read_csv('Data/Titles.csv')

# Gather Sindex Entries
destdir = Path('test/')
files = [p for p in destdir.iterdir() if p.is_file()]
keys = []
for p in files:
    try:
        tree = ET.parse('test/' + p.name)
        root = tree.getroot()
        for n in root.iter('name'):
            keys.append(n.text)
    except:
        pass
# Order Sindex List Ascending/Remove 1 and 2 Letter Entries (Ambiguous)
ordered_keys = sorted(keys, key=len)
for n in ordered_keys:
    if len(n) < 3:
        ordered_keys.remove(n)
# Check Duplicates
key_set = set(keys)

# Number of Unique Sindex Entries
print('Number of Unique Sindex Entries:', len(key_set))

# Track Grouped Terms
grouped_terms = []

# Recursive Search and Delete
def remove_titles(text_list):
    for word in text_list:
        if(titles['Titles'].str.contains(word).any()):
            text_list.remove(word)
            remove_titles(text_list)
        else:
            return ' '.join(text_list)

def group(text):
    # Create List
    check = text.split()
    # Remove Titles If Any (Recursive Function)
    pruned = remove_titles(check)
    # Create 'Similar' List
    similar = list()
    for k in ordered_keys:
        if(pruned in k):
            similar.append(k)
    # Duplicates
    distinct_similar = set(similar)
    complete = dict()
    # complete_sorted = dict()
    for word in distinct_similar:
        count = 0
        for k in similar:
            if(k.count(word)):
                count += 1
        complete.update({word : count})
        
    # Init Dataframe
    columns = ['Sindex_Entry', 'Freq', 'Category']
    output = pd.DataFrame(columns=columns)
    sin = []
    freq = []
    cate = []
    # Order by count, Title Entry Designated by Frequency    
    for r in sorted(complete, key=complete.get, reverse=True):
        # complete_sorted.update({r : complete[r]})
        # print(r, complete[r], c.categorize(r))
        sin.append(r)
        freq.append(complete[r])
        cate.append(c.category(r))
    
    # Purge for Categories
    sindex = ' '.join(check)
    category = c.category(sindex)
    
   # Add Results to DataFrame
    output['Sindex_Entry'] = sin
    output['Freq'] = freq
    output['Category'] = cate
    
    output = output[output['Category'] == category]
    
    # Append to grouped_terms var
    temp_group = output['Sindex_Entry'].tolist()
    for x in temp_group:
        grouped_terms.append(str(x))
    
    output.to_csv('Output/'+sin[0]+'.csv') 

    return output

def main():
    count = 0
    failed = 0
    i = 1
    for entry in list(key_set):
        if(entry not in grouped_terms):
            try:
                group(entry)
                count += 1
            except:
                failed += 1
        print(i, '/', len(key_set), 'completed')
        i += 1
    print(count, ' entries successfully grouped')
    print(failed, 'entries cannot be grouped')

main()




