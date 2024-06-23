"""
Main
"""
from os import environ
from datetime import datetime
from flask import Flask, request, jsonify
from database import DatabaseManager

app = Flask(__name__)

db_host = environ.get('DATABASE_HOST', 'localhost')
db_user = environ.get('DATABASE_USERNAME', 'username')
db_password = environ.get('DATABASE_PASSWORD')
db_name = environ.get('DATABASE_NAME', 'api')
db_table_name = environ.get('DATABASE_TABLE_NAME',"users")

db_manager = DatabaseManager(db_host, db_user, db_password, db_name, db_table_name)
db_manager.create_table()

@app.route('/hello/<username>', methods=['PUT'])
def add_user(username):
    """Put username and birthday info."""
    data = request.get_json()
    date_of_birth = data.get('dateOfBirth')
    try:
        current_date = datetime.now().date()
        if not username.isalpha():
            return jsonify({"message": "Username should contain only letters"}), 400
        if datetime.strptime(date_of_birth, "%Y-%m-%d").date() >= current_date:
            return jsonify({"message": "Birthday should be a date before the today date"}), 400
        db_manager.write_data(username, date_of_birth)
        return jsonify({"message": "User added/updated successfully"}), 204
    except Exception as err:
        return jsonify({"error": str(err)}), 400

@app.route('/hello/<username>', methods=['GET'])
def get_user(username):
    """Get user and return the number of days till next birthday"""
    try:
        user = db_manager.get_data(username)
        if user:
            today = datetime.today().date()
            birthday = user['birthday']
            next_birthday = birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            if days_left == 0:
                output = jsonify({"message": f"Hello, {username}! Happy birthday!"}), 200
            else:
                output = jsonify({"message": f"Hello, {username}! Your birthday is "
                                              f"in {days_left} day(s)"}), 200
            return output
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 400

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    conn = db_manager.connect()
    if conn:
        conn.close()
        return jsonify({"status": "healthy"}), 200
    else:
        return jsonify({"status": "unhealthy"}), 500

if __name__ == '__main__':
    app.run(debug=True)
