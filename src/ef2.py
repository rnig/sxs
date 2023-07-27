import sys
import time

#######################################################################
# Op basis van  nested_level kan je een  headerlijn definieren terwijl
# de XML wordt afgelezen.  Telkens een tag wordt afgewerkt moet de tag
# zelf in de header verwerkt worden.
#
# Als we buiten de tag zitten dus  in de feitelijke data, moet de data
# in de datarij worden opgeslagen onder de juiste header.
#
# Als een  tag (meerdere)  geneste tags en  dus sub-levels  heeft maar
# zonder  zelf  data   te  bevatten  moeten  de   sub-levels  via  een
# verbindingsteken aan hun parent-level  worden gekleefd in de header,
# bijv:
#
# P1-H1.1 | P1-H1.2 | H2 | P3-H3.1  | P3-H3.2
# --------+---------+----+----------+--------
# d1.1    | d1.2    | d2 | d3.1     | d3.2
#
# Alternatief  zou  je  in  een rekenblad  alle  sublevels  onder  een
# parent-headerlijn kunnen grouperen, bijv:
#
# P1           |       | P3
# H1.1 | H1.2  | H2    | H3.1  | H3.2
# -----+-------+-------+-------+--------
# d1.1 | d1.2  | d2    | d3.1  | d3.2
#
#######################################################################

input_file = open(input('Welke file wil je verwerken?')) #, encoding="unicode_escape") #utf-8")

start = time.time()
chunk_counter = 0
chunk = 1
data_read = None
focus_line = ''
inside_tag = False
inside_closing_tag = False
last_tag=None
nested_level = -1
open_tags=[]
csv_header = []
records = []
last_record = []
while True:
    input_file.seek(chunk_counter)
    data_read = input_file.read(chunk)
    if not data_read:
        break
    else:
        focus_line += data_read
        chunk_counter += 1
    if data_read == '>':
        print(f'<*>[{data_read=}], {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {open_tags=}, {last_tag=}, {nested_level=}, {csv_header=}, {last_record=}, {records=}.')        
        inside_tag = False
        if inside_closing_tag:
            inside_closing_tag = False
            if len(open_tags) >= nested_level and len(open_tags[nested_level]) > 0:
                popped_tag = open_tags[nested_level].pop()
                if len(open_tags[nested_level]) == 0:
                    del open_tags[-1]
            if nested_level == 1:
                records.append(last_record)
                last_record = []
            print('Levelling down.')
            nested_level -= 1
            print(f'<level-change>[{data_read=}], {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {open_tags=}, {last_tag=}, {nested_level=}, {csv_header=}, {last_record=}, {records=}.')
        else:
            last_tag = focus_line[focus_line.find('<')+1:-1].split()[0].strip('?')
            if nested_level == -1:
                open_tags.append( [ last_tag ] )
            elif nested_level == 0:
                open_tags[nested_level].append(last_tag)
            else:
                if len(open_tags) <= nested_level+1:
                    open_tags.append( [ last_tag ] )
                else:
                    print(f'Deze situatie is niet voorzien!\n[{data_read=}], {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {open_tags=}, {last_tag=}, {nested_level=}, {csv_header=}, {last_record=}, {records=}.')
                    sys.exit()
            if last_tag not in csv_header:
                csv_header.append(last_tag)
        focus_line=''
    elif data_read == '<':
        inside_tag = True
    elif data_read == '/':
        if inside_tag:
            if len(focus_line) == 2 and focus_line[0] == '<':
                inside_closing_tag = True
            else:
                i = focus_line.find('<')
                if i > 0 and focus_line.find(data_read) == i+1:
                    inside_closing_tag = True
    else:
        print(f"{focus_line=}.")
        if inside_tag and len(focus_line) == 2 and focus_line[1] != '?':
            print('Levelling up.')
            nested_level += 1
            print(f'<level-change>[{data_read=}], {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {open_tags=}, {last_tag=}, {nested_level=}, {csv_header=}, {last_record=}, {records=}.')
        if inside_closing_tag and focus_line[-2] == '/' and focus_line[0] != '<':
            while len(last_record) < len(csv_header):
                last_record.append('')
            last_record[csv_header.index(last_tag)] = focus_line[:focus_line.find('<')]
            print(f"<***>{focus_line[:focus_line.find('<')]} goes into slot {csv_header.index(last_tag)=} so we get record {last_record=}.")
            print(f'<****>:{data_read}, {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {open_tags=}, {last_tag=}, {nested_level=}, {csv_header=}, {last_record=}, {records=}.')
input_file.close()
stop = time.time()
delta = stop - start
print(f"After {delta} seconds we counted {chunk_counter} characters and entered {len(records)} records.")
output_folder = input('To which folder do you want to write the fields focused upon?')
record_file = open(output_folder+'/records.csv', 'a')
record_file.write(';'.join(csv_header)+'\n')
for record in records:
    print(record)
    record_file.write(';'.join(record)+'\n')
