import regex as re

def get_author(content):
    row_list = content.splitlines()
    print(type(row_list))
    for row in row_list:
        if row.strip():
            if row.find('Discover all poems by '):
                author_name = row
                break
            
    return author_name


def get_title(content):
    """
    Retrieves poem title. 

    Args:
        content (str): The poem.

    Returns:
        title (str): The name of the poem
    """

    # Split the str into a list of lines
    row_list = content.splitlines()
    
    # Iterate over lines to find the first non-empty one
    for row in row_list:
        # Check if row is empty after removing whitespace
        if row.strip():
            title_row = row.strip()
            break
    # Isolate the name of the poem
    title = title_row.replace(' - Poetry Archive', '')

    return title

def get_poem():
    pass