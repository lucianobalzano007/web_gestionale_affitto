# 🏠 Web Gestionale Affitto

Applicazione web per la gestione degli affitti, sviluppata con l'obiettivo di semplificare e centralizzare le principali attività legate alla gestione degli immobili e delle locazioni.

## 📋 Indice
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [📌 Descrizione](#-descrizione)
- [✨ Funzionalità](#-funzionalit%C3%A0)
- [🚀 Installazione](#-installazione)
- [🛠️ Tecnologie](#-tecnologie)
- [📂 Struttura del progetto](#-struttura-del-progetto)
- [💡 Obiettivo del progetto](#-obiettivo-del-progetto)
- [🔧 Sviluppi futuri](#-sviluppi-futuri)
- [🤝 Contributi](#-contributi)
- [👨‍💻 Autore](#-autore)
- [📄 Licenza](#-licenza)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 📌 Descrizione

**Web Gestionale Affitto** è un progetto pensato per offrire un'interfaccia semplice e organizzata attraverso cui gestire le informazioni relative agli affitti.

Il progetto è disponibile pubblicamente su GitHub.

## ✨ Funzionalità

Il gestionale è pensato per centralizzare le operazioni relative alla gestione degli affitti.

Tra le funzionalità del progetto possono rientrare:

- 🏠 Gestione degli immobili
- 👤 Gestione degli affittuari
- 💰 Gestione dei pagamenti
- 📅 Monitoraggio delle scadenze
- 📊 Visualizzazione delle informazioni tramite dashboard
- 🔎 Consultazione e ricerca dei dati

> Le funzionalità disponibili dipendono dalla versione corrente dell'applicazione.

## 🚀 Installazione

Installa Docker seguendo la seguente [Documentazione](https://docs.docker.com/engine/install/)

Esegui il seguente file compose

```bash
services:
  web:
      image: lucianobalzano/web_gestionale_affitto
      environment:
          MONGO_INITDB_ROOT_USERNAME: example
          MONGO_INITDB_ROOT_PASSWORD: example
          MONGO_HOST_NAME: mongo_web_gestionale_affitto
          MONGO_PORT: 27017 
          SECRET_KEY_SESSION: b'YOUR_SECRET_KEY'
      ports:
        - "5000:5000"
      depends_on:
        - mongo
  
  mongo:
    image: mongo
    hostname: mongo_web_gestionale_affitto
    environment:
      MONGO_INITDB_ROOT_USERNAME: example
      MONGO_INITDB_ROOT_PASSWORD: example
    ports:
      - "27017:27017"
    volumes:
      - ./mongo_data:/data/db
```

Per la generazione della secret key fare riferimento alla seguente [documentazione](https://flask.palletsprojects.com/en/stable/quickstart/#sessions)

## 🛠️ Tecnologie

Le tecnologie utilizzate possono essere consultate direttamente all'interno della repository e nei relativi file di configurazione.

## 📂 Struttura del progetto

La repository contiene il codice sorgente e le risorse necessarie per il funzionamento dell'applicazione.

La struttura può essere esplorata direttamente da GitHub oppure dopo aver clonato il progetto localmente.

## 💡 Obiettivo del progetto

L'obiettivo di **Web Gestionale Affitto** è realizzare uno strumento intuitivo per organizzare le informazioni relative alla gestione degli affitti, riducendo la necessità di utilizzare strumenti separati per immobili, pagamenti e scadenze.

## 🔧 Sviluppi futuri

Possibili miglioramenti:

- Dashboard con statistiche avanzate
- Gestione automatica delle scadenze
- Notifiche per pagamenti e contratti
- Esportazione dei dati
- Generazione di report
- Miglioramento dell'esperienza mobile
- Sistema di autenticazione e gestione utenti
- Backup dei dati

## 🤝 Contributi

Contributi, suggerimenti e segnalazioni sono benvenuti.

Per proporre una modifica:

1. Esegui il fork della repository
2. Crea un nuovo branch
3. Effettua le modifiche
4. Esegui il commit
5. Apri una Pull Request

## 👨‍💻 Autore

**Luciano Balzano**

GitHub: https://github.com/lucianobalzano007

## 📄 Licenza

Consulta la repository per verificare la licenza associata al progetto.

---

⭐ Se il progetto ti è stato utile, lascia una **Star** alla repository!
