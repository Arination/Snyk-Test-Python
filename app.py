import sqlite3

# Create an in-memory database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create a simple users table
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

# Insert test data
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'mypassword')")
conn.commit()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # 🚨 Vulnerable Query (Directly embedding user input)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"Executing Query: {query}")  # Debugging output

    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")

if __name__ == "__main__":
    login()
