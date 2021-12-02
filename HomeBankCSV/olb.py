from .HomeBankCSV import HomeBankCSV

class olb(HomeBankCSV):
    CONV={
        "SEPERATOR": ';',
        "DATUM": 1,
        "EMPFÄNGER": 3,
        "TYP": None,
        "VWZ": 6,
        "KATEGORIE": None,
        "BETRAG": 7,
        "BETRAG_SEPERATOR": True,
        "BETRAG_UMRECHNEN": False,
        "ERSTE_ZEILE": 2,
        "CONVERT": None,
        "ENCODING": "latin1"
    }

    def get_typ(self, val):
        """
        Gibt nun als Typ immer "Lastschrift" zurück.
        """
        return "11"
