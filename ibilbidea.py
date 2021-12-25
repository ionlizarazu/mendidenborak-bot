class Ibilbidea:
    def __init__(self):
        self.bidea = ""
        self.positiboa = 0
        self.negatiboa = 0
        self.luzeera = 0

    def set_bidea(self, bidea):
        self.bidea = bidea

    def set_luzeera(self, luzeera):
        self.luzeera = luzeera

    def set_positiboa(self, positiboa):
        try:
            self.positiboa = int(positiboa)
            return 0
        except ValueError:
            self.positiboa = 0
            return -1

    def set_negatiboa(self, negatiboa):
        try:
            self.negatiboa = int(negatiboa)
            return 0, 'OK'
        except ValueError:
            self.negatiboa = 0
            return -1
