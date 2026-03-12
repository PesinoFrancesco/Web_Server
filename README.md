# Server Web TCP in Python

Questo progetto implementa un **server HTTP multi-thread personalizzato** scritto in Python. Utilizza i moduli nativi `socket` e `threading` per gestire connessioni concorrenti, appoggiandosi a un file di configurazione YAML per la definizione delle rotte, dei limiti di connessione e della gestione degli errori.

Il frontend allegato presenta un'interfaccia utente dinamica basata su **HTML5 Canvas**.

---

# Caratteristiche Principali

### Gestione Multi-thread

Elaborazione parallela delle richieste tramite il modulo `threading`.
Il codice include un **ritardo artificiale** implementato specificamente per dimostrare il funzionamento della concorrenza in locale.

### Configurazione Centralizzata

Parametri di rete (**host**, **porta**), limiti di connessione, routing delle pagine e mappatura dei tipi MIME sono gestiti esternamente tramite il file:

```
server_config.yaml
```

### Controllo della Concorrenza

Il server monitora attivamente il numero di connessioni e rifiuta le richieste eccedenti il limite massimo stabilito, restituendo un errore **HTTP 503**.

### Gestione Errori Personalizzata

Supporto nativo per l'instradamento verso pagine di errore personalizzate:

* **404 Not Found**
* **500 Internal Server Error**

definite nel file di configurazione.

### Interfaccia Grafica

I file statici forniti implementano:

* design coerente
* animazioni CSS
* rendering grafico tramite **Canvas**

---

# Prerequisiti

Per eseguire correttamente il server è necessario disporre di:

* **Python 3.x**
* modulo **PyYAML**

---

# Struttura del Progetto

Assicurarsi che i file siano organizzati nella seguente gerarchia:

```
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
```

---

# Installazione e Avvio

## 1. Scaricare il progetto

Clonare o scaricare il repository e assicurarsi che tutti i file si trovino nella stessa directory.

---

## 2. Installare le dipendenze

Installare la libreria YAML necessaria per leggere la configurazione:

```bash
pip install pyyaml
```

---

## 3. Avviare il server

Eseguire lo script principale:

```bash
python server.py
```

---

## 4. Accedere al servizio

Aprire il browser e visitare:

```
http://localhost:8080
```

oppure l'indirizzo **IP e porta** definiti nel file `server_config.yaml`.

---

# Configurazione

Il file `server_config.yaml` permette di modificare il comportamento del server **senza alterare il codice sorgente**.

### Parametri principali

**server.host**
Definisce l'indirizzo di bind del server.

**server.port**
Definisce la porta di ascolto.

**server.max_connections**
Numero massimo di client gestibili simultaneamente.

**static_dir**
Directory radice contenente i file frontend.
Valore predefinito:

```
./public
```

**routes**
Associa i percorsi URL ai file fisici.

Esempio:

```
/about -> about.html
```

**mime_types**
Mappa le estensioni dei file ai rispettivi header HTTP `Content-Type`.

**error_pages**
Definisce i percorsi dei file HTML di errore personalizzati.

---

# Autore

Progetto sviluppato e curato da **Francesco Pesaresi**.

