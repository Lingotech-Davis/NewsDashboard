import os

import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector
from psycopg2 import extensions
from src.db import models, schemas
import datetime


#     DB_USER: str
#     DB_PASSWORD: str
#     DB_NAME: str


def filter_out_existing_articles(articles, db_session):
    all_incoming_urls = [article["url"] for article in articles]
    existing_articles = (
        db_session.query(models.Article)
        .filter(models.Article.url.in_(all_incoming_urls))
        .all()
    )

    existing_urls = {article.url for article in existing_articles}
    unstored_articles = [
        article for article in articles if article["url"] not in existing_urls
    ]

    return unstored_articles


def store_articles(articles_data, db_session):
    """
    Persists a list of articles and their embeddings to the database.

    Args:
        articles_data (list): A list of dictionaries, where each dictionary
                              represents a single article with its chunks and embeddings.
        db_session: An SQLAlchemy session object connected to the database.
    """
    for article_data in articles_data:
        try:
            # Create a new Article instance from the data
            article = models.Article(
                url=article_data["url"],
                urlToImage=article_data.get("urlToImage"),
                source=article_data.get("source"),
                author=article_data.get("author"),
                title=article_data.get("title"),
                description=article_data.get("description"),
                # Convert the ISO 8601 string to a Python datetime object
                publishedAt=datetime.datetime.fromisoformat(
                    article_data.get("publishedAt").replace("Z", "+00:00")
                )
                if article_data.get("publishedAt")
                else None,
                scrape_successful=article_data.get("scrape_successful"),
                text=article_data.get("text"),
            )
            db_session.add(article)

            # Create Chunk instances for each chunk and link them
            # to the newly created Article instance
            for chunk_text, embeddings_list in zip(
                article_data["chunks"], article_data["embeddings_list"]
            ):
                chunk = models.Chunk(
                    content=chunk_text,
                    # The pgvector type correctly handles the list of floats.
                    embedding=embeddings_list,
                    article=article,
                )
                db_session.add(chunk)

            db_session.commit()
            print(f"Successfully stored article: {article.title}")

        except Exception as e:
            db_session.rollback()
            print(f"Failed to store article from {article_data.get('url')}. Error: {e}")


# def store_sql(article_chunks, USER, PWD, DB_NAME):
#     """
#     stores chunks into a postgreSQL database.
#     input: list of objects of class ArticleChunk, that have vector embeddings
#     """
#     # SQL connection params
#     hostname = "localhost"
#     database = "newsdash"
#     username = "postgres"
#     pwd = POSTGRESQL_PWD
#     port_id = 5432
#     conn = None
#     cur = None
#
#     print("article chunk length: ", len(article_chunks))
#
#     try:
#         # initializing connection object
#         conn = psycopg2.connect(
#             host=hostname, database=database, user=username, password=pwd, port=port_id
#         )
#
# register_vector(conn)
#
#         # Turn on autocommit so CREATE EXTENSION runs immediately
#         conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#
#         # open a cursor, performs SQL operations
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
#         cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
#         cur.execute("DROP TABLE IF EXISTS chunked_data;")
#
#         # Switch back to transactional mode to make the table
#         conn.set_isolation_level(extensions.ISOLATION_LEVEL_READ_COMMITTED)
#
#         create_script = """ CREATE TABLE IF NOT EXISTS chunked_data (
#                                 chunk_id UUID NOT NULL PRIMARY KEY,
#                                 author VARCHAR(50),
#                                 url VARCHAR(300),
#                                 title VARCHAR(200),
#                                 source VARCHAR(100),
#                                 content TEXT,
#                                 embedding VECTOR(384))"""
#
#         cur.execute(create_script)
#         # insert data into the table
#
#         insert_script = "INSERT INTO chunked_data (chunk_id, author, url, title, source, content, embedding) VALUES (uuid_generate_v4(), %s, %s, %s, %s, %s, %s)"
#
#         for chunk in article_chunks:
#             data = [
#                 chunk.author,
#                 chunk.url,
#                 chunk.title,
#                 chunk.source,
#                 chunk.content,
#                 chunk.embedding,
#             ]
#             cur.execute(insert_script, data)
#
#         # always place this at the bottom
#         conn.commit()
#
#     except Exception as error:
#         import traceback
#
#         traceback.print_exc()
#         raise
#     finally:
#         # close the cursor and the connection
#         if cur is not None:
#             cur.close()
#         if conn is not None:
#             conn.close()
#
#
# def fetch_sql(encoded_query, n_chunks):
#     """
#     stores chunks into a postgreSQL database.
#     input: list of objects of class ArticleChunk, that have vector embeddings
#     """
#     # SQL connection params
#     hostname = "localhost"
#     database = "newsdash"
#     username = "postgres"
#     pwd = POSTGRESQL_PWD
#     port_id = 5432
#     conn = None
#     cur = None
#
#     try:
#         # initializing connection object
#         conn = psycopg2.connect(
#             host=hostname, database=database, user=username, password=pwd, port=port_id
#         )
#
#         register_vector(conn)
#
#         # Turn on autocommit so CREATE EXTENSION runs immediately
#         conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#
#         # open a cursor, performs SQL operations
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#         # Switch back to transactional mode to make the table
#         conn.set_isolation_level(extensions.ISOLATION_LEVEL_READ_COMMITTED)
#
#         # fetching data
#         featch_script = """
#         SELECT
#             chunk_id,
#             author,
#             url,
#             title,
#             source,
#             content,
#             embedding <=> %s   AS cosine_dist
#         FROM chunked_data
#         ORDER BY cosine_dist
#         LIMIT %s;
#         """
#
#         cur.execute(featch_script, (encoded_query, n_chunks))
#         top_n_chunks = cur.fetchall()
#
#         print("SQL select completed")
#         # always place this at the bottom
#         conn.commit()
#
#     except Exception as error:
#         import traceback
#
#         traceback.print_exc()
#         raise
#     finally:
#         # close the cursor and the connection
#         if cur is not None:
#             cur.close()
#         if conn is not None:
#             conn.close()
#
#         return top_n_chunks
