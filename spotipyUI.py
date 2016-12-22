#!/usr/bin/python
import sys
import spotipy
import spotipy.util as util
from PyQt4 import QtCore, QtGui, uic

username = 'alienbob93'

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi('spotipy_form.ui', self)

        # Initilaize SpotiPy (get user tokens)
        self.sp = InitilaizeSpotiPy()
        if self.sp == None:
            sys.exit()

        # set pixmaps
        PlayIcon = QtGui.QPixmap("play_icon_orange.png")
        NextIcon = QtGui.QPixmap("next_grey.png")
        PrevIcon = QtGui.QPixmap("previous_black.png")

        # set button icons
        self.Play_button.setIcon(QtGui.QIcon(PlayIcon))
        self.Next_button.setIcon(QtGui.QIcon(NextIcon))
        self.Prev_button.setIcon(QtGui.QIcon(PrevIcon))

        # connect signals to slots
        self.Search.returnPressed.connect(self.returnpressed)
        self.GetDefaultPlaylists.clicked.connect(self.getPlaylists)

    def returnpressed(self, text):
        results = self.sp.search(text, limit = 20)
        populateSearchResults(self, results)

    def getPlaylists(self):
        playlists = self.sp.user_playlists(username)
        for playlist in playlists['items']:
            item = QtGui.QListWidgetItem(playlist['name'])
            self.resultsList.addItem(item)
            #print playlist['name']

    def changePage(self, i):
        # index 1 is search results, 2 is the player window
        self.resultsWindow.setCurrentIndex(i)

    def populateSearchResults(self, searchResults):
        for results in enumerate(searchResults['tracks']['items']):
            item = QtGui.QListWidgetItem(results['name'])
            self.resultsList.addItem(item)

def InitilaizeSpotiPy():
    token = util.prompt_for_user_token(username)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        sp = None
    return sp

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyDialog()
    #p = myapp.palette()
    #p.setColor(myapp.backgroundRole(), QtCore.Qt.black)
    #myapp.setPalette(p)
    myapp.show()
    sys.exit(app.exec_())
