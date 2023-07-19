import time

input_file = input('Welke bestand met records wil je in kaart brengen?') 
output_file = open(input('Naar welke file wil je rapporteren?'), 'w') 
start = time.time()
harvest = ''
with open(input_file) as fi:
    for line in fi:
        harvest += line[:-2]
stop = time.time()
delta = stop - start
print(delta)
print(harvest)
output_file.write(harvest)
output_file.close()
