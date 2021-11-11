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
