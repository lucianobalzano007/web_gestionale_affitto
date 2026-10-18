import db_manager as db

class Contratto():
    def __init__(self,tipo_abi,ind_abi,city_abi,prov_abi,note_abi,ag_contr,datarec_contr,datasti_contr,cod_contr,durata_contr,nome_loc,cog_loc,cf_loc,nome_cond,cog_cond,cf_cond):
        self.tipo_abi=tipo_abi
        self.ind_abi=ind_abi
        self.city_abi=city_abi
        self.prov_abi=prov_abi
        self.note_abi=note_abi
        self.ag_contr=ag_contr
        self.datarec_contr=datarec_contr
        self.datasti_contr=datasti_contr
        self.cod_contr=cod_contr
        self.durata_contr=durata_contr
        self.nome_loc=nome_loc
        self.cog_loc=cog_loc
        self.cf_loc=cf_loc
        self.nome_cond=nome_cond
        self.cog_cond=cog_cond
        self.cf_cond=cf_cond
    
    def crea_contratto_di_locazione(self):
        '''
            Precondizione:Nessuno
            Postcondizione: Carica il documento json su mongodb
        '''
        contratto={
            'tipo_abi':self.tipo_abi,
            'ind_abi':self.ind_abi,
            'city_abi':self.city_abi,
            'prov_abi':self.prov_abi,
            'note_abi':self.note_abi,
            'ag_contr':self.ag_contr,
            'datarec_contr':self.datarec_contr,
            'datasti_contr':self.datasti_contr,
            'cod_contr':self.cod_contr,
            'durata_contr':self.durata_contr,
            'nome_loc':self.nome_loc,
            'cog_loc':self.cog_loc,
            'cf_loc':self.cf_loc,
            'nome_cond':self.nome_cond,
            'cog_cond':self.cog_cond,
            'cf_cond':self.cf_cond
        }
        result=db.inserimento_contratto(contratto)
        return result
    
    def modifica_contratto_di_locazione(self,codice):
        contratto={
            'tipo_abi':self.tipo_abi,
            'ind_abi':self.ind_abi,
            'city_abi':self.city_abi,
            'prov_abi':self.prov_abi,
            'note_abi':self.note_abi,
            'ag_contr':self.ag_contr,
            'datarec_contr':self.datarec_contr,
            'datasti_contr':self.datasti_contr,
            'cod_contr':self.cod_contr,
            'durata_contr':self.durata_contr,
            'nome_loc':self.nome_loc,
            'cog_loc':self.cog_loc,
            'cf_loc':self.cf_loc,
            'nome_cond':self.nome_cond,
            'cog_cond':self.cog_cond,
            'cf_cond':self.cf_cond
        }
        result=db.update_contratto(codice,contratto)
        return result