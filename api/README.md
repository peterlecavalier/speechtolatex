# API

## Features
- Add a file to the db
- Get all files from a user


## Install
1. Clone the repo
2. CD into the repo
3. CD  into the api `cd api`
4. Install required packages
```
pip3 install Flask PyMySQL firebase-admin python-dotenv
```
5. Create a .env file with the following:
```
DB_HOST=""
DB_USER=""
DB_PASSWORD=""
DB_DATABASE=""
FIREBASE_PROJECT_ID=""
```
6. Put the Firebase admin json as `firebase.json`. Firebase project home > click the cog in the top left > Project Settings > Service accounts > Generate new private key
7. Install some sort of pdflatex cli tool

## Usage
`python3 app.py`
