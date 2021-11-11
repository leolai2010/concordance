import pandas as pd
import datetime

class Concordance:
    def __init__(self, files):
        self.files = files
        self.outputFileName = datetime.date.today().strftime('%Y%m%d') + '_' + datetime.datetime.now().strftime('%H%M%S')
    
    def format(self):
        kits_dic = {}
        while self.files:
            for fileSelect in self.files:
                currentFile = pd.read_csv(fileSelect)