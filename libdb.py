import bcrypt 
import pymongo

class LibraryDatabase:
    def __init__(self, db_name='library'):
        self.db_name = db_name
        self.client = self.connect_to_database()

    def connect_to_database(self):
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017')
            db = client[self.db_name]
            print(f"Connected to MongoDB database '{self.db_name}'")
            return db
        except Exception as e:
            print(f"Error connecting to MongoDB database: {e}")
            return None

    def verify_user(self, email, password):
        try:
            user_collection = self.client['patrons'] 
            user = user_collection.find_one({'email': email})
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False

    def register_user(self, email, password, phone, first_name, middle_name, last_name, address, member_since):
        try:
            # password hashing before storing it in the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user_collection = self.client['patrons']
            # check if the email is already taken
            if not self.is_email_taken(email):
                user = {
                    'email': email,
                    'password': hashed_password.decode('utf-8'),
                    'phone': phone,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'address': address,
                    'is_admin': False,  
                    'member_since': member_since 
                }
                user_collection.insert_one(user)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    def is_email_taken(self, email):
        try:
            user_collection = self.client['patrons'] 
            return user_collection.find_one({'email': email}) is not None
        except Exception as e:
            print(f"Error checking email existence: {e}")
            return False

    def is_admin(self, email):
        try:
            user_collection = self.client['patrons']  
            user = user_collection.find_one({'email': email})
            return user and user.get('is_admin', False)
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False

    def get_username_by_email(self, email):
        try:
            user_collection = self.client['patrons']  
            user = user_collection.find_one({'email': email})
            if user:
                return user.get('first_name', None)
            else:
                return None
        except Exception as e:
            print(f"Error getting username by email: {e}")
            return None


