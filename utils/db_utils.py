import sqlite3
from typing import List, Dict
import re


# def connect_db(db_path: str):
#     return sqlite3.connect(db_path)


# def query_images(db_path: str, keywords: List[str], max_results: int = 5) -> List[Dict]:
#     conn = connect_db(db_path)
#     cursor = conn.cursor()
#     keyword_query = ' OR '.join([f"tags LIKE '%{kw}%'" for kw in keywords])
#     query = f"SELECT id, url, tags FROM images WHERE {keyword_query} LIMIT {max_results};"
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()
#     return [{"id": r[0], "url": r[1], "tags": r[2]} for r in results]


# def query_links(db_path: str, keywords: List[str], max_results: int = 5) -> List[Dict]:
#     conn = connect_db(db_path)
#     cursor = conn.cursor()
#     keyword_query = ' OR '.join([f"topic_tags LIKE '%{kw}%'" for kw in keywords])
#     query = f"SELECT id, url, title, topic_tags, type FROM resources WHERE {keyword_query} LIMIT {max_results};"
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()
#     return [
#         {
#             "id": r[0],
#             "url": r[1],
#             "title": r[2],
#             "topic_tags": r[3],
#             "type": r[4]
#         }
#         for r in results
#     ]



# import sqlite3

# def get_links_for_keywords(keywords, db_path="links.db"):
#     """
#     Query the 'resources' table in links.db and return entries
#     where any keyword appears in the topic_tags column.
#     """
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # We'll use LIKE queries for basic tag matching
#     results = []
#     for kw in keywords:
#         pattern = f"%{kw.lower()}%"
#         cursor.execute("""
#             SELECT url, topic_tags FROM resources WHERE LOWER(topic_tags) LIKE ?
#         """, (pattern,))
#         # for row in cursor.fetchall():
#         #     if kw.lower() in row[1].lower():
#         #         results.append({"keyword": kw, "url": row[0]})

#         for row in cursor.fetchall():
#             db_tags = [tag.strip().lower() for tag in row[1].split(",")]
#             if any(tag in kw.lower() for tag in db_tags):
#                 results.append({"keyword": kw, "url": row[0]})
#     conn.close()
#     return results


# def get_images_for_keywords(keywords, db_path="media.db"):
#     """
#     Query the 'images' table in media.db and return entries
#     where any keyword appears in the tags column.
#     """
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     results = []
#     for kw in keywords:
#         pattern = f"%{kw.lower()}%"
#         cursor.execute("""
#             SELECT url, tags FROM images WHERE LOWER(tags) LIKE ?
#         """, (pattern,))
#         # for row in cursor.fetchall():
#         #     if kw.lower() in row[1].lower():
#         #         results.append({"keyword": kw, "url": row[0]})

#         for row in cursor.fetchall():
#             db_tags = [tag.strip().lower() for tag in row[1].split(",")]
#             if any(tag in kw.lower() for tag in db_tags):
#                 results.append({"keyword": kw, "url": row[0]})
#     conn.close()
#     return results


# def get_links_for_keywords(keywords, db_path="links.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     results = []
#     for kw in keywords:
#         pattern = f"%{kw.lower()}%"
#         cursor.execute("""
#             SELECT url, topic_tags FROM resources WHERE LOWER(topic_tags) LIKE ?
#         """, (pattern,))
#         for row in cursor.fetchall():
#             db_tags = [tag.strip().lower() for tag in row[1].split(",")]
#             if kw.lower() in db_tags:
#                 results.append({"keyword": kw, "url": row[0]})
#     conn.close()
#     return results


# def get_images_for_keywords(keywords, db_path="media.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     results = []
#     for kw in keywords:
#         pattern = f"%{kw.lower()}%"
#         cursor.execute("""
#             SELECT url, tags FROM images WHERE LOWER(tags) LIKE ?
#         """, (pattern,))
#         for row in cursor.fetchall():
#             db_tags = [tag.strip().lower() for tag in row[1].split(",")]
#             if kw.lower() in db_tags:
#                 results.append({"keyword": kw, "url": row[0]})
#     conn.close()
#     return results


def tokenize(text):
    return re.split(r"[,\s\-]+", text.lower())

def get_links_for_keywords(keywords, db_path="links.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    results = []
    for kw in keywords:
        kw_parts = tokenize(kw)
        pattern = f"%{kw_parts[0]}%"
        cursor.execute("""
            SELECT url, topic_tags FROM resources WHERE LOWER(topic_tags) LIKE ?
        """, (pattern,))
        for row in cursor.fetchall():
            db_tags = tokenize(row[1])
            if any(part in db_tags for part in kw_parts):
                results.append({"keyword": kw, "url": row[0]})
    conn.close()
    return results

def get_images_for_keywords(keywords, db_path="media.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    results = []
    for kw in keywords:
        kw_parts = tokenize(kw)
        pattern = f"%{kw_parts[0]}%"
        cursor.execute("""
            SELECT url, tags FROM images WHERE LOWER(tags) LIKE ?
        """, (pattern,))
        for row in cursor.fetchall():
            db_tags = tokenize(row[1])
            if any(part in db_tags for part in kw_parts):
                results.append({"keyword": kw, "url": row[0]})
    conn.close()
    return results
