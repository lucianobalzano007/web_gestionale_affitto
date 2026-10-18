def NumberToTextInteger(n):
    """ 
        Precondizione: deve essere un intero
        Postcondizione: Ritorna un numero tradotto in lettere
    """
    if n == 0: 
        return ""
    elif n <= 19:
        return ("UNO", "DUE", "TRE", "QUATTRO", "CINQUE", 
                "SEI", "SETTE", "OTTO", "NOVE", "DIECI", 
                "UNDICI", "DODICI", "TREDICI", 
                "QUATTORDICI", "QUINDICI", "SEDICI", 
                "DICIASETTE", "DICIOTTO", "DICIANNOVE")[n-1]
                 
    elif n <= 99:
        decine = ("VENTI", "TRENTA", "QUARANTA",
                  "CINQUANTA", "SESSANTA", 
                  "SETTANTA", "OTTANTA", "NOVANTA")
        letter = decine[int(n/10)-2]
        t = n%10
        if t == 1 or t == 8:
            letter = letter[:-1]
        return letter + NumberToTextInteger(n%10)
         
    elif n <= 199:
        return "CENTO" + NumberToTextInteger(n%100)
         
    elif n <= 999:
        m = n%100
        m = int(m/10)
        letter = "CENT"
        if m != 8:
            letter = letter + "O"
        return NumberToTextInteger( int(n/100)) + \
               letter + \
               NumberToTextInteger(n%100)
         
    elif n<= 1999 :
        return "MILLE" + NumberToTextInteger(n%1000)
     
    elif n<= 999999:
        return NumberToTextInteger(int(n/1000)) + \
               "MILA" + \
               NumberToTextInteger(n%1000)
         
    elif n <= 1999999:
        return "UNMILIONE" + NumberToTextInteger(n%1000000)
         
    elif n <= 999999999:
        return NumberToTextInteger(int(n/1000000))+ \
               "MILIONI" + \
               NumberToTextInteger(n%1000000)
    elif n <= 1999999999:
        return "UNMILIARDO" + NumberToTextInteger(n%1000000000)
         
    else:
        return NumberToTextInteger(int(n/1000000000)) + \
               "MILIARDI" + \
               NumberToTextInteger(n%1000000000)
 
def NumberToText(x, pos=2):
   """ 
        Precondizione: deve essere un float
        Postcondizione: Ritorna un numero tradotto in lettere secondo un formato finanziario
   """
   sign = ""
   if x<0:
      sign = "meno"
      x = abs(x)
   x = round(x, pos)
   n = int(x)
   frmt = "{0:0."+"{0:d}".format(pos)+"f}"
   spic = frmt.format(x-n)[2:]
   if n == 0:
      num = "zero"
   else:
      num = NumberToTextInteger(n)
   return sign+num+"/"+spic
 
# prelevo il valore numerico

def calcolo_iva_totale(ivap,prezzo_no_iva):
    iva=(ivap*prezzo_no_iva)/100
    prezzo_totale=iva+prezzo_no_iva
    return prezzo_totale

def calcolo_iva(ivap,prezzo_no_iva):
    iva=(ivap*prezzo_no_iva)/100
    return iva

def check_zero(numero):
    if numero=='':
        return 0
    else:
        return float(numero)