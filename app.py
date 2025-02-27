from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="test_db"
)
cursor = db.cursor()

# Create users table (Run this once in MySQL)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
""")
db.commit()

# Insert sample users (Run this once)
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'password1')")
db.commit()

# Vulnerable Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # 🚨 SQL Injection Vulnerability 🚨
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        print(f"Executing Query: {query}")  # Debugging

        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return "✅ Login successful!"
        else:
            return "❌ Login failed!"

    return render_template_string("""
        <form method="post">
            <input type="text" name="username" placeholder="Username"><br>
            <input type="password" name="password" placeholder="Password"><br>
            <input type="submit" value="Login">
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
