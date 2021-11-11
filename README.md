# HomeBankCSV

Mit diesem Python modul lassen sich Transaktionübersichten verschiedener Banken in ein passendes Format für die Software [HomeBank](http://homebank.free.fr/en/index.php) wandeln.

Folgende Banken werden bis jetzt unterstützt:
- Bank of Scotland
- Barclays
- Landes Bank Berlin (Amazon Kreditkarte)
- n26
- OLB

Die Klasse HomeBankCSV bildet die Grundlagen um weitere Banken hinzuzufügen.


## Beispiel
```python
from HomeBankCSV import n26, lbb, barclays, olb, bankofscotland

# Initalisieren der Klassen
n26 = n26.n26("Download/n26.csv")
lbb = lbb.lbb("Download/lbb.csv")
barclays = barclays.barclays("Download/barclays.xlsx")
olb = olb.olb("Download/olb.csv")
bankofscotland = bankofscotland.bankofscotland("Download/bos.xls")

# Speichern der Transaktionen im passenden Format für HomeBank
n26.save("n26.csv")
lbb.save("lbb.csv")
barclays.save("barclays.csv")
olb.save("olb.csv")
bankofscotland.save("bos.csv")
```



