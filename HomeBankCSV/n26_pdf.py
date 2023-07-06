from .HomeBankCSV import HomeBankCSV
from pypdf import PdfReader

class n26(HomeBankCSV):
    CONV={
        "SEPERATOR": ';',
        "DATUM": 0,
        "EMPFÄNGER": 1,
        "TYP": None,
        "VWZ": 2,
        "KATEGORIE": None,
        "BETRAG": 3,
        "BETRAG_SEPERATOR": True,
        "BETRAG_UMRECHNEN": False,
        "ERSTE_ZEILE": 1,
        "CONVERT": True,
        "ENCODING": "utf-8"
    }

    def _get_Betrag(self, data):
        find_char = '+'
        if '-' in data:
            find_char = '-'

        return data[data.find(find_char):data.find('€') + 1].replace(".", "")
    
    def _get_Datum(self, data):
        if '-' in data:
            last_char = data.find('-') - 1
        else:
            last_char = data.find('+') - 1

        return data[last_char - 10:last_char]

    def _get_VWZ(self, data):
        return data

    def _get_Empfänger(self, data):
        return data

    def Convert2CSV(self):
        """
        Die Eingabedatei wird nach CSV gewandelt.
        In diesem Fall von PDF zu CSV.
        """
        ## PDF Datei öffnen
        reader = PdfReader(self.file)

        csv =""
        act_page=0

        while act_page < len(reader.pages):
            page = reader.pages[act_page]
            data = page.extract_text()

            # Wenn die Seite den Text nicht enthält, ist sie nicht wichtig für uns
            if not 'Space Kontoauszug' in data:
                act_page += 1
                continue

            # Lese die Daten in ein Array ein
            lines = []
            for line in data.splitlines():
                lines.append(line)

            # Das Array nun einmal "drehen" damit wir rückwärts abarbeiten können
            # Dannach nur die interessanten Zeilen abarbeiten
            lines.reverse()
            last_line=len(lines) - 6
            skip_lines = 0
            for index, line in list(enumerate(lines[3:last_line], start=3)):
                # Die Schleife solange überspringen bis wir beim nächsten Datensatz sind
                if skip_lines > 0:
                    skip_lines -= 1
                    continue

                # Die erste Zeile muss den Betrag und das Datum Enthalten, sonst stimmt etwas nicht
                if not '€' in line:
                    raise('PDF scheint nicht gültig zu sein!')

                # Finde nächste Zeile mit Betrag
                next_data = index
                found = False
                for nl in lines[index + 1:last_line]:
                    if '€' in nl:
                        found = True
                        break

                    next_data += 1

                if found:
                    skip_lines = next_data - index
                else:
                    next_data = last_line
                    skip_lines = last_line - index

                # Extrahiere Betrag
                betrag = self._get_Betrag(line)

                # Extrahiere Datum
                datum = self._get_Datum(line)

                # Extrahiere VWZ
                # Wenn die nächste Zeile ein "•" enthält, gibt es keinen VWZ
                if "•" in lines[index + 1]:
                    vwz = ""
                else:
                    vwz = self._get_VWZ(lines[index + 1])

                # Extrahiere Empfänger
                empf = self._get_Empfänger(lines[next_data])

                # CSV Zeile zusammenbauen
                zeile = '"' + str(datum) + '"' + self.CONV["SEPERATOR"]
                zeile += '"' + str(empf) + '"' + self.CONV["SEPERATOR"]
                zeile += '"' + str(vwz) + '"' + self.CONV["SEPERATOR"]
                zeile += '"' + str(betrag) + '"' + self.CONV["SEPERATOR"]

                csv += zeile + '\n'

            act_page += 1

        return csv
    
    def get_typ(self, val):
        return 1
