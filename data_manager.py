from datetime import datetime

def cambia_data_formato(data):
    '''
        precondizione: data stringa
        post_condizione: ritorna la data nel formato dd/mm/yyyy
    '''
    dt_obj = datetime.strptime(data, "%Y-%m-%d")
    # Poi formattarla nel nuovo formato dd/mm/yyyy
    data_formattata = dt_obj.strftime("%d/%m/%Y")
    return data_formattata

def estrai_anno(data):
    '''
        precondizione: data stringa
        post_condizione: ritorna l'anno
    '''
    dt_obj = datetime.strptime(data, "%Y-%m-%d")
    anno=dt_obj.strftime("%Y")
    return anno

def estrai_mese(data):
    '''
        precondizione: data stringa
        post_condizione: ritorna il mese a lettere
    '''
    dt_obj = datetime.strptime(data, "%Y-%m-%d")
    mese_num=dt_obj.strftime("%m")
    if mese_num=='01':
        return 'Gennaio'
    elif mese_num=='02':
        return 'Febbraio'
    elif mese_num=='03':
        return 'Marzo'
    elif mese_num=='04':
        return 'Aprile'
    elif mese_num=='05':
        return 'Maggio'
    elif mese_num=='06':
        return 'Giugno'
    elif mese_num=='07':
        return 'Luglio'
    elif mese_num=='08':
        return 'Agosto'
    elif mese_num=='09':
        return 'Settembre'
    elif mese_num=='10':
        return 'Ottobre'
    elif mese_num=='11':
        return 'Novembre'
    elif mese_num=='12':
        return 'Dicembre'