from newspaper import Article
from newspaper.article import ArticleException

# REWRITING ARTICLE CONTENT 
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
    
def extract_content(article_list):
    """
    given a list of articles, get the content for them
    """

    for i in range(len(article_list)):
        content = rewrite_content(article_list[i]['url'])

        # skip articles that contain nothing or that block the scraper
        if (article_list[i]['content'] == None) or (content == None):
            continue
        article_list[i]['content'] = content

        
class ArticleChunk:
    def __init__(self, author, url, title, source, content):
        self.author = author
        self.title = title
        self.source = source
        self.url = url
        self.content = content
        self.embedding = None
    
    def embed(self, embedding):
        self.embedding = embedding.tolist()

def divide_content(content, max_tokens=300, overlap=25):
    """
    input: a string of content from an article
    output: a flat list of said content in max 300 token long chunks each, with 25 token of overlap each
    """
    # Split content into tokens (assuming whitespace tokenization)
    tokens = content.split()

    # Validate overlap
    if overlap >= max_tokens:
        raise ValueError("Overlap must be smaller than max_tokens.")

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk = tokens[start:end]
        chunks.append(" ".join(chunk))

        # Move start forward, keeping overlap
        start += max_tokens - overlap

    return chunks

def chunkify(raw_articles):
    """
    each item here is a dict with content. need to break each into 300 token chunks
    output will be a list of ArticleChunks. 
    """
    chunks = []

    for article in raw_articles:
        # small content can go straight into a chunk

        if len(article['content'].split()) < 300:
            chunks.append(ArticleChunk(article['author'], article['url'], article['title'], article['source']['name'], article['content']))
        else:
            # divide article content into max 300 token long chunks with 30 token overlap each, this is a list of content
            divided_content = divide_content(article['content'])
            for content in divided_content:
                chunks.append(ArticleChunk(article['author'], article['url'], article['title'], article['source']['name'], content))

    return chunks

