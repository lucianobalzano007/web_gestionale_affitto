import db_manager as db
from finicial import *
from file_manager import *
import os

class Ricevuta():
    def __init__(self,contratto,codice_id,num_ric,data_ric,datain_ric,dataout_ric,cas1imp_ric,cas2_ric,cas2imp_ric,cas3_ric,cas3imp_ric,cas4_ric,cas4imp_ric,cas5_ric,cas5imp_ric,pagato_ric,iva_ric):
        self.contratto=contratto
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
        if result!=1:
            buffer = stampa_ricevuta_pdf(self.contratto,ricevuta)
            return buffer
        else:
            return result
    
    def update_ricevuta(self):
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
        result=db.update_ricevuta(id_ric,ricevuta)
        return result
