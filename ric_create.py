from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def crea_ricevuta(
    nome_file="ricevuta_affitto_A5.pdf",
    numero_ricevuta="14",
    data_emissione="15/10/2026",
    ufficio_territoriale="",
    data_stipula="",
    data_registrazione="",
    codice_contratto="",
    durata_contratto="",
    descrizione_immobile="",
    locatore="",
    cf_locatore="",
    conduttore="",
    cf_conduttore="",
    note="",
    importo_lettere="",
    causali=None,
    importi=None,
    totale_importi="",
    percentuale_iva="",
    totale_iva="",
    totale=""
):
    # ==================================================
    # PAGINA A5 VERTICALE
    # ==================================================
    W, H = A5
    c = canvas.Canvas(nome_file, pagesize=A5)

    sx = 8 * mm
    dx = W - 8 * mm
    larghezza = dx - sx

    nero = colors.HexColor("#222222")
    grigio = colors.HexColor("#777777")
    chiaro = colors.HexColor("#EEEEEE")

    # ==================================================
    # FUNZIONI GRAFICHE
    # ==================================================
    def testo(x, y, contenuto, size=7.2, bold=False):
        c.setFillColor(nero)
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, size)
        c.drawString(x, y, str(contenuto))

    def linea(x1, y1, x2, y2, spessore=0.45):
        c.setStrokeColor(grigio)
        c.setLineWidth(spessore)
        c.line(x1, y1, x2, y2)

    def sezione(titolo, y):
        c.setFillColor(chiaro)
        c.rect(
            sx, y - 1.5 * mm,
            larghezza, 6 * mm,
            fill=1, stroke=0
        )
        c.setFillColor(nero)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(W / 2, y, titolo)

    def campo(
        etichetta,
        x,
        y,
        x_fine,
        spazio_etichetta=None,
        dato=""
    ):
        """
        Disegna etichetta, dato e linea.

        dato:
            Stringa o numero da stampare nel PDF.
            Se vuoto, il campo rimane in bianco.
        """
        dimensione = 7.2

        if etichetta:
            testo(x, y, etichetta, dimensione, True)

        if spazio_etichetta is None:
            spazio_etichetta = (
                c.stringWidth(
                    etichetta,
                    "Helvetica-Bold",
                    dimensione
                ) + 2 * mm
                if etichetta else 0
            )

        x_dato = x + spazio_etichetta

        if dato is not None and str(dato) != "":
            dato = str(dato)

            c.setFillColor(nero)
            c.setFont("Helvetica", dimensione)
            c.drawString(x_dato, y, dato)

            larghezza_dato = c.stringWidth(
                dato, "Helvetica", dimensione
            )

        else:
            pass

    def riga_tabella(y_top, altezza, riempita=False):
        if riempita:
            c.setFillColor(chiaro)
            c.rect(
                sx, y_top - altezza,
                larghezza, altezza,
                fill=1, stroke=0
            )

        c.setStrokeColor(grigio)
        c.setLineWidth(0.45)
        c.rect(
            sx, y_top - altezza,
            larghezza, altezza,
            fill=0, stroke=1
        )

    # ==================================================
    # PREPARAZIONE DELLE CINQUE CAUSALI
    # ==================================================
    if causali is None:
        causali = [""] * 5

    if importi is None:
        importi = [""] * 5

    causali = list(causali)[:5]
    importi = list(importi)[:5]

    causali += [""] * (5 - len(causali))
    importi += [""] * (5 - len(importi))

    # ==================================================
    # INTESTAZIONE
    # ==================================================
    testo(sx, 201 * mm, "Ricevuta d'Affitto", 14, True)

    campo(
        "Ricevuta n.",
        88 * mm, 201 * mm, dx,
        17 * mm, dato=numero_ricevuta
    )

    campo(
        "Data emissione:",
        88 * mm, 194 * mm, dx,
        24 * mm, dato=data_emissione
    )

    # ==================================================
    # MARCA DA BOLLO: 55 x 44 mm
    # ==================================================
    bollo_w = 55 * mm
    bollo_h = 44 * mm
    bollo_x = sx
    bollo_y = 145 * mm

    c.setStrokeColor(grigio)
    c.setLineWidth(0.6)
    c.rect(
        bollo_x, bollo_y,
        bollo_w, bollo_h,
        fill=0, stroke=1
    )

    c.setFont("Helvetica", 8)
    c.setFillColor(grigio)
    c.drawCentredString(
        bollo_x + bollo_w / 2,
        bollo_y + bollo_h / 2,
        "Marca da bollo"
    )

    testo(
        75 * mm,
        bollo_y + bollo_h / 2,
        "COPIA PER IL CONDUTTORE",
        7.2, True
    )

    # ==================================================
    # CONTRATTO DI LOCAZIONE
    # ==================================================
    sezione("CONTRATTO DI LOCAZIONE", 138 * mm)

    y = 130 * mm
    passo = 6 * mm

    campo(
        "Ufficio territoriale:", sx, y, dx,
        27 * mm, dato=ufficio_territoriale
    )
    y -= passo

    campo(
        "Data stipula:", sx, y, dx,
        22 * mm, dato=data_stipula
    )
    y -= passo

    campo(
        "Data registrazione:", sx, y, dx,
        29 * mm, dato=data_registrazione
    )
    y -= passo

    campo(
        "Codice identificativo contratto:",
        sx, y, dx, 47 * mm,
        dato=codice_contratto
    )
    y -= passo

    campo(
        "Durata contratto:", sx, y, dx,
        25 * mm, dato=durata_contratto
    )

    # ==================================================
    # UNITÀ IMMOBILIARE LOCATA
    # ==================================================
    sezione("UNITÀ IMMOBILIARE LOCATA", 97 * mm)

    y = 89 * mm

    campo(
        "Descrizione immobile:", sx, y, dx,
        31 * mm, dato=descrizione_immobile
    )
    y -= 6 * mm

    campo(
        "Locatore:", sx, y, 75 * mm,
        16 * mm, dato=locatore
    )
    campo(
        "C.F.:", 79 * mm, y, dx,
        10 * mm, dato=cf_locatore
    )
    y -= 6 * mm

    campo(
        "Conduttore:", sx, y, 75 * mm,
        22 * mm, dato=conduttore
    )
    campo(
        "C.F.:", 79 * mm, y, dx,
        10 * mm, dato=cf_conduttore
    )
    y -= 6 * mm

    campo(
        "Note:", sx, y, dx,
        11 * mm, dato=note
    )

    # ==================================================
    # DICHIARAZIONE E IMPORTO IN LETTERE
    # ==================================================
    testo(
        sx, 60 * mm,
        "Il Locatore dichiara di aver ricevuto dal Conduttore,",
        6.7
    )

    testo(
        sx, 56 * mm,
        "in riferimento al contratto sopra indicato, la somma di:",
        6.7
    )

    campo(
        importo_lettere, sx, 51 * mm, dx,
        0
    )

    # ==================================================
    # TABELLA: INTESTAZIONE + CINQUE CAUSALI
    # ==================================================
    tab_top = 46 * mm
    row_h = 4.5 * mm
    col_div = sx + larghezza * 0.73

    # Intestazione
    riga_tabella(tab_top, row_h, riempita=True)

    testo(
        sx + 2 * mm,
        tab_top - 3.1 * mm,
        "Causale", 7.2, True
    )

    testo(
        col_div + 2 * mm,
        tab_top - 3.1 * mm,
        "Importo", 7.2, True
    )

    # Cinque righe compilabili
    for i in range(5):
        y_top = tab_top - row_h * (i + 1)
        y_testo = y_top - 3.1 * mm

        riga_tabella(y_top, row_h)

        campo(
            "",
            sx + 1.5 * mm,
            y_testo,
            col_div - 1 * mm,
            0,
            dato=causali[i]
        )

        campo(
            "",
            col_div + 1.5 * mm,
            y_testo,
            dx - 1 * mm,
            0,
            dato=importi[i]
        )

    # Bordo esterno e divisione verticale
    tab_bottom = tab_top - row_h * 6

    c.setStrokeColor(grigio)
    c.rect(
        sx, tab_bottom,
        larghezza, row_h * 6,
        fill=0, stroke=1
    )

    linea(col_div, tab_top, col_div, tab_bottom)

    # ==================================================
    # FIRMA E RIEPILOGO IMPORTI
    # ==================================================
    base = tab_bottom

    testo(
        sx, base - 4 * mm,
        "Firma per quietanza", 7, True
    )

    linea(
        sx, base - 11 * mm,
        sx + 42 * mm, base - 11 * mm
    )

    x_lab = sx + 57 * mm
    x_val = dx - 17 * mm

    riepilogo = [
        ("Totale importi:", totale_importi, "€"),
        ("Perc. IVA su affitto:", percentuale_iva, "%"),
        ("Totale IVA:", totale_iva, "€"),
        ("TOTALE:", totale, "€"),
    ]

    for i, (etichetta, dato, simbolo) in enumerate(riepilogo):
        yy = base - (2.5 + i * 3.5) * mm
        bold = etichetta == "TOTALE:"

        testo(x_lab, yy, etichetta, 6.2, bold)
        testo(x_val - 4 * mm, yy, simbolo, 6.2, bold)

        if dato is not None and str(dato) != "":
            c.setFillColor(nero)
            c.setFont(
                "Helvetica-Bold" if bold else "Helvetica",
                6.2
            )
            c.drawRightString(
                x_val - 5 * mm,
                yy,
                str(dato)
            )

    # ==================================================
    # SALVATAGGIO DEL PDF
    # ==================================================
    c.showPage()
    # ==================================================
    # INTESTAZIONE
    # ==================================================
    testo(sx, 201 * mm, "Ricevuta d'Affitto", 14, True)
    
    campo(
        "Ricevuta n.",
        88 * mm, 201 * mm, dx,
        17 * mm, dato=numero_ricevuta
    )
    
    campo(
        "Data emissione:",
        88 * mm, 194 * mm, dx,
        24 * mm, dato=data_emissione
    )
    
    # ==================================================
    # MARCA DA BOLLO: 55 x 44 mm
    # ==================================================
    bollo_w = 55 * mm
    bollo_h = 44 * mm
    bollo_x = sx
    bollo_y = 145 * mm
    
    c.setStrokeColor(grigio)
    c.setLineWidth(0.6)
    c.rect(
        bollo_x, bollo_y,
        bollo_w, bollo_h,
        fill=0, stroke=1
    )
    
    c.setFont("Helvetica", 8)
    c.setFillColor(grigio)
    c.drawCentredString(
        bollo_x + bollo_w / 2,
        bollo_y + bollo_h / 2,
        "Marca da bollo"
    )
    
    testo(
        75 * mm,
        bollo_y + bollo_h / 2,
        "COPIA PER IL LOCATORE",
        7.2, True
    )
    
    # ==================================================
    # CONTRATTO DI LOCAZIONE
    # ==================================================
    sezione("CONTRATTO DI LOCAZIONE", 138 * mm)
    
    y = 130 * mm
    passo = 6 * mm
    
    campo(
        "Ufficio territoriale:", sx, y, dx,
        27 * mm, dato=ufficio_territoriale
    )
    y -= passo
    
    campo(
        "Data stipula:", sx, y, dx,
        22 * mm, dato=data_stipula
    )
    y -= passo
    
    campo(
        "Data registrazione:", sx, y, dx,
        29 * mm, dato=data_registrazione
    )
    y -= passo
    
    campo(
        "Codice identificativo contratto:",
        sx, y, dx, 47 * mm,
        dato=codice_contratto
    )
    y -= passo
    
    campo(
        "Durata contratto:", sx, y, dx,
        25 * mm, dato=durata_contratto
    )
    
    # ==================================================
    # UNITÀ IMMOBILIARE LOCATA
    # ==================================================
    sezione("UNITÀ IMMOBILIARE LOCATA", 97 * mm)
    
    y = 89 * mm
    
    campo(
        "Descrizione immobile:", sx, y, dx,
        31 * mm, dato=descrizione_immobile
    )
    y -= 6 * mm
    
    campo(
        "Locatore:", sx, y, 75 * mm,
        16 * mm, dato=locatore
    )
    campo(
        "C.F.:", 79 * mm, y, dx,
        10 * mm, dato=cf_locatore
    )
    y -= 6 * mm
    
    campo(
        "Conduttore:", sx, y, 75 * mm,
        22 * mm, dato=conduttore
    )
    campo(
        "C.F.:", 79 * mm, y, dx,
        10 * mm, dato=cf_conduttore
    )
    y -= 6 * mm
    
    campo(
        "Note:", sx, y, dx,
        11 * mm, dato=note
    )
    
    # ==================================================
    # DICHIARAZIONE E IMPORTO IN LETTERE
    # ==================================================
    testo(
        sx, 60 * mm,
        "Il Locatore dichiara di aver ricevuto dal Conduttore,",
        6.7
    )
    
    testo(
        sx, 56 * mm,
        "in riferimento al contratto sopra indicato, la somma di:",
        6.7
    )
    
    campo(
        importo_lettere, sx, 51 * mm, dx,
        0
    )
    
    # ==================================================
    # TABELLA: INTESTAZIONE + CINQUE CAUSALI
    # ==================================================
    tab_top = 46 * mm
    row_h = 4.5 * mm
    col_div = sx + larghezza * 0.73
    
    # Intestazione
    riga_tabella(tab_top, row_h, riempita=True)
    
    testo(
        sx + 2 * mm,
        tab_top - 3.1 * mm,
        "Causale", 7.2, True
    )
    
    testo(
        col_div + 2 * mm,
        tab_top - 3.1 * mm,
        "Importo", 7.2, True
    )
    
    # Cinque righe compilabili
    for i in range(5):
        y_top = tab_top - row_h * (i + 1)
        y_testo = y_top - 3.1 * mm
    
        riga_tabella(y_top, row_h)
    
        campo(
            "",
            sx + 1.5 * mm,
            y_testo,
            col_div - 1 * mm,
            0,
            dato=causali[i]
        )
    
        campo(
            "",
            col_div + 1.5 * mm,
            y_testo,
            dx - 1 * mm,
            0,
            dato=importi[i]
        )
    
    # Bordo esterno e divisione verticale
    tab_bottom = tab_top - row_h * 6
    
    c.setStrokeColor(grigio)
    c.rect(
        sx, tab_bottom,
        larghezza, row_h * 6,
        fill=0, stroke=1
    )
    
    linea(col_div, tab_top, col_div, tab_bottom)
    
    # ==================================================
    # FIRMA E RIEPILOGO IMPORTI
    # ==================================================
    base = tab_bottom
    
    testo(
        sx, base - 4 * mm,
        "Firma per quietanza", 7, True
    )
    
    linea(
        sx, base - 11 * mm,
        sx + 42 * mm, base - 11 * mm
    )
    
    x_lab = sx + 57 * mm
    x_val = dx - 17 * mm
    
    riepilogo = [
        ("Totale importi:", totale_importi, "€"),
        ("Perc. IVA su affitto:", percentuale_iva, "%"),
        ("Totale IVA:", totale_iva, "€"),
        ("TOTALE:", totale, "€"),
    ]
    
    for i, (etichetta, dato, simbolo) in enumerate(riepilogo):
        yy = base - (2.5 + i * 3.5) * mm
        bold = etichetta == "TOTALE:"
    
        testo(x_lab, yy, etichetta, 6.2, bold)
        testo(x_val - 4 * mm, yy, simbolo, 6.2, bold)
    
        if dato is not None and str(dato) != "":
            c.setFillColor(nero)
            c.setFont(
                "Helvetica-Bold" if bold else "Helvetica",
                6.2
            )
            c.drawRightString(
                x_val - 5 * mm,
                yy,
                str(dato)
            )
    
    c.save()
    print(f"PDF creato correttamente: {nome_file}")