from search_wikipedia import get_wiki_url, get_keyword, analyze_threshold, get_wiki_description, get_wiki_title


most_relevant_keyword = ""


def process_row(description, wiki_page, collection_term):
    return (
        populate_wiki(wiki_page),  # Wikipedia
        populate_description(description, wiki_page,
                             collection_term),  # Description
        populate_event_name(wiki_page),  # Event Name
    )


def populate_wiki(wiki_page):
    """
    populate wikipedia link in spreadsheet
    returns content to be inserted into given cell    
    """
    try:
        return get_wiki_url(wiki_page)
    except Exception as e:
        print("Error getting wiki url " + str(e))
        return None


def populate_description(current_description, wiki_page, collection_term):
    """ populate description in spreadsheet using wikipedia library and keyword frequency threshold analytics
        returns content to be populated for description field     
    """
    global most_relevant_keyword
    if current_description:
        return current_description

    try:
        most_relevant_keyword = get_keyword(wiki_page)
        most_relevant_keyword = analyze_threshold(
            3, wiki_page, most_relevant_keyword, collection_term)

        if not most_relevant_keyword:
            return None  # article has low ontological relevance
        return get_wiki_description(wiki_page)

    except Exception as e:
        print("Error 2")
        return None


def populate_event_name(wiki_page):
    """uses wikipedia article title to populate event name in spreadsheet
       returns event name to be written to spreadsheet
    """
    try:
        return get_wiki_title(wiki_page)

    except Exception as e:
        print("Error in generating Event Name")
        return None
