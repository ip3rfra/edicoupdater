from os import environ, path, startfile
import requests as r
import strings
import sys
from threading import Thread
from win32com.client import Dispatch
import wx

resourcePath = sys._MEIPASS

# initialize wx
app = wx.App()
frame = wx.Frame(
    None,
    title=strings.branding,
    size=(500, 300),
    style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX,
)
frame.SetIcon(wx.Icon(f"{resourcePath}/icon.ico", wx.BITMAP_TYPE_ICO))
frame.Center()
panel = wx.Panel(frame, wx.ID_ANY)
panel.SetSize(frame.GetSize())

# error dialog
def showError(error):
    wx.MessageBox(
        strings.error.safe_substitute(error=error),
        strings.errorTitle,
        wx.OK | wx.ICON_ERROR,
    )


# get the json from GitHub
def getJSON():
    JSONURL = "https://raw.githubusercontent.com/edicoIta/remoteConfig/main/edico.json"
    try:
        response = r.get(JSONURL, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            showError(
                strings.serverResponseError.safe_substitute(
                    statusCode=response.status_code
                )
            )
            return None
    except r.exceptions.RequestException:
        showError(strings.serverUnreachable)
        return None


# parse the json file and get the download url
def getURLFromJSON():
    json = getJSON()
    if json is not None:
        return json["url"]


# download the file from json url
def downloadFile():
    url = getURLFromJSON()
    path = f"EdicoSetup-v{getVersionFromJSON()}.exe"
    try:
        response = r.get(url, stream=True, timeout=5)
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True, path
    except r.exceptions.RequestException:
        showError(strings.serverUnreachable)
        return False, None


# get the version from EDICO executable
def getVersionFromExecutable():
    try:
        userProfileDir = environ["USERPROFILE"]
        edicoPath = (
            f"{userProfileDir}\\AppData\\Local\\Programs\\edico\\EdicoLauncher.exe"
        )
        if not path.exists(edicoPath):
            return None
        parser = Dispatch("Scripting.FileSystemObject")
        version = parser.GetFileVersion(edicoPath)
        return version
    except Exception as e:
        showError(strings.cannotReadVersionFromExecutable.safe_substitute(error=e))


# parse the json and get the latest version number
def getVersionFromJSON():
    json = getJSON()
    if json is not None:
        return json["version"]


# compare the versions
def compareVersions():
    version2 = getVersionFromExecutable()
    if version2 == None:
        return 2
    version1 = getVersionFromJSON()
    if version1 > version2:
        return 1
    elif version1 == version2:
        return 0
    else:
        return -1


# check if the internet connection is available before starting the download
def checkInternet():
    try:
        r.get("https://www.google.com", timeout=5)
        return True
    except r.exceptions.RequestException:
        showError(strings.serverUnreachable)
        return False


# download and (under user consent) install the latest version
def downloadAndInstall():
    # download the file
    success, path = downloadFile()
    if success:
        # ask if the user wants to install the new version
        if (
            wx.MessageBox(
                strings.askInstall,
                strings.downloadComplete,
                wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION,
            )
            == wx.YES
        ):
            # run the file
            try:
                startfile(path)
                sys.exit()  # the updater is not necessary anymore
            except Exception as e:
                showError(e)
    else:
        sys.exit()  # same as above


# process the version
def processVersion(event):
    if compareVersions() == 0:
        wx.MessageBox(
            strings.versionUpToDate.safe_substitute(
                version1=getVersionFromJSON(), version2=getVersionFromExecutable()
            ),
            strings.versionUpToDateTitle,
            wx.OK | wx.ICON_INFORMATION,
        )
        sys.exit()
    elif compareVersions() == 1:
        # ask the user if he wants to update
        if (
            wx.MessageBox(
                strings.newVersionAvailable.safe_substitute(
                    version1=getVersionFromJSON(), version2=getVersionFromExecutable()
                ),
                strings.newVersionAvailableTitle,
                wx.YES_NO | wx.CANCEL | wx.ICON_WARNING,
            )
            == wx.YES
        ):
            t = Thread(target=downloadAndInstall, daemon=True)
            t.start()
            progress = spawnProgressDialog()
            while t.is_alive():
                progress.Pulse()
                progress.Show()
            progress.Destroy()
    elif compareVersions() == 2:
        # ask the user if he wants to download the latest version
        if (
            wx.MessageBox(
                strings.notInstalled,
                strings.notInstalledTitle,
                wx.YES_NO | wx.CANCEL | wx.ICON_WARNING,
            )
            == wx.YES
        ):
            if checkInternet():
                t = Thread(target=downloadAndInstall, daemon=True)
                t.start()
                progress = spawnProgressDialog()
                while t.is_alive():
                    progress.Pulse()
                    progress.Show()
                progress.Destroy()
    elif compareVersions() == -1:
        showError(strings.versionError)


# create the progress dialog, used while downloading
def spawnProgressDialog():
    return wx.ProgressDialog(
        strings.progressDialogTitle,
        strings.progressDialogText,
        maximum=100,
        parent=frame,
        style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME,
    )


# about dialog
def aboutDialog(event):
    wx.MessageBox(
        strings.aboutText, strings.aboutTitle, wx.OK | wx.ICON_NONE,
    )


# show the main window
def show():
    # title label
    title = wx.StaticText(panel, wx.ID_ANY, label=strings.branding)
    title.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    title.SetPosition((frame.GetSize()[0] / 2 - title.GetSize()[0] / 2, 10))
    # create a textbox to show the version
    versionText = wx.StaticText(panel, wx.ID_ANY, label=strings.version)
    versionText.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
    versionText.SetBackgroundColour("#ff0000")
    versionText.SetForegroundColour("#ffffff")
    versionText.SetPosition(
        (frame.GetSize()[0] / 2 - versionText.GetSize()[0] / 2 + 80, 40)
    )
    desc = wx.StaticText(
        panel, wx.ID_ANY, style=wx.ALIGN_CENTER, label=strings.description,
    )
    desc.Wrap(300)
    desc.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
    desc.SetPosition((frame.GetSize()[0] / 2 - desc.GetSize()[0] / 2, 70))
    # get version button
    getVersionButton = wx.Button(panel, wx.ID_ANY, label=strings.updateButton)
    getVersionButton.SetPosition(
        (
            frame.GetSize()[0] / 2 - getVersionButton.GetSize()[0] / 2,
            frame.GetSize()[1] - 90,
        )
    )
    getVersionButton.Bind(wx.EVT_BUTTON, processVersion)
    # menubar and menu
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()
    aboutMenu = wx.Menu()
    fileMenu.Append(wx.ID_EXIT, "&Esci")
    aboutMenu.Append(wx.ID_ABOUT, "&Informazioni su...")
    menubar.Append(fileMenu, "&File")
    menubar.Append(aboutMenu, "&Aiuto")
    frame.SetMenuBar(menubar)
    # bind the events
    frame.Bind(wx.EVT_MENU, aboutDialog, id=wx.ID_ABOUT)
    frame.Bind(wx.EVT_MENU, sys.exit, id=wx.ID_EXIT)
    # show the frame
    title.Show()
    versionText.Show(False)
    desc.Show()
    getVersionButton.Show()
    panel.Show()
    frame.Show()
    # start the event loop
    app.MainLoop()


if __name__ == "__main__":
    show()
