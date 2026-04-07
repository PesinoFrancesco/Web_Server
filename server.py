import http.server
import threading
import socket
import time
import yaml
import os
import logging

connessione_attive = 0
lock_connessioni = threading.Lock()

try:
    with open('server_config.yaml', 'r', encoding='utf-8') as file:
        configurazione = yaml.safe_load(file)

        # Configuriamo il logging in base al file YAML
        logging.basicConfig(
            filename=configurazione['logging']['file'],
            level=configurazione['logging']['level']
        )
        try:
            host = configurazione['server']['host']
            port = configurazione['server']['port']
            max_conn = configurazione['server']['max_connections']
        except KeyError:
            host = 'localhost'
            port = 8080
            max_conn = 5
            logging.warning("Chiavi di configurazione mancanti. Utilizzo valori predefiniti.")
except FileNotFoundError:
    configurazione = {
        'server': {
            'host': 'localhost',
            'port': 8080,
            'max_connections': 5
        },
        'logging': {
            'level': 'INFO',
            'file': 'server.log' 
        },
        'static_dir': '.',
        'routes': [], 
        'mime_types': {}, 
        'error_pages': {404: '404.html', 500: '500.html'}
    }
    host = configurazione['server']['host']
    port = configurazione['server']['port']
    max_conn = configurazione['server']['max_connections']
    logging.warning("File di configurazione non trovato. Utilizzo valori predefiniti.")
#Creiamo il nostro "Ritardatore" personalizzato
class Ritardatore(http.server.SimpleHTTPRequestHandler):
    # do_GET è il momento esatto in cui il client chiede la pagina
    def do_GET(self):
        global configurazione
        try:
            if self.path == '/reload-config':
                try:
                    with open('server_config.yaml', 'r', encoding='utf-8') as file:
                        configurazione = yaml.safe_load(file)
                        logging.info("Configurazione ricaricata con successo!")
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"Configurazione ricaricata!")
                        return
                except Exception as e:
                    logging.error(f"Errore durante il reload: {e}")
                    file_errore_500 = os.path.join(configurazione['static_dir'], configurazione['error_pages'][500])
                    try:
                        # Apriamo il nostro file 500 personalizzato
                        with open(file_errore_500, 'rb') as f:
                            contenuto = f.read()
                
                            # Inviamo il codice 500 e il contenuto del file
                            self.send_response(500)
                            self.end_headers()
                            self.wfile.write(contenuto)

                    except FileNotFoundError:
                        # Se per caso il file 500.html manca dalla cartella, usiamo l'errore base di Python
                        self.send_error(500)
                        self.end_headers()

                    return
            for percorso in configurazione['routes']:
                if percorso['path']==self.path:
                    percorso_completo = os.path.join(configurazione['static_dir'], percorso['file'])
                    logging.info(f"Richiesta ricevuta per {percorso_completo}! Faccio finta di lavorare per 2 secondi...")
                    time.sleep(2)  # ritardo nella risposta per verificare threading in localhost
                    with open(percorso_completo, 'rb') as f:
                        contenuto = f.read()
                    self.send_response(200)  # Dice al browser che la richiesta è andata a buon fine
                    estensione_file = os.path.splitext(percorso['file'])[1] #separiamo l'estensione dal nome (es:ciao.html--> [ciao][html]) e poi selezioniamo l'elemento dell'estensione con [1]
                    self.send_header('Content-type', configurazione['mime_types'][estensione_file]) #mandiamo il content type in base all'estensione trovata e al file yaml di configurazione
                    self.end_headers()  #Questo comando inserisce quella riga divisoria obbligatoria
                    self.wfile.write(contenuto)  # Invia il contenuto del file al browser
                    return
            file_errore_404 = os.path.join(configurazione['static_dir'], configurazione['error_pages'][404])
            try:
                # Apriamo il nostro file 404 personalizzato
                with open(file_errore_404, 'rb') as f:
                    contenuto = f.read()
        
                    # Inviamo il codice 404 e il contenuto del file
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(contenuto)

            except FileNotFoundError:
                # Se per caso il file 404.html manca dalla cartella, usiamo l'errore base di Python
                self.send_error(404)
                self.end_headers()
        except Exception as e:
            
            logging.error(f"ERRORE: {e}")
            file_errore_500 = os.path.join(configurazione['static_dir'], configurazione['error_pages'][500])
            try:
                # Apriamo il nostro file 500 personalizzato
                with open(file_errore_500, 'rb') as f:
                    contenuto = f.read()
                        
                    # Inviamo il codice 500 e il contenuto del file
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(contenuto)

            except FileNotFoundError:
                # Se per caso il file 500.html manca dalla cartella, usiamo l'errore base di Python
                self.send_error(500)
                self.end_headers()

# Creiamo il nostro socket server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((host, port))
server_sock.listen(max_conn)

logging.info(f"Server in ascolto su {host}:{port} — max {max_conn} connessioni")

while True:
    conn, addr = server_sock.accept()

    with lock_connessioni:
        if connessione_attive >= max_conn:
            logging.warning(f"[{addr}] Server pieno! Rifiuto la connessione.")
            conn.sendall(b"HTTP/1.1 503 Service Unavailable\r\n\r\nServer occupato.")
            conn.close()
            continue

        connessione_attive += 1
        logging.info(f"[{addr}] Connessione accettata. Connessioni attive: {connessione_attive}/{max_conn}")

    def gestisci(conn, addr):
        global connessione_attive #dichiariamo la variabile globale per poterla modificare all'interno della funzione
        try:
            Ritardatore(conn, addr, None)
        finally:
            with lock_connessioni:
                connessione_attive -= 1
                logging.info(f"[{addr}] Chiuso. Attive: {connessione_attive}/{max_conn}")

    t = threading.Thread(target=gestisci, args=(conn, addr), daemon=True)
    t.start()