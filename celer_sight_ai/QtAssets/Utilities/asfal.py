import pyAesCrypt
from celer_sight_ai.QtAssets.Utilities.WarningWindow import WarningUi


class saveModelHandler:
    def __init__(self, fileToSave=None, fileName=None, folderToSave=None, MODE_USED=0):
        self.folderToSave = folderToSave
        self.fileToSave = fileToSave
        self.fileName = fileName
        self.pickled = 0
        self.json = 1
        self.MODE = MODE_USED
        if fileToSave == None or fileToSave == None:
            WarningUi(errorCode="Error during saving.")
        if self.MODE == self.pickled:
            pass
        elif self.MODE == self.json:
            pass
        else:
            WarningUi(errorCode="Error during saving, wrong mode.")
        self.intPass = "this is just a conviniece section for easier file loading"

    def savePickled(self):
        import tempfile
        import pickle
        import pyAesCrypt
        import os

        tempdir = tempfile.mkdtemp()
        saved_umask = os.umask(0o077)
        pickle.dump(self.fileToSave, open(tempdir + self.fileName, "wb"))
        self.intPass
        # pipeline to encrypt we get a password, that is generated from a code that is
        # encryption/decryption buffer size - 64K
        bufferSize = 64 * 1024
        # encrypt
        pyAesCrypt.encryptFile(
            tempdir + self.fileName,
            os.path.join(self.folderToSave, self.fileName),
            self.intPass,
            bufferSize,
        )

    def renameOLD(self, oldFilename, NewFilename):
        import os

        try:
            os.rename(oldFilename, NewFilename)
        except:
            WarningUi(errorCode="Error renaming model.")

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def getPassword(self):
        pass

    def createPassword(self):
        pass


if __name__ == "__main__":
    pass
