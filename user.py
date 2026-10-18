import db_manager
import crypto

class User:
    def __init__(self, name, surname, email, password):
        self.name=name
        self.surname=surname
        self.email=email
        self.password=password
    
    def create_user(self):
        new_password = crypto.hash_password(self.password)
        new_user = {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "password": new_password
        }
        db_manager.create_user(new_user)
    
    def get_user_by_email(email):
        user = db_manager.trova_utente(email)
        if user is None:
            return None
        utente = User(user["name"], user["surname"], user["email"], user["password"])
        return utente
    
    def check_password(self, password):
        hashed_password = crypto.hash_password(password)
        if self.password == hashed_password:
            return True
        else:
            return False