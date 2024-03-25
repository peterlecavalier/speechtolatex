from flask import Flask, request, jsonify
import pymysql
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred)


# Load MySQL Database Configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'cursorclass': pymysql.cursors.DictCursor
}

# Get all files owned by a user
@app.route('/files', methods=['GET'])
def get_files():
    # Verify Firebase auth token
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except Exception as e:
        return jsonify({'error': 'Invalid or expired Firebase token.'}), 401

    # Retrieve files from MySQL database
    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM files WHERE userId = %s"
                cursor.execute(sql, (user_id,))
                files = cursor.fetchall()
                return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a file, user must own the file
@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    # Verify Firebase auth token
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except Exception as e:
        return jsonify({'error': 'Invalid or expired Firebase token.'}), 401

    # Retrieve the specific file from MySQL database
    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM files WHERE id = %s AND userId = %s"
                cursor.execute(sql, (file_id, user_id))
                file = cursor.fetchone()
                if file:
                    return jsonify(file)
                else:
                    return jsonify({'error': 'File not found or access denied.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete a file, user must own the file
@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    # Verify Firebase auth token
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except Exception as e:
        return jsonify({'error': 'Invalid or expired Firebase token.'}), 401

    # Delete the specific file from MySQL database
    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                # Check if the file exists and belongs to the user before attempting to delete
                check_sql = "SELECT id FROM files WHERE id = %s AND userId = %s LIMIT 1"
                cursor.execute(check_sql, (file_id, user_id))
                if cursor.fetchone():
                    # File exists and belongs to the user; proceed with delete
                    delete_sql = "DELETE FROM files WHERE id = %s"
                    cursor.execute(delete_sql, (file_id,))
                    connection.commit()
                    if cursor.rowcount > 0:
                        return jsonify({'message': 'File deleted successfully.'}), 200
                    else:
                        return jsonify({'error': 'File not found.'}), 404
                else:
                    return jsonify({'error': 'File not found or access denied.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Create a file, user must be auth
@app.route('/files', methods=['POST'])
def add_file():
    # Verify Firebase auth token
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except Exception as e:
        return jsonify({'error': 'Invalid or expired Firebase token.'}), 401

    # Extract file data from request
    try:
        data = request.json
        title = data.get('title')
        text = data.get('text')
        latex = data.get('latex')
        
        if not title:  # Title is required
            return jsonify({'error': 'Title is required.'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid input.'}), 400

    # Insert file into MySQL database
    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO files (title, text, latex, userId)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (title, text, latex, user_id))
                connection.commit()
                return jsonify({'message': 'File added successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)