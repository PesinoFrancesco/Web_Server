# Server Web TCP in Python

Questo progetto implementa un server HTTP multi-thread personalizzato scritto in Python. Utilizza i moduli nativi `socket` e `threading` per gestire connessioni concorrenti, appoggiandosi a un file di configurazione YAML per la definizione delle rotte, dei limiti di connessione e della gestione degli errori. Il frontend allegato presenta un'interfaccia utente dinamica basata su HTML5 Canvas.

## Caratteristiche Principali

* **Gestione Multi-thread**: Elaborazione parallela delle richieste tramite il modulo `threading`. Il codice include un ritardo artificiale implementato specificamente per dimostrare il funzionamento della concorrenza in locale.
* **Configurazione Centralizzata**: Parametri di rete (host, porta), limiti di connessione, routing delle pagine e mappatura dei tipi MIME sono gestiti esternamente tramite il file `server_config.yaml`.
* **Controllo della Concorrenza**: Il server monitora attivamente il numero di connessioni e rifiuta le richieste eccedenti il limite massimo stabilito, restituendo un errore HTTP 503.
* **Gestione Errori Personalizzata**: Supporto nativo per l'instradamento verso pagine di errore personalizzate (404 Not Found e 500 Internal Server Error) definite nel file di configurazione.
* **Interfaccia Grafica**: I file statici forniti implementano un design coerente con animazioni CSS e rendering grafico tramite Canvas.

## Prerequisiti

Per eseguire correttamente il server, è necessario disporre di:

* Python 3.x
* Modulo `PyYAML`

## Struttura del Progetto

Assicurarsi che i file siano organizzati nella seguente gerarchia, in conformità con il file di configurazione:

    .
    ├── server.py
    ├── server_config.yaml
    └── public/
        ├── index.html
        ├── about.html
        ├── contatti.html
        └── errors/
            ├── 404.html
            └── 500.html

Nota: i file di errore (404.html e 500.html) devono risiedere all'interno della sottocartella `errors` dentro `public`.

## Installazione e Avvio

1. **Clonare o scaricare il repository**: Assicurarsi che tutti i file si trovino nella stessa directory di lavoro.
2. **Installare le dipendenze**: Installare la libreria YAML necessaria per leggere la configurazione eseguendo il seguente comando nel terminale:
   ```bash
   pip install pyyaml
Avviare il server: Eseguire lo script principale:

Bash
python server.py
Accedere al servizio: Aprire un browser web e navigare all'indirizzo http://localhost:8080 (o all'indirizzo IP e porta specificati nel file di configurazione).

Configurazione
Il file server_config.yaml permette di modificare il comportamento del server senza alterare il codice sorgente:

server.host e server.port: Definiscono l'indirizzo di bind e la porta di ascolto.

server.max_connections: Imposta il numero massimo di client gestibili simultaneamente.

static_dir: Indica la directory radice contenente i file frontend (predefinito: ./public).

routes: Associa i percorsi URL (es. /about) ai rispettivi file fisici (es. about.html).

mime_types: Mappa le estensioni dei file alle rispettive intestazioni HTTP Content-type.

error_pages: Definisce i percorsi per i file HTML di errore personalizzati.

Autore
Progetto sviluppato e curato da Francesco Pesaresi.


---
Posso aiutarti a redigere dei commenti aggiuntivi per il file `server.py` o c'è un'altra
