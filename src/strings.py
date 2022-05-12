import _constants
from string import Template

# how the program identifies itself
branding = "Edico Updater"
version = "1.0.2"

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

# shown when Edico executable is not found
edicoNotFound = "Impossibile trovare l'eseguibile di Edico."

# shown in the about dialog
aboutTitle = "Informazioni su Edico Updater"
aboutText = (
    f"{branding}\n\n"
    f"Versione {version} ({_constants.buildDate})\n"
    f"Copyright © 2022 {_constants.author}. Tutti i diritti riservati.\n\n"
    "Edico è di proprietà di ONCE CTI.\n"
    "Questo software non è affiliato in alcun modo a ONCE."
)

# shown in the main window
description = (
    f"Ti diamo il benvenuto su {branding}.\n"
    "Questo programma permette di verificare la disponibilità di nuove versioni di Edico, scaricarle e installarle senza dover consultare il sito di Irifor.\n"
    "Inoltre, permette di installare Edico se non è presente nel sistema.\n"
)

# shown in the main window
updateButton = "Installa o aggiorna"

notInstalledTitle = "Edico non è installato"
notInstalled = "Edico non è installato.\n\nDesideri scaricarlo?"
versionUpToDateTitle = "Versione aggiornata"
versionUpToDate = Template(
    "Possiedi l'ultima versione di Edico.\n\n"
    "Versione disponibile: $version1\n"
    "Versione installata: $version2\n"
)
newVersionAvailableTitle = "Nuova versione disponibile"
newVersionAvailable = Template(
    "Una nuova versione di Edico è disponibile.\n\n"
    "Versione disponibile: $version1\n"
    "Versione installata: $version2\n"
    "Desideri scaricarla?"
)
progressDialogTitle = "Download in corso"
progressDialogText = "Scaricamento in corso..."
askInstall = "Download completato\n\n" "Desideri eseguire l'installazione di Edico?"
downloadComplete = "Download completato"
