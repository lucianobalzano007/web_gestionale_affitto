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