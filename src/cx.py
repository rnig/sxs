import sys
sys.path.insert(0, 'd:\dm')
print(sys.path)
import grep
import hy_fi
import time

input_file = input('Welke bestand met records wil je in kaart brengen?') 
output_file = open(input('Naar welke file wil je rapporteren?'), 'a') 
start = time.time()
harvest = {}
with open(input_file) as fi:
    for line in fi:
        a_text_pattern, a_type = line.split('|')
        print(a_text_pattern, a_type)
        ifs = hy_fi.interactive_find(i_pattern='*.xml'
                                     , i_path='G:\\PL\\fusie\\dat\\in\\CAP2\\'
                                     , i_deep_dive=True
                                     , i_do_fils=True
                                     , i_do_dirs=False
                                     , i_do_fuzz=False
                                     , i_do_debug=False)
        if a_text_pattern not in harvest.keys():
            harvest[a_text_pattern] = grep.grep(ifs, a_text_pattern)
        else:
            print("Found duplicate key {a_text_pattern} in {input_file}.")
            sys.exit()
stop = time.time()
delta = stop - start
print(delta)
print(harvest)
