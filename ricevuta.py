import db_manager as db
from contratto import Contratto
from finicial import *
from file_manager import *
import data_manager
import os
import api_telegram

class Ricevuta():
    def __init__(self,codice_id,num_ric,data_ric,datain_ric,dataout_ric,cas1imp_ric,cas2_ric,cas2imp_ric,cas3_ric,cas3imp_ric,cas4_ric,cas4imp_ric,cas5_ric,cas5imp_ric,pagato_ric,iva_ric):
        self.codice_id=codice_id
        self.num_ric=num_ric
        self.data_ric=data_ric
        self.datain_ric=datain_ric
        self.dataout_ric=dataout_ric
        self.cas1imp_ric=cas1imp_ric
        self.cas2_ric=cas2_ric
        self.cas2imp_ric=cas2imp_ric
        self.cas3_ric=cas3_ric
        self.cas3imp_ric=cas3imp_ric
        self.cas4_ric=cas4_ric
        self.cas4imp_ric=cas4imp_ric
        self.cas5_ric=cas5_ric
        self.cas5imp_ric=cas5imp_ric
        self.pagato_ric=pagato_ric
        self.iva_ric=iva_ric
    
    def creazione_ricevuta(self):
        id_ric=self.num_ric+'-'+self.codice_id
        cas1imp=check_zero(self.cas1imp_ric)
        cas2imp=check_zero(self.cas2imp_ric)
        cas3imp=check_zero(self.cas3imp_ric)
        cas4imp=check_zero(self.cas4imp_ric)
        cas5imp=check_zero(self.cas5imp_ric)
        iva=check_zero(self.iva_ric)
        totale_senza_iva=format(cas1imp+cas2imp+cas3imp+cas4imp+cas5imp,'.2f')
        totale_iva=format(calcolo_iva_totale(iva,float(totale_senza_iva)),'.2f')
        iva_eur=format(calcolo_iva(iva,float(totale_senza_iva)),'.2f')
        ricevuta={
            '_id':id_ric,
            'codice_id':self.codice_id,
            'num_ric':self.num_ric,
            'data_ric':self.data_ric,
            'datain_ric':self.datain_ric,
            'dataout_ric':self.dataout_ric,
            'cas1imp_ric':self.cas1imp_ric,
            'cas2_ric':self.cas2_ric,
            'cas2imp_ric':self.cas2imp_ric,
            'cas3_ric':self.cas3_ric,
            'cas3imp_ric':self.cas3imp_ric,
            'cas4_ric':self.cas4_ric,
            'cas4imp_ric':self.cas4imp_ric,
            'cas5_ric':self.cas5_ric,
            'cas5imp_ric':self.cas5imp_ric,
            'iva_ric':self.iva_ric,
            'totale_senza_iva':totale_senza_iva,
            'iva':iva_eur,
            'totale_iva':totale_iva,
            'pagato':self.pagato_ric
        }
        result=db.salvataggio_ricevuta(ricevuta)
        contratto=Contratto.get_contratto_json(self.codice_id)
        if result!=1:
            buffer = stampa_ricevuta_pdf(contratto,ricevuta)
            contr=Contratto.get_contratto(self.codice_id)
            chat_id=contr.get_chat_id()
            if chat_id!="null" and os.getenv('BOT_TOKEN')!='null':
                pippo=self.__create_telegram_message__(chat_id,cas1imp,cas2imp,cas3imp,cas4imp,cas5imp,iva,totale_senza_iva,totale_iva,iva_eur)
            return buffer
        else:
            return result
    
    def update_ricevuta(self,cod_ric):
        id_ric=self.num_ric+'-'+self.codice_id
        cas1imp=check_zero(self.cas1imp_ric)
        cas2imp=check_zero(self.cas2imp_ric)
        cas3imp=check_zero(self.cas3imp_ric)
        cas4imp=check_zero(self.cas4imp_ric)
        cas5imp=check_zero(self.cas5imp_ric)
        iva=check_zero(self.iva_ric)
        totale_senza_iva=format(cas1imp+cas2imp+cas3imp+cas4imp+cas5imp,'.2f')
        totale_iva=format(calcolo_iva_totale(iva,float(totale_senza_iva)),'.2f')
        iva_eur=format(calcolo_iva(iva,float(totale_senza_iva)),'.2f')
        ricevuta={
            '_id':id_ric,
            'codice_id':self.codice_id,
            'num_ric':self.num_ric,
            'data_ric':self.data_ric,
            'datain_ric':self.datain_ric,
            'dataout_ric':self.dataout_ric,
            'cas1imp_ric':self.cas1imp_ric,
            'cas2_ric':self.cas2_ric,
            'cas2imp_ric':self.cas2imp_ric,
            'cas3_ric':self.cas3_ric,
            'cas3imp_ric':self.cas3imp_ric,
            'cas4_ric':self.cas4_ric,
            'cas4imp_ric':self.cas4imp_ric,
            'cas5_ric':self.cas5_ric,
            'cas5imp_ric':self.cas5imp_ric,
            'iva_ric':self.iva_ric,
            'totale_senza_iva':totale_senza_iva,
            'iva':iva_eur,
            'totale_iva':totale_iva,
            'pagato':self.pagato_ric
        }
        result_el=db.eliminazione_ricevuta(cod_ric)
        if result_el==0:
            result=db.salvataggio_ricevuta(ricevuta)
        else:
            return 1
        return result

    def get_lista_ricevute(id_contr):
        lista_mongo=Ricevuta.get_lista_ricevute_json(id_contr)
        lista_ricevute=[]
        for ric in lista_mongo:
            element=Ricevuta(ric['codice_id'],ric['num_ric'],ric['data_ric'],ric['datain_ric'],ric['dataout_ric'],ric['cas1imp_ric'],ric['cas2_ric'],ric['cas2imp_ric'],ric['cas3_ric'],ric['cas3imp_ric'],ric['cas4_ric'],ric['cas4imp_ric'],ric['cas5_ric'],ric['cas5imp_ric'],ric['pagato'],ric['iva_ric'])
            codice=str(ric['_id'])
            totale_senza_iva=format(check_zero(element.cas1imp_ric)+check_zero(element.cas2imp_ric)+check_zero(element.cas3imp_ric)+check_zero(element.cas4imp_ric)+check_zero(element.cas5imp_ric),'.2f')
            totale_iva=format(calcolo_iva_totale(check_zero(element.iva_ric),check_zero(totale_senza_iva)),'.2f')
            anno=data_manager.estrai_anno(element.data_ric)
            mese=data_manager.estrai_mese(element.data_ric)
            elemento=[element,codice,totale_iva,mese,anno]
            lista_ricevute.append(elemento)
        return lista_ricevute
    
    def get_lista_ricevute_by_year(id_contr,year):
        lista_mongo=Ricevuta.get_lista_ricevute_json(id_contr)
        lista_ricevute=[]
        for ric in lista_mongo:
            element=Ricevuta(ric['codice_id'],ric['num_ric'],ric['data_ric'],ric['datain_ric'],ric['dataout_ric'],ric['cas1imp_ric'],ric['cas2_ric'],ric['cas2imp_ric'],ric['cas3_ric'],ric['cas3imp_ric'],ric['cas4_ric'],ric['cas4imp_ric'],ric['cas5_ric'],ric['cas5imp_ric'],ric['pagato'],ric['iva_ric'])
            codice=str(ric['_id'])
            totale_senza_iva=format(check_zero(element.cas1imp_ric)+check_zero(element.cas2imp_ric)+check_zero(element.cas3imp_ric)+check_zero(element.cas4imp_ric)+check_zero(element.cas5imp_ric),'.2f')
            totale_iva=format(calcolo_iva_totale(check_zero(element.iva_ric),check_zero(totale_senza_iva)),'.2f')
            anno=data_manager.estrai_anno(element.data_ric)
            mese=data_manager.estrai_mese(element.data_ric)
            if anno==year:
                elemento=[element,codice,totale_iva,mese,anno]
                lista_ricevute.append(elemento)
        return lista_ricevute
    
    def get_pagato_ric(self):
        return self.pagato_ric
    
    def get_num_ric(self):
        return self.num_ric

    def eliminazione_ricevute(id_contr):
        return db.eliminazione_ricevute(id_contr)
    
    def elimina_ricevuta(id_ric):
        return db.eliminazione_ricevuta(id_ric)
    
    def conta_ricevute(id_contr):
        return db.conta_ricevute(id_contr)
    
    def get_ricevuta_json(id_ric):
        return db.cerca_ricevuta(id_ric)
    
    def stampa_ricevuta(id_ric,id_contr):
        contr=Contratto.get_contratto_json(id_contr)
        ric=Ricevuta.get_ricevuta_json(id_ric)
        return stampa_ricevuta_pdf(contr,ric)

    def get_lista_ricevute_json(id_contr):
        return db.cerca_ricevute(id_contr)
    
    def get_ricevuta(codice_ric):
        ric=db.cerca_ricevuta(codice_ric)
        elemento=Ricevuta(ric['codice_id'],ric['num_ric'],ric['data_ric'],ric['datain_ric'],ric['dataout_ric'],ric['cas1imp_ric'],ric['cas2_ric'],ric['cas2imp_ric'],ric['cas3_ric'],ric['cas3imp_ric'],ric['cas4_ric'],ric['cas4imp_ric'],ric['cas5_ric'],ric['cas5imp_ric'],ric['pagato'],ric['iva_ric'])
        return elemento
    
    def notify_ric(self,chat_id):
        cas1imp=check_zero(self.cas1imp_ric)
        cas2imp=check_zero(self.cas2imp_ric)
        cas3imp=check_zero(self.cas3imp_ric)
        cas4imp=check_zero(self.cas4imp_ric)
        cas5imp=check_zero(self.cas5imp_ric)
        iva=check_zero(self.iva_ric)
        totale_senza_iva=format(cas1imp+cas2imp+cas3imp+cas4imp+cas5imp,'.2f')
        totale_iva=format(calcolo_iva_totale(iva,float(totale_senza_iva)),'.2f')
        iva_eur=format(calcolo_iva(iva,float(totale_senza_iva)),'.2f')
        if chat_id!="null" and os.getenv('BOT_TOKEN')!='null':
            return self.__create_telegram_message__(chat_id,cas1imp,cas2imp,cas3imp,cas4imp,cas5imp,iva,totale_senza_iva,totale_iva,iva_eur)
        

    def __create_telegram_message__(self,chat_id,cas1imp,cas2imp,cas3imp,cas4imp,cas5imp,iva,totale_senza_iva,totale_iva,iva_eur):
        mese=data_manager.estrai_mese(self.datain_ric)
        anno=data_manager.estrai_anno(self.datain_ric)
        message = f"<b>⚠️ NOTIFICA DI RICEVUTA D'AFFITTO ⚠️</b>\n\n"
        message += f"<b>Ricevuta d'affitto {mese} {anno}</b>\n\n"
        message += "---------------------------------------\n"
        message += f"RICEVUTA N. {self.num_ric} del {data_manager.cambia_data_formato(self.data_ric)}\n"
        message += f"CAUSALE: Affitto dal {data_manager.cambia_data_formato(self.datain_ric)} al {data_manager.cambia_data_formato(self.dataout_ric)}\n"
        message += f"IMPORTO: {cas1imp} €\n"
        message += "---------------------------------------\n"

        if self.cas2_ric != "":
            message += f"CAUSALE: {self.cas2_ric}\n"
            message += f"IMPORTO: {cas2imp} €\n"
            message += "---------------------------------------\n"
        if self.cas3_ric != "":
            message += f"CAUSALE: {self.cas3_ric}\n"
            message += f"IMPORTO: {cas3imp} €\n"
            message += "---------------------------------------\n"
        if self.cas4_ric != "":
            message += f"CAUSALE: {self.cas4_ric}\n"
            message += f"IMPORTO: {cas4imp} €\n"
            message += "---------------------------------------\n"
        if self.cas5_ric != "":
            message += f"CAUSALE: {self.cas5_ric}\n"
            message += f"IMPORTO: {cas5imp} €\n"
            message += "---------------------------------------\n"

        message += f"Totale senza IVA: {totale_senza_iva} €\n"
        message += f"Perc. IVA su affitto: {iva} %\n"
        message += f"Totale IVA: {iva_eur} €\n\n"
        message += f"<b>TOTALE: {totale_iva} €</b>\n"  # Grassetto HTML
        return api_telegram.send_message(chat_id=chat_id, message=message)