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
    
    def update_user(self,old_email):
        mod_user = {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "password": self.password
        }
        result=db_manager.update_user(mod_user,old_email)
        return result
    
    def get_email(self):
        return self.email

    def set_name(self,name):
        self.name=name
    
    def set_surname(self,surname):
        self.surname=surname
    
    def set_email(self,email):
        self.email=email
    
    def set_password(self,password):
        new_password=crypto.hash_password(password)
        self.password=new_password

    def check_password(self, password):
        return crypto.verify_password(self.password,password)