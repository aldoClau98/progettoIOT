# progettoIOT


il progetto che si intende realizzare è essenzialmente un salvadanaio smart, capace di aprirsi e chiudersi a
comando e con un semplice sistema di allarme antifurto che suona quando l’oggetto viene capovolto.
In particolare, il sistema sfrutterà la board ESP32 NodeMCU con microontrollore ESP32 WROOM 32,
l’apertura sarà pilotata da un servo motore SG90, il cui azionamento sarà avviato dall’utente tramite
applicazione Android o web dopo aver inserito un codice, mentre la chiusura verrà triggerata da un tasto
fisico presente sulla box.
Il meccanismo di allarme antifurto viene implementato con un giroscopio che comunicherà con il
microcontrollore sfruttando il protocollo I2C, facendo attivare un buzzer piezoelettrico al rilevamento di
capovolgimento del dispositivo.
Il microcontrollore sarà connesso ad internet via WiFi, con l’ausilio di MQTT verranno scambiati i dati per
l’apertura del device, mentre sfruttando Zerynth Device Manager verranno mantenuti i dati per generare una
history di timestamp di apertura e chiusura consultabili e cancellabili dall’applicazione, che avrà pertanto
come finalità visualizzazione e configurazione.
Il progetto sarà realizzato in team da Emilio Schiavo e  Aldo Claudini, la collaborazione avverrà in remoto e
avremo hardware duplicato.
