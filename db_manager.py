from pymongo import MongoClient
import pymongo
from pymongo import collection
from os import getenv
from datetime import datetime

key_contr=['_id','tipo_abi','ind_abi','city_abi','prov_abi','note_abi','ag_contr','datarec_contr','datasti_contr','cod_contr','durata_contr','nome_loc','cog_loc','cf_loc','nome_cond','cog_cond','cf_cond']
key_ric=['_id','codice_id','num_ric','data_ric','datain_ric','dataout_ric','cas1imp_ric','cas2_ric','cas2imp_ric','cas3_ric','cas3imp_ric','cas4_ric','cas4imp_ric','cas5_ric','cas5imp_ric','iva_ric','totale_senza_iva','iva','totale_iva','pagato']

def check_key_contr(dataframe):
    '''
        Precondizione: nessuna
        Postcondizione: controlla se le key dei contratti di un dataframe coincidono ritornando 0 se coincidono altrimenti ritorna 1
    '''
    i=0
    for key in dataframe:
        if key_contr[i]!=key:
            return 1
        i+=1
    return 0

def check_key_ric(dataframe):
    '''
        Precondizione: nessuna
        Postcondizione: controlla se le key delle ricevute di un dataframe coincidono ritornando 0 se coincidono altrimenti ritorna 1
    '''
    i=0
    for key in dataframe:
        if key_ric[i]!=key:
            return 1
        i+=1
    return 0

def db_init():
    '''
        Precondizione: nessuna
        Postcondizione: Crea la connessione con mongodb
    '''
    host_mongo = getenv('MONGO_HOST_NAME')
    user_mongo = getenv('MONGO_INITDB_ROOT_USERNAME')
    password_mongo = getenv('MONGO_INITDB_ROOT_PASSWORD')
    connection_string = f"mongodb://{user_mongo}:{password_mongo}@{host_mongo}:27017/"
    #connection_string = f"mongodb://example:example@localhost:27017/"
    client = MongoClient(connection_string)
    return client['Gestionale_Affitto_DB']

def inserimento_contratto(contratto):
    '''
        Precondizione: deve essere un dizionario
        Postcondizione: Inserimento del contratto all'interno del db ritornando 0, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['contratti']
    try:
        result=collection_name.insert_one(contratto)
    except Exception as e:
        print(e)
    else:
        return 0

def preleva_contratti():
    '''
        Precondizione: nessuna
        Postcondizione: Ritorna una lista di tuple di contratti, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['contratti']
    try:
        lista=collection_name.find()
    except Exception as e:
        return 1
    else:
        return lista

def eliminazione_contratto(codice):
    '''
        Precondizione: nessuna
        Postcondizione: Elimina un elemento dal db ritornando 0, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['contratti']
    try:
        result=collection_name.delete_one({"_id":collection.ObjectId(codice)})
    except Exception as e:
        return 1
    else:
        return 0

def cerca_contratto(codice):
    '''
        Precondizione:nessuna
        Postcondizione:mi ritorna il contratto di locazione, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['contratti']
    print(codice)
    try:
        result=collection_name.find_one({"_id":collection.ObjectId(codice)})
    except Exception as e:
        print(e)
    finally:
        return result

def update_contratto(codice,modifica):
    '''
        Precondizione:nessuna
        Postcondizione:modifica il contratto di locazione ritornando 0, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['contratti']
    print(modifica)
    try:
        result=collection_name.update_one(filter={"_id":collection.ObjectId(codice)},update={'$set':modifica})
    except Exception as e:
        return 1
    else:
        return 0

def salvataggio_ricevuta(ricevuta):
    '''
        Precondizione:nessuna
        Postcondizione:Inserimento della ricevuta all'interno del db ritornando 0, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.insert_one(ricevuta)
    except Exception as e:
        return 1
    else:
        return 0

