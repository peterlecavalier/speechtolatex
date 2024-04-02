import subprocess
import os
from firebase_admin import credentials, initialize_app, storage


def compile_latex(document_id, latex_string):
    
    directory = "./output"  # Ensure this directory exists

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # File paths incorporating the document ID
    tex_file_path = os.path.join(directory, f"{document_id}.tex")
    pdf_file_path = os.path.join(directory, f"{document_id}.pdf")



    # Write the LaTeX code to a .tex file
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write(latex_string)

    # Compile the .tex file to PDF using pdflatex
    subprocess.run(['pdflatex', '-output-directory', directory, tex_file_path])




def upload_pdf(document_id, user_id):

    directory = "./output"  # Ensure this directory exists

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

     # File paths incorporating the document ID
    tex_file_path = os.path.join(directory, f"{document_id}.tex")
    pdf_file_path = os.path.join(directory, f"{document_id}.pdf")
    aux_file_path = os.path.join(directory, f"{document_id}.aux")
    log_file_path = os.path.join(directory, f"{document_id}.log")

    # # Initialize Firebase Admin, replace with your Firebase setup details
    # cred = credentials.Certificate('firebase.json')
    # initialize_app(cred, {'storageBucket': 'your-bucket-name.appspot.com'})

    # Reference to your Firebase Storage bucket
    bucket = storage.bucket()

    # Upload the PDF to Firebase Storage
    with open(pdf_file_path, 'rb') as pdf_file:
        blob = bucket.blob(f'pdfs/{document_id}.pdf')
        blob.metadata = {
            'document_id': document_id,
            'user_id': user_id
        }
        blob.upload_from_file(pdf_file, content_type='application/pdf')



    # After successful upload, delete the .tex and .pdf files
    os.remove(tex_file_path)
    os.remove(pdf_file_path)
    os.remove(aux_file_path)
    os.remove(log_file_path)