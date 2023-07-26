import time

#
# De module cy is bedoeld om een door tags semantisch opgemaakte tekst
# die in  lijnen is gekapt  op vaste lengte  en waar er  eventueel nog
# bijkomende  karakters werden  gebruik om  elke regel  visueel af  te
# bakenen (een regeleinde zie je  niet visueel) weder samen te stellen
# als één lange lijn zonder regeleinden.
#
# In smime  bestanden zie je  vaak zo'n typische tekst  opmaak waarbij
# bijlagen  dan afgekapt  worden op  bijv.  80 karakters  met een  '='
# gevolgd door een '\n'.
#

input_file = input('Welke bestand met records wil je in kaart brengen?') 
output_file = open(input('Naar welke file wil je rapporteren?'), 'w')
cut_off = int(input('Hoeveel karakters wil je afkappen achteraan de lijnen?'))
start = time.time()
harvest = ''
with open(input_file) as fi:
    for line in fi:
        harvest += line[:-cut_off]
stop = time.time()
delta = stop - start
print(delta)
print(harvest)
output_file.write(harvest)
output_file.close()
