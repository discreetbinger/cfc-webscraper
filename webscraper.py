from bs4 import BeautifulSoup, Comment
import requests
import json
import string

# function to export to json file
def export_to_json(file, item):
    with open(file, 'w') as f:
        json.dump(item, f, indent=0)

'''
    Task 1 & 2
                '''

# checks if the given path is externally hosted
def path_is_external(path):
    # the location is internal if it contains the cfc domain or does not contain 'http' since local files do not
    if 'cfcunderwriting.com' in path or 'http' not in path:
        return False
        
    return True

# returns a list of the external resources
def get_external_resources(soup):
    external_resources = []
    tags = {'img': 'src', 'script': 'src', 'link': 'href', 'iframe': 'src'} # tags and their attributes we want to look for
    for tag in tags:
        # looks through every single appearance of the specified tags on the webpage
        for eachTag in soup.find_all(tag):
            try:
                item = eachTag[tags.get(tag)]
                # collect the paths that are external
                if path_is_external(item):
                    external_resources.append(item)
            except KeyError:
                pass

    return external_resources



'''
    Task 3
            '''

# returns all the hyperlinks from a webpage
def enumerate_hyperlinks(soup):
    hyperlinks = []
    for link in soup.find_all('a'):
        try:
            # could use a set here to not have duplicate links
            # stores pairs of links and text found in the same anchor element
            hyperlinks.append((link.get('href'), link.find(text=True)))
        except KeyError:
            pass

    return hyperlinks

# searches through hyperlinks to locate the 'Privacy Policy' page
def privacy_policy_path(links):
    # looks through pairs of the links and their related text
    for(link, text) in links:
        try:
            # we found the path and return it
            if text.lower() == 'Privacy Policy'.lower():
                return link
        except AttributeError:
            pass

    return None



'''
    Task 4
            '''

# scrapes the page and returns the visible text from it
def get_visible_text(soup):
    blacklist = ['head', 'title', 'script', 'style', '[document]'] # hidden content thats not visible on page
    text = soup.findAll(text=True)
    visible_text = ''
    # checks if text is visible on page and also not comments of code
    for elem in text:
        if elem.parent.name not in blacklist and not isinstance(elem, Comment):
            visible_text += ' ' + elem.strip()
            
    return visible_text

# returns a dictionary of words and their count from a text
def get_word_frequency(soup):
    # cleanup the visible text
    page_text = get_visible_text(soup)
    page_text = page_text.encode('ascii', 'ignore').decode()  # removes unicode chars
    page_text = page_text.translate(str.maketrans('', '', string.punctuation)) # removes punctuation

    # split text into a list of words
    text = page_text.split(' ')
    text = list(filter(None, text)) # removes empty strings

    # count the occurence of each word
    word_count = {}
    for word in text:
        word = word.lower()
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count



if __name__ == '__main__':

    url = 'https://www.cfcunderwriting.com'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # scrapes the index page and gets the externally loaded resources exported to json file
    external_resources = get_external_resources(soup)
    export_to_json('external_resources.json', external_resources)

    # gathers hyperlinks from the index page
    hyperlinks = enumerate_hyperlinks(soup)
    
    # finds the path to the privacy policy page from hyperlinks
    # and appends it to the url of the index page
    privacy_policy_url = url + privacy_policy_path(hyperlinks)
    privacy_policy_page = requests.get(privacy_policy_url)
    privacy_policy_soup = BeautifulSoup(privacy_policy_page.content, 'html.parser')
    
    # gets the word frequency count of the privacy policy page and exports to json file
    word_frequency = get_word_frequency(privacy_policy_soup)
    export_to_json('word_frequency.json', word_frequency)