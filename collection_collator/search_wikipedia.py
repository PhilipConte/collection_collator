from collections import Counter
import re
import sys
import wordninja


def populate_description(current_description, wiki_page, collection_term):
    """ populate description in spreadsheet using wikipedia library and keyword frequency threshold analytics
        returns content to be populated for description field     
    """
    if current_description:
        return current_description

    try:
        most_relevant_keyword = analyze_threshold(
            3, wiki_page, get_keyword(wiki_page), collection_term)

        if not most_relevant_keyword:
            return None  # article has low ontological relevance
        return get_wiki_description(wiki_page)

    except Exception as e:
        print("Error 2")
        return None


def get_wiki_content(wiki_page):
    """This function returns the content of the wikipage, in UTF8
        Args:
                wiki_page: The wiki_page object to find content and strip down.	
    """
    return [l.replace('\n', '') for l in wiki_page.content.encode('UTF8').split('.')]


def get_keyword(wiki_page):
    """Returns most relevant ontology entity from a given wikipedia article
    Args:
        wiki_page: The wiki_page object to find keyword.
    """
    global most_relevant_keyword
    owl_filename = 'CTRontology.owl'
    wc = get_wiki_content(wiki_page)
    oc = get_owl_categories(owl_filename)
    most_relevant_keyword = calculate_category(oc, wiki_page, wc)

    return most_relevant_keyword


def get_wiki_description(wiki_page):
    """ Select a relevant sentence from a given wikipedia article to serve as a description sentence 
    for an event collection based on ontological relevance
    Args:
        wiki_page: The wiki_page object to find description.	

    """
    global most_relevant_keyword
    wc = get_wiki_content(wiki_page)

    for line in wc:
        line = line.replace('\n', '')
        # TODO possibly strip commas to fill in spreadsheet
        if most_relevant_keyword.upper() in line.upper():
            return "\"" + line + "\""


def analyze_threshold(threshold, wiki_page, most_relevant_keyword, collection_term):
    """
    analyzes ontological entity names as keywords in the given wikipedia article
    select and return the most common keyword as most relevant 
    """

    wc = get_wiki_content(wiki_page)

    keyword_count = []
    index = 0
    for cline in wc:
        cline = cline.replace('\n', '')
        keyword_count.append(0)
        if most_relevant_keyword.upper() in cline.upper():
            index += 1

    if (index < threshold):

        print("FLAG: Article has low ontological relevance for search for \"" + str(collection_term) +
              "\" using known keyword from ontology: \""+str(most_relevant_keyword)+"\" with results " + str(index) + " " + ("entry" if index == 1 else "entries") + ".\n\t")
        most_relevant_keyword = None

        with open('stoplist.txt') as f:
            stoplist = f.read().split()

        # Suggest keywords to user to add to ontology
        words = wiki_page.content.encode('UTF8').split(" ")
        cap_words = [word.lower() for word in words]  # All caps
        # filter out stop words
        filtered = [word for word in cap_words if word not in stoplist]
        word_counts = Counter(filtered).most_common(5)  # count each
        print("Here are some suggestions: " + str(word_counts) + "\n")
        return None
    return most_relevant_keyword


def calculate_category(category_list, wiki_page, wiki_content):
    """ returns most relevant keyword in given wikipedia article based on ontological relevance
        formats input from ontology file to give full list of ontological terms
    Args
        category_list: These are the categories to sort the data.        .    
    """
    index = -1
    keyword_count = []

    # Fist section, get the category count
    for line in category_list:

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
        for cline in wiki_content:
            cline = cline.replace('\n', '')
            keyword_count.append(0)
            if line.upper() in cline.upper():
                keyword_count[index] = keyword_count[index] + 1

    m = max(keyword_count)

    max_indices = [i for i, j in enumerate(keyword_count) if j == m]

    most_relevant_keyword = category_list[max_indices[0]]
    most_relevant_keyword = most_relevant_keyword.replace('<Class IRI=\"#', '')
    most_relevant_keyword = most_relevant_keyword.replace('\"/>', '')
    most_relevant_keyword = most_relevant_keyword.replace('_', ' ')
    most_relevant_keyword = most_relevant_keyword.replace('\t', '')
    most_relevant_keyword = most_relevant_keyword.replace(' ', '')
    most_relevant_keyword = most_relevant_keyword.replace('\n', '')
    return most_relevant_keyword


def get_owl_categories(owl_filename):
    """
        opens ontology file as readable object 
        split by line
    """
    return open(owl_filename, 'r').readlines()
