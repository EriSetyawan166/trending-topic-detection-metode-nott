import mysql.connector

def connect_db(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    return conn, cursor

def main():
    # Connect to the database
    conn, cursor = connect_db("localhost", "root", "", "deteksi_trending_topik")
    
    # Execute a query to fetch some data from the database
    cursor.execute("SELECT text_bersih FROM dokumen")
    rows = cursor.fetchall()
    
    # Print the fetched data
    for row in rows:
        print(row)
    
    # Close the database connection
    cursor.close()
    conn.close()

    
if __name__ == "__main__":
    main()
