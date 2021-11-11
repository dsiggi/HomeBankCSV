from .HomeBankCSV import HomeBankCSV

class n26(HomeBankCSV):
    CONV={
        "SEPERATOR": ',',
        "DATUM": 0,
        "EMPFÄNGER": 1,
        "TYP": 3,
        "VWZ": 4,
        "KATEGORIE": None,
        "BETRAG": 5,
        "BETRAG_SEPERATOR": False,
        "BETRAG_UMRECHNEN": False,
        "ERSTE_ZEILE": 2,
        "CONVERT": None,
        "ENCODING": "utf-8"
    }

    def get_typ(self, val):
        """
        Wandeln des Typs der Transaktion
        """
        if val[self.CONV["TYP"]] == "MasterCard Zahlung":
            return "1"
        elif val[self.CONV["TYP"]] == "Lastschrift":
            return "11"
        elif val[self.CONV["TYP"]] == "Überweisung":
            if "cbs.overdraft-fee-charge" in val[self.CONV["VWZ"]]:
                return "10"
            else:
                return "4"
        elif val[self.CONV["TYP"]] == "Abhebung":
            return "3"
        elif val[self.CONV["TYP"]] == "Gutschrift":
            return "9"
        elif val[self.CONV["TYP"]] == "Cash26 Auszahlung":
            return "3"
        else:
            return "0"

