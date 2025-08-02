import os

import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector
from psycopg2 import extensions

POSTGRESQL_PWD = os.getenv("POSTGRESQL_PWD")


#     DB_USER: str
#     DB_PASSWORD: str
#     DB_NAME: str


def store_sql(article_chunks, USER, PWD, DB_NAME):
    """
    stores chunks into a postgreSQL database.
    input: list of objects of class ArticleChunk, that have vector embeddings
    """
    # SQL connection params
    hostname = "localhost"
    database = "newsdash"
    username = "postgres"
    pwd = POSTGRESQL_PWD
    port_id = 5432
    conn = None
    cur = None

    print("article chunk length: ", len(article_chunks))

    try:
        # initializing connection object
        conn = psycopg2.connect(
            host=hostname, database=database, user=username, password=pwd, port=port_id
        )

        register_vector(conn)

        # Turn on autocommit so CREATE EXTENSION runs immediately
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        # open a cursor, performs SQL operations
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        cur.execute("DROP TABLE IF EXISTS chunked_data;")

        # Switch back to transactional mode to make the table
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_READ_COMMITTED)

        create_script = """ CREATE TABLE IF NOT EXISTS chunked_data (
                                chunk_id UUID NOT NULL PRIMARY KEY,
                                author VARCHAR(50),
                                url VARCHAR(300),
                                title VARCHAR(200),
                                source VARCHAR(100),
                                content TEXT,
                                embedding VECTOR(384))"""

        cur.execute(create_script)
        # insert data into the table

        insert_script = "INSERT INTO chunked_data (chunk_id, author, url, title, source, content, embedding) VALUES (uuid_generate_v4(), %s, %s, %s, %s, %s, %s)"

        for chunk in article_chunks:
            data = [
                chunk.author,
                chunk.url,
                chunk.title,
                chunk.source,
                chunk.content,
                chunk.embedding,
            ]
            cur.execute(insert_script, data)

        # always place this at the bottom
        conn.commit()

    except Exception as error:
        import traceback

        traceback.print_exc()
        raise
    finally:
        # close the cursor and the connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def fetch_sql(encoded_query, n_chunks):
    """
    stores chunks into a postgreSQL database.
    input: list of objects of class ArticleChunk, that have vector embeddings
    """
    # SQL connection params
    hostname = "localhost"
    database = "newsdash"
    username = "postgres"
    pwd = POSTGRESQL_PWD
    port_id = 5432
    conn = None
    cur = None

    try:
        # initializing connection object
        conn = psycopg2.connect(
            host=hostname, database=database, user=username, password=pwd, port=port_id
        )

        register_vector(conn)

        # Turn on autocommit so CREATE EXTENSION runs immediately
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        # open a cursor, performs SQL operations
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Switch back to transactional mode to make the table
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_READ_COMMITTED)

        # fetching data
        featch_script = """
        SELECT
            chunk_id,
            author,
            url,
            title,
            source,
            content,
            embedding <=> %s   AS cosine_dist
        FROM chunked_data
        ORDER BY cosine_dist
        LIMIT %s;
        """

        cur.execute(featch_script, (encoded_query, n_chunks))
        top_n_chunks = cur.fetchall()

        print("SQL select completed")
        # always place this at the bottom
        conn.commit()

    except Exception as error:
        import traceback

        traceback.print_exc()
        raise
    finally:
        # close the cursor and the connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

        return top_n_chunks
