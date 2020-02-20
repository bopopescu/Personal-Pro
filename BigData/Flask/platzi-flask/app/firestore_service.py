import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

project_id = 'platzi-flask-99'
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential,{'projectId': project_id})

db = firestore.client()

def get_user():
    return db.collection('users').get()

def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()
