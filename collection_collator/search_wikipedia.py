from collections import Counter


with open('CTRontology.owl', 'r') as f:
    OWL = f.readlines()


with open('stoplist.txt') as f:
    STOP_LIST = f.read().split()


def populate_description(full_text, collection_term):
    """ populate description in spreadsheet using wikipedia library and keyword frequency threshold analytics
        returns content to be populated for description field     
    """
    lines = full_text.split('.')
    try:
        most_relevant_keyword = analyze_threshold(
            3, full_text, lines, calculate_category(lines), collection_term)

        if not most_relevant_keyword:
            return None  # article has low ontological relevance
        return get_wiki_description(lines, most_relevant_keyword)

    except Exception as e:
        print("Error 2")
        return None


def get_wiki_description(lines, most_relevant_keyword):
    """ Select a relevant sentence from a given wikipedia article to serve as a description sentence 
    for an event collection based on ontological relevance
    """
    for line in lines:
        # TODO possibly strip commas to fill in spreadsheet
        if most_relevant_keyword.upper() in line.upper():
            return "\"" + line + "\""


def analyze_threshold(threshold, full_text, lines, most_relevant_keyword, collection_term):
    """
    analyzes ontological entity names as keywords in the given wikipedia article
    select and return the most common keyword as most relevant 
    """
    keyword_count = []
    index = 0
    for cline in lines:
        keyword_count.append(0)
        if most_relevant_keyword.upper() in cline.upper():
            index += 1

    if (index < threshold):

        print("FLAG: Article has low ontological relevance for search for \"" + str(collection_term) +
              "\" using known keyword from ontology: \""+str(most_relevant_keyword)+"\" with results " + str(index) + " " + ("entry" if index == 1 else "entries") + ".\n\t")
        most_relevant_keyword = None

        # Suggest keywords to user to add to ontology
        cap_words = [word.lower() for word in full_text.split()]  # All caps
        # filter out stop words
        filtered = [word for word in cap_words if word not in STOP_LIST]
        word_counts = Counter(filtered).most_common(5)  # count each
        print("Here are some suggestions: " + str(word_counts) + "\n")
        return None
    return most_relevant_keyword


def calculate_category(lines):
    """ returns most relevant keyword in given wikipedia article based on ontological relevance
        formats input from ontology file to give full list of ontological terms      .    
    """
    index = -1
    keyword_count = []

    # Fist section, get the category count
    for line in OWL:

        index = index + 1
        keyword_count.append(0)
        line = line.replace('_', ' ')
        if 'Class IRI=' in line:
            line = line.replace('<Class IRI=\"#', '')
            line = line.replace('\"/>', '')
            line = line.replace('\t', '')
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = ' ' + line + ' '
        for cline in lines:
            cline = cline.replace('\n', '')
            keyword_count.append(0)
            if line.upper() in cline.upper():
                keyword_count[index] = keyword_count[index] + 1

    m = max(keyword_count)

    max_indices = [i for i, j in enumerate(keyword_count) if j == m]

    most_relevant_keyword = OWL[max_indices[0]]
    most_relevant_keyword = most_relevant_keyword.replace('<Class IRI=\"#', '')
    most_relevant_keyword = most_relevant_keyword.replace('\"/>', '')
    most_relevant_keyword = most_relevant_keyword.replace('_', ' ')
    most_relevant_keyword = most_relevant_keyword.replace('\t', '')
    most_relevant_keyword = most_relevant_keyword.replace(' ', '')
    most_relevant_keyword = most_relevant_keyword.replace('\n', '')
    return most_relevant_keyword
