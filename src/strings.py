import _constants
from string import Template

# how the program identifies itself
branding = "EDICO Updater"
version = "1.0.1"

# shown in the (temporary) version label
versionText = Template("Versione: $version")

# error related strings
errorTitle = "Errore"
error = Template("Qualcosa è andato storto.\n\n$error")
cannotReadVersionFromExe = Template(
    "Impossibile leggere la versione dall'eseguibile.\n\n$error"
)
serverResponseError = Template("Il server ha risposto in maniera inattesa: $statusCode")
serverUnreachable = (
    "Impossibile connettersi al server.\n"
    "Forse il server è offline o la connessione è assente."
)
versionError = "Impossibile ottenere la versione."

# shown when EDICO executable is not found
edicoNotFound = "Impossibile trovare l'eseguibile di EDICO."

# shown in the about dialog
aboutTitle = "Informazioni su EDICO Updater"
aboutText = (
    f"{branding}\n\n"
    f"Versione {version} ({_constants.buildDate})\n"
    f"Copyright © 2022 {_constants.author}. Tutti i diritti riservati.\n\n"
    "EDICO è di proprietà di ONCE CTI.\n"
    "Questo software non è affiliato in alcun modo a ONCE."
)

# shown in the main window
description = (
    f"Ti diamo il benvenuto su {branding}.\n"
    "Questo programma permette di verificare la disponibilità di nuove versioni di EDICO, scaricarle e installarle senza dover consultare il sito di Irifor.\n"
    "Inoltre, permette di installare EDICO se non è presente nel sistema.\n"
)

# shown in the main window
updateButton = "Installa o aggiorna"

notInstalledTitle = "EDICO non è installato"
notInstalled = "EDICO non è installato.\n\nDesideri scaricarlo?"
versionUpToDateTitle = "Versione aggiornata"
versionUpToDate = Template(
    "Possiedi l'ultima versione di EDICO.\n\n"
    "Versione disponibile: $version1\n"
    "Versione installata: $version2\n"
)
newVersionAvailableTitle = "Nuova versione disponibile"
newVersionAvailable = Template(
    "Una nuova versione di EDICO è disponibile.\n\n"
    "Versione disponibile: $version1\n"
    "Versione installata: $version2\n"
    "Desideri scaricarla?"
)
progressDialogTitle = "Download in corso"
progressDialogText = "Scaricamento in corso..."
askInstall = "Download completato\n\n" "Desideri eseguire l'installazione di EDICO?"
downloadComplete = "Download completato"