def conta_ricevute(codice_id):
    '''
        Precondizione: nessuna
        Postcondizione: ritorna il numero delle ricevute per un determinato contratto
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.count_documents({'codice_id':codice_id})
    except Exception as e:
        return 1
    else:
        return result

def cerca_ricevute(codice_id):
    '''
        Precondizione:nessuna
        Postcondizione:Creazione lista di tupla di ricevute di quel codice, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        lista=collection_name.find({'codice_id':codice_id})
    except Exception as e:
        return 1
    else:
        dati=[]
        for element in lista:
            ricevuta=()
            for elemento in element.values():
                el=(elemento,)
                ricevuta=ricevuta+el
            dati.append(ricevuta)
        return dati

def eliminazione_ricevuta(codice_id):
    '''
        Precondizione:nessuna
        Postcondizione:Eliminazione ricevuta, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.delete_one({"_id":codice_id})
        return 0
    except Exception as e:
        return 1

def cerca_ricevuta(codice_id):
    '''
        Precondizione:nessuna
        Postcondizione:Ritorna la ricevuta d'affitto, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.find_one({"_id":codice_id})
    except Exception as e:
        return 1
    finally:
        ricevuta=()
        for elemento in result.values():
            el=(elemento,)
            ricevuta=ricevuta+el
        return ricevuta

def update_ricevuta(codice_id,ricevuta):
    '''
        Precondizione:nessuna
        Postcondizione:Modifica la ricevuta d'affitto ritornando 0, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.update_one(filter={'_id':codice_id,},update={'$set':ricevuta})
    except Exception as e:
        return 1
    else:
        return 0

def cerca_ricevuta_nt(codice_id):
    '''
        Precondizione:nessuna
        Postcondizione:Ritorna la ricevuta d'affitto, altrimenti ritorna 1 come errore
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.find_one({"_id":codice_id})
    except Exception as e:
        return 1
    finally:
        return result

def eliminazione_ricevute(codice_id):
    '''
        Precondizione: nessuna
        Postcondizione: elimina tutte le ricevute collegate a quel codice ritornando 0, altrimenti ritorna 1
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        result=collection_name.delete_many({'codice_id':codice_id})
    except Exception as e:
        return 1
    else:
        return 0

def preleva_ricevute():
    '''
        Precondizione: nessuna
        Postcondizione: Preleva le ricevute d'affitto dal db, altrimenti ritorna 1
    '''
    db=db_init()
    collection_name=db['ricevute']
    try:
        lista=collection_name.find()
    except Exception as e:
        return 1
    else:
        dati=[]
        for element in lista:
            i=0
            ricevuta=()
            for elemento in element.values():
                el=(elemento,)
                ricevuta=ricevuta+el
            dati.append(ricevuta)
        return dati

def get_keys(collection):
    '''
        Precondizione: nessuna
        Postcondizione: Preleva le chiavi dal db, altrimenti ritorna 1
    '''
    db=db_init()
    collection_name=db[collection]
    try:
        result=collection_name.find()
    except Exception as e:
        return 1
    else:
        chiavi=[]
        for element in result:
            for chiave in element.keys():
                chiavi.append(chiave)
            return chiavi

def db_erase():
    '''
        Precondizione: nessuna
        Postcondizione: cancella tutto il db ritornando 0, altrimenti ritorna 1
    '''
    db=db_init()
    collection_name_contr=db['contratti']
    collection_name_ric=db['ricevute']
    try:
        result=collection_name_contr.delete_many(filter={})
        result=collection_name_ric.delete_many(filter={})
    except Exception as e:
        return 1
    else: 
        return 0

def create_user(utente):
    '''
        Precondizione: nessuna
        Postcondizione: crea un nuovo e singolo utente all'interno del db
    '''
    db=db_init()
    collection_name=db['utente']
    try:
        result=collection_name.insert_one(utente)
    except Exception as e:
        print(e)
    else:
        return 0

def trova_utente(email):
    '''
        Precondizione: nessuna
        Postcondizione: cerca l'utente all'interno del db
    '''
    db=db_init()
    collection_name=db['utente']
    try:
        result=collection_name.find_one({'email':email})
    except Exception as e:
        print(e)
    else:
        return result

def conta_utenti():
    db=db_init()
    collection_user=db['utente']
    result=collection_user.count_documents({})
    return result