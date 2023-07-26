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
print(f'A:{data_read}, {focus_line=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {open_tags=}.')
while True:
    input_file.seek(chunk_counter)
    data_read = input_file.read(chunk)
    if not data_read:
        break
    else:
        #print(f"Read '{data_read}' and sticking it to '{focus_line}'.")
        focus_line += data_read
        chunk_counter += 1
    if data_read == '>':
        inside_tag = False
        if len(focus_line) > 0 and focus_line[-2] == '?':
            print('Exiting prolog.')
        elif inside_closing_tag:
            inside_closing_tag = False
            print(f"{focus_line=}, {nested_level=}, {open_tags=}, {last_tag=}.")
            if len(open_tags) >= nested_level and len(open_tags[nested_level]) > 0:
                popped_tag = open_tags[nested_level].pop()
                if len(open_tags[nested_level]) == 0:
                    del open_tags[-1]
            nested_level -= 1
            print(f"Leveling down, {popped_tag=}, {open_tags=}, {nested_level=}.")
        else:
            last_tag = focus_line[focus_line.find('<')+1:-1].split()[0]
            if nested_level == 0:
                open_tags.append( [ last_tag ] )
            else:
                print(f"{focus_line=}, {nested_level=}, {open_tags=}, {last_tag=}.")
                if len(open_tags) <= nested_level:
                    open_tags.append( [ last_tag ] )
                else:
                    print(f'B:{data_read}, {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {open_tags=}, {last_tag=}, {nested_level=}.')
                    sys.exit()
                #     if len(open_tags) == nested_level +1:
                #     if len(open_tags[nested_level]) > 0:
                #         open_tags[nested_level].append(last_tag)
                #     else len(open_tags[nested_level]) > 0:
                # else:
                #     open_tags[nested_level].append(last_tag)
            # if last_tag not in csv_header:
            #     csv_header.append(last_tag)
            #     if len(csv_header) > 5:
            #         print(f"{csv_header}, {open_tags=}.")
            #         sys.exit()
        focus_line=''
    elif data_read == '<':
        inside_tag = True
        # if len(focus_line) > 1 and focus_line[-2] == '>' and focus_line[-3] != '?':
        #     focus_line = data_read
        #     print('Leveling up.')
        #     nested_level += 1
        #     print(f"L+:{focus_line=}, {nested_level=}, {open_tags=}, {last_tag=}.")
    elif data_read == '?':
        if len(focus_line) > 0 and focus_line[-2] == '<':
            print(f'Entering prolog.')
    elif data_read == '/':
        if inside_tag:
            inside_closing_tag = True
    elif data_read == '\n':
        print(f'Skipping newline after {focus_line[-5:]}.')
    else:
        if inside_tag and len(focus_line) == 2:
            print('Leveling up.')
            nested_level += 1
            print(f"L+:{focus_line=}, {nested_level=}, {open_tags=}, {last_tag=}.")
        print(f'A:{data_read}, {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {nested_level=}.')
print(f'Z:{data_read}, {focus_line=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {open_tags=}.')
    # if data_read in [ '<', '/', '>' ]:
    #     if data_read == '<':        
    #         inside_tag = True
    #         if len(focus_line) > 2 and focus_line[-2] == '>' and focus_line[-3] != '?':
    #             last_tag = focus_line.split()[0].strip('</>?')
    #             if len(open_tags) == nested_level +1 and len(open_tags[nested_level]) > 0:
    #                 open_tags[nested_level].append(last_tag)
    #             else:
    #                 open_tags.append( [ last_tag ] )
    #             if last_tag not in csv_header:
    #                 csv_header.append(last_tag)
    #                 if len(csv_header) > 5:
    #                     print(f"{csv_header}, {open_tags=}.")
    #                     sys.exit()
    #             focus_line = ''
    #             nested_level += 1
    #         print(f'B:{data_read}, {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {nested_level=}.')
    #     if inside_tag:
    #         if data_read == '>':
    #             inside_tag = False
    #             print(f'C.1:{data_read}, {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {nested_level=}.')
    #             if inside_closing_tag:
    #                 inside_closing_tag = False
    #                 start_data_index = focus_line.find('>')+1
    #                 end_data_index = focus_line.find('</')
    #                 print(f'D:{data_read}, {focus_line=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {start_data_index=}, {end_data_index=}.')
    #                 if end_data_index > 0:
    #                     if last_tag in csv_header:
    #                         record_index = csv_header.index(last_tag)
    #                         while len(last_record) < record_index + 1:
    #                             last_record.append('')
    #                         if last_record[record_index] == '':
    #                             last_record.insert(record_index, focus_line[start_data_index:end_data_index])
    #                         else:
    #                             last_record[record_index] += '| ' + focus_line[start_data_index:end_data_index]
    #                         print(f'E:{data_read}, {focus_line=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {start_data_index=}, {end_data_index=}.')
    #                         print(f"Inserted '{focus_line[start_data_index:end_data_index]}' at index {record_index}.") 
    #                     else:
    #                         print(f'F:{data_read}, {focus_line=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {start_data_index=}, {end_data_index=}.')
    #                         print(f"Oekandana!")
    #                         sys.exit()    
    #                     focus_line=focus_line[end_data_index:].strip()
    #                     print(f'G:{data_read}, {focus_line=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {start_data_index=}, {end_data_index=}.')
    #                 nested_level -= 1
    #                 focus_line=''
    #                 if len(open_tags[nested_level]) == 0:
    #                     print(open_tags.pop())
    #                     if nested_level == 1:
    #                         records.append(last_record)
    #                         last_record = []
    #                         print(f"{records=}.")
    #         elif data_read == '/' and focus_line[-2] == '<':
    #             inside_closing_tag = True
    #             start_data_index = focus_line.find('>')+1
    #             last_tag = focus_line[:start_data_index].strip('</>?')
    #             print(f'C.2:{data_read}, {focus_line[-5:]=}, {inside_tag=}, {inside_closing_tag=}, {last_tag=}, {nested_level=}, {start_data_index=}.')
    #             if len(open_tags) == nested_level +1 and len(open_tags[nested_level]) > 0:
    #                 open_tags[nested_level].append(last_tag)
    #             else:
    #                 open_tags.append( [ last_tag ] )
    #             if last_tag not in csv_header:
    #                 csv_header.append(last_tag)
    #                 if len(csv_header) > 5:
    #                     print(f"{csv_header}, {open_tags=}.")
    #                     sys.exit()
    #     else:
    #         print(f'{data_read} not inside tag, {focus_line=}.')
input_file.close()

stop = time.time()
delta = stop - start
print(f"After {delta} seconds we counted {chunk_counter} characters and entered {len(records)} records.")
# output_folder = input('To which folder do you want to write the fields focused upon?')
# record_file = open(output_folder+'/records.txt', 'a')
# record_file.write(';'.join(csv_header)+'\n'+len(csv_header)*'='+'\n')
# for record in records:
#     print(record)
#     record_file.write(';'.join(record)+'\n')
