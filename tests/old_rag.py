from newspaper import Article
from newspaper.article import ArticleException
from keybert import KeyBERT
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
import requests

def call_news_api(keyword, date, NEWS_API_KEY, everything=True):
    API_KEY = NEWS_API_KEY
    
    # choose endpoint
    endpoint = "everything" if everything else "top-headlines"
    # build URL with the passed-in variables
    url = (
        f"https://newsapi.org/v2/{endpoint}"
        f"?q={keyword}"
        f"&from={date}"
        "&sortBy=relevancy"
        f"&apiKey={API_KEY}"
    )
    response = requests.get(url)

    return response
    
def search_article_type(lean_list, all_articles, ratio):
    """
    combs through articles and returns N amount of a certain type of article, meaning N amount of left, right, and center
    """
    count = 0
    i = 0
    type_list = []
    while count < ratio:
        i += 1
        if(all_articles[i]['source']['name'] in lean_list):
            type_list.append(all_articles[i])
            count += 1

    return type_list

def get_blend(all_articles, n_search):
    blended_articles = []
    
    # compile list of sources for each type
    right_leaning = ['Breitbart News', ]
    left_leaning = []
    center_leaning = ['NBC News','The Washington Post','ABC News',]

    # how much of each type of source to get. this automatically assumes an equal blend of each source
    ratio = n_search // 3       
    
    # loop through each type
    types = ['right', 'left', 'center']
    for x in types:
        result = search_article_type(x, all_articles, ratio)
        blended_articles.append(result)

    return blended_articles

def rewrite_content(article_url):
    """
    given a url to some article, return its content
    this is really just a helper function. also has safeguards for articles that block the scraping tool. 
    """
    article = Article(article_url)
    try: 
        article.download()
        article.parse()
    
        # cleaning it up
        text = article.text
        filtered_lines = filter(str.strip, text.splitlines())
        cleaned_text = "\n".join(filtered_lines)
        return cleaned_text

    except ArticleException as e:
        print(f"[!] Skipping article at {article_url} — {e}")
        return None
    
def get_keyword(query):
    """
    simply return the main keyword of the query the user has asked
    """
    keyword_model = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = keyword_model.extract_keywords(query)            # a list of keywords with the most relevant listed first

    return keywords[0][0]

def get_similarities(all_articles, query):
    """
    sort the articles in order of their semantic similarity to the query 
    return only the top n results
    need to add a "score" attribute to all of the articles
    """
    semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
    encoded_query = semantic_model.encode(query)

    for article in all_articles:
        encoded_description = semantic_model.encode(article['description'])
        article["sem_sim"] = 1-distance.cosine(encoded_query, encoded_description)

def get_n_matches(all_articles, N):
    """
    all_articles is a list of dictionaries. need to sort this list to get N of the dictionaries with the largest sem_sim value
    """
    sorted_articles = sorted(all_articles, key=lambda x: x['sem_sim'], reverse=True)
    
    return sorted_articles[:N]
    
def extract_content(article_list):
    """
    given a list of articles, get the content for them
    save this in a text file
    """
    all_content = ""
    article_list

    for article in article_list:
        content = rewrite_content(article['url'])

        # skip articles that contain nothing or that block the scraper
        if (article['content'] == None) or (content == None):
            continue
        article['content'] = content
        all_content += article['source']['name'] + "\n"
        all_content += article['content'] + "\n----------------------------\n"

    return all_content

def get_citation(articles):
    citation = "Response is based on the following sources: \n"

    for article in articles:
        citation += (
                        f"{article['author']}. "
                        f"\"{article['title']}\". "
                        f"{article['source']['name']}. "
                        f"{article['url']}\n"
                    )
    
    return citation

