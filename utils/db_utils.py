import sqlite3
from typing import List, Dict
import re

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
