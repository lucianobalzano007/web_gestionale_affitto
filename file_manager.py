from db_manager import *
from finicial import *
from ric_create import *
import data_manager
import pandas as pd
import csv
import os
import io

def stampa_ricevuta_pdf(contratto,dati_contratto):
    descr=contratto['tipo_abi']+' presso '+contratto['ind_abi']+' '+contratto['city_abi']+' ('+contratto['prov_abi']+')'
    totale_scritto=NumberToText(float(dati_contratto.get(('totale_iva'))))
    frase_totale='€  '+str(cast_float(dati_contratto.get('totale_iva')))+' dicasi in euro '+totale_scritto
    periodo='Affitto dal '+data_manager.cambia_data_formato(dati_contratto.get('datain_ric'))+' al '+data_manager.cambia_data_formato(dati_contratto.get('dataout_ric'))
    causali=[
        periodo,
        dati_contratto.get('cas2'),
        dati_contratto.get('cas2_ric'),
        dati_contratto.get('cas3_ric'),
        dati_contratto.get('cas4_ric'),
        dati_contratto.get('cas5_ric'),
    ]

    importi=[
        '€  '+str(cast_float(dati_contratto.get('cas1imp_ric'))),
        '€  '+str(cast_float(dati_contratto.get('cas2imp_ric'))),
        '€  '+str(cast_float(dati_contratto.get('cas3imp_ric'))),
        '€  '+str(cast_float(dati_contratto.get('cas4imp_ric'))),
        '€  '+str(cast_float(dati_contratto.get('cas5imp_ric'))),
    ]

    buffer = crea_ricevuta("Untitled",
                  dati_contratto.get('num_ric'),
                  data_manager.cambia_data_formato(dati_contratto.get('data_ric')),
                  contratto['ag_contr'],
                  data_manager.cambia_data_formato(contratto['datasti_contr']),
                  data_manager.cambia_data_formato(contratto['datarec_contr']),
                  contratto['cod_contr'],
                  contratto['durata_contr'],
                  descr,
                  contratto['cog_loc']+' '+contratto['nome_loc'],
                  contratto['cf_loc'],
                  contratto['cog_cond']+' '+contratto['nome_cond'],
                  contratto['cf_cond'],
                  contratto['note_abi'],
                  frase_totale,
                  causali,
                  importi,
                  str(cast_float(dati_contratto.get('totale_senza_iva'))),
                  str(cast_float(dati_contratto.get('iva_ric'))),
                  dati_contratto.get('iva'),
                  str(cast_float(dati_contratto.get('totale_iva')))
                  )
    return buffer

def cast_float(value):
    if value!="":
        return "{0:.2f}".format(float(value))
    else:
        return ""

def export_contratti_csv():
    '''
        Precondizione:nessuna
        Postcondizione:Esporta i contratti dal db in un file .csv ritornando quest'ultimo. In caso di errori ritorna 1
    '''
    contratti=preleva_contratti()
    keys=get_keys('contratti')
    if contratti==1 or keys==1:
        return 1
    csvfile=io.StringIO()
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(keys)
    for contratto in contratti:
        spamwriter.writerow(get_values(contratto))
    return csvfile

def export_ricevute_csv():
    '''
        Precondizione:nessuna
        Postcondizione:Esporta le ricevute dal db in un file .csv ritornando quest'ultimo. In caso di errori ritorna 1
    '''
    ricevute=preleva_ricevute()
    keys=get_keys('ricevute')
    if ricevute==1 or keys==1:
        return 1
    csvfile=io.StringIO()
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(keys)
    for ricevuta in ricevute:
        spamwriter.writerow(get_values(ricevuta))
    return csvfile
    
def export_csv_ric(finestra,codice_id):
    '''
        Precondizione: nessuna
        Postcondizione: esporta le ricevute del contratto selezionato ritornando 0, altrimenti ritorna 1
    '''
    filetype=[("File CSV", "*.csv")]
    ric_csv_file=tk.filedialog.asksaveasfilename(initialfile="Ricevute.csv",defaultextension=".csv",filetypes=filetype,parent=finestra)
    ricevute=cerca_ricevute(codice_id)
    keys=get_keys('ricevute')
    if ricevute==1 or keys==1:
        return 1
    with open(ric_csv_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(keys)
        for ricevuta in ricevute:
            spamwriter.writerow(ricevuta)
    return 0

def import_csv(finestra):
    '''
        Precondizione: le chiavi dei file .csv devono coincidere con le chiavi del db
        Postcondizione: inizzializza il db e importa tutto il file csv all'interno del db ritornando 0, altrimenti ritorna 1 per un errore generico, 7 per l'errore delle chiavi sul contratto, 8 l'errore invece sulle ricevute
    '''
    filetype=[("File CSV", "*.csv")]
    contr_csv_file=tk.filedialog.askopenfile(title='Selezione il file dei contratti',parent=finestra,filetypes=filetype)
    ric_csv_file=tk.filedialog.askopenfile(title='Selezione il file delle ricevute',parent=finestra,filetypes=filetype)
    dataframe_contr=pd.read_csv(contr_csv_file).fillna(value="NA")
    dataframe_ric=pd.read_csv(ric_csv_file).fillna(value="")
    res=check_key_contr(dataframe_contr)
    if res==1:
        return 7
    res=check_key_ric(dataframe_ric)
    if res==1:
        return 8
    result=db_erase()
    if result==1:
        return 1
    print(dataframe_contr.to_dict())
    for element in dataframe_contr.to_dict(orient='index').values():
        elemento={}
        chiave=element.get('_id')
        oid=pymongo.collection.ObjectId(chiave)
        element.update({'_id':oid})
        result=inserimento_contratto(element)
        if result==1:
            return 1
    for element in dataframe_ric.to_dict(orient='index').values():
        result=salvataggio_ricevuta(element)
        if result==1:
            return 1
    return 0