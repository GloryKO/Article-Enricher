import sqlite3

def query_media_db():
    """Query the media.db for images and videos"""
    try:
        conn = sqlite3.connect("media.db")
        
        # Query images table
        print("=== IMAGES ===")
        cursor = conn.execute("SELECT id, url, title, description, tags FROM images LIMIT 10")
        for row in cursor:
            print(f"ID: {row[0]}, URL: {row[1]}, Title: {row[2]}, Description: {row[3]}, Tags: {row[4]}")
        
        print("\n=== VIDEOS ===")
        # Query videos table
        cursor = conn.execute("SELECT id, url, title, description, tags FROM videos LIMIT 10")
        for row in cursor:
            print(f"ID: {row[0]}, URL: {row[1]}, Title: {row[2]}, Description: {row[3]}, Tags: {row[4]}")
            
    except sqlite3.Error as e:
        print(f"Error querying media.db: {e}")
    finally:
        if conn:
            conn.close()

def query_links_db():
    """Query the links.db for resources"""
    try:
        conn = sqlite3.connect("links.db")
        
        print("=== RESOURCES ===")
        cursor = conn.execute("SELECT id, url, title, description, topic_tags, type FROM resources LIMIT 10")
        for row in cursor:
            print(f"ID: {row[0]}, URL: {row[1]}, Title: {row[2]}, Description: {row[3]}, Topic Tags: {row[4]}, Type: {row[5]}")
            
    except sqlite3.Error as e:
        print(f"Error querying links.db: {e}")
    finally:
        if conn:
            conn.close()

def inspect_db_schema(db_path):
    """Inspect the actual schema of a database to see what tables and columns exist"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n=== SCHEMA FOR {db_path} ===")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get column info for each table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
                
    except sqlite3.Error as e:
        print(f"Error inspecting {db_path}: {e}")
    finally:
        if conn:
            conn.close()

def main():
    # First, inspect the actual schema of both databases
    inspect_db_schema("media.db")
    inspect_db_schema("links.db")
    
    print("\n" + "="*50)
    print("QUERYING DATA")
    print("="*50)
    
    # Query both databases
    query_media_db()
    print()
    query_links_db()

if __name__ == "__main__":
    main()

    