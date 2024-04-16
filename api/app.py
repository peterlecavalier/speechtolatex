import datetime
from flask import Flask, request, jsonify
import pymysql
import firebase_admin
from firebase_admin import credentials, auth, storage
from dotenv import load_dotenv
import os
from convert import compile_latex, upload_pdf
from flask_cors import CORS, cross_origin

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# CORS(app)

# Initialize Firebase Admin SDK
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {'storageBucket': f'{FIREBASE_PROJECT_ID}.appspot.com'})


# Load MySQL Database Configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'port': int(os.getenv('DB_PORT')),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'cursorclass': pymysql.cursors.DictCursor
}

# Get all files owned by a user
@app.route('/files', methods=['GET'])
@cross_origin()
def get_files():
    # Verify Firebase auth token
    try:
        id_token = request.headers.get('Authorization').split('Bearer ')[1]
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
@cross_origin()
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
    

@app.route('/files/<int:file_id>', methods=['PATCH'])
@cross_origin()
def patch_file(file_id):
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
        latex = data.get('latex')
        text = data.get('text')

        
        if not title:  # title is required
            return jsonify({'error': 'Title is required.'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid input.'}), 400



    # Retrieve the specific file from MySQL database
    try:


        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE files SET title = %s, latex = %s, text = %s WHERE id = %s AND userId = %s"
                cursor.execute(sql, (title, latex, text, file_id, user_id))

                if cursor.rowcount > 0:
                    connection.commit()

                    # If rows were updated, you can return a success response
                    # Note: You may need to adjust this part according to your application's requirements
                    return jsonify({'message': 'File updated successfully.'}), 200
                else:
                    return jsonify({
                        'error': 'File not found or access denied.',
                        'user_id': user_id,
                        'file_id': file_id
                    }), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete a file, user must own the file
@app.route('/files/<int:file_id>', methods=['DELETE'])
@cross_origin()
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
@cross_origin()
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


# Create a file, user must be auth
@app.route('/storage', methods=['POST'])
@cross_origin()
def upload_pdf_logic():
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
        id = data.get('id')
        latex = data.get('latex')
        
        if not any((id, latex)):
            return jsonify({'error': 'id and latex string required.'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid input.'}), 400

    try:
        compile_latex(id, latex)
        upload_pdf(id, user_id)
        return jsonify({'message': 'PDF uploaded successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Create a file, user must be auth
@app.route('/storage/<id>', methods=['GET'])
@cross_origin()
def get_pdf(id):
    # Verify Firebase auth token
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except Exception as e:
        return jsonify({'error': 'Invalid or xfexpired Firebase token.'}), 401



    # Insert file into MySQL database
    try:
        file_path = f'pdfs/{id}.pdf'
        bucket = storage.bucket()
        blob = bucket.blob(file_path)

        url = blob.generate_signed_url(version='v4', expiration=datetime.timedelta(days=1), method='GET')
        return jsonify({'url': url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ping', methods=['GET'])
@cross_origin()
def get_ping():
    return jsonify({"message": "pong"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
