#imports and initialize
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("adv-program-firebase-adminsdk-fbsvc-88f8cc8cbc.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
test_collection = "test"
test_document = "test_2"
test_data = {'timestamp': firestore.firestore.SERVER_TIMESTAMP, 'Quantity_On_Hand': 10}
test_data_2 = {'timestamp': firestore.firestore.SERVER_TIMESTAMP, 'Quantity_On_Hand': 2}

#CRUD operations
#Create
def create_doc(collection, data):
    db.collection(collection).add(data)

def create_doc_with_id(collection, doc_id, data): #if you know the specific document id you want to update
    db.collection(collection).document(doc_id).set(data)

def create_doc_auto_id(collection, data): 
    db.collection(collection).document().set(data)

def create_doc_merge(collection, doc_id, data):
    db.collection(collection).document(doc_id).set(data, merge=True)

#Read
def read_doc_with_id(collection, doc_id): #Only usable if document ID known, unlikely in multi-user app
    result = db.collection(collection).document(doc_id).get()
    if result.exists:
        print(result.to_dict())

def read_all_docs(collection):
    docs = db.collection(collection).get()
    for doc in docs:
        print(doc.to_dict())

#Query
def read_docs_query(collection):
    docs = db.collection(collection).where("Quantity_On_Hand", "<", 4).get()
    for doc in docs:
        print(doc.to_dict())

#Update
def update_doc_with_id(collection, doc_id, field, new_value):
    db.collection(collection).document(doc_id).update({field: new_value})

#Delete
def delete_doc_with_id(collection, doc_id):
    db.collection(collection).document(doc_id).delete()

def delete_field_with_id(collection, doc_id, field):
    db.collection(collection).document(doc_id).update({field:firestore.firestore.DELETE_FIELD})

update_doc_with_id("test", "test_2", "Quantity_On_Hand", 1)