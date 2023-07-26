import time

#
# The xx  module is only meant  to "get to know"  something about some
# interesting tags in the (potentially large) xml file.
#

input_file = input('Welke file wil je verwerken?')
f = open(input_file, encoding="unicode_escape") #utf-8")

output_file = input('In welke file wil je extracts dumpen?')
o = open(output_file, 'w', encoding="unicode_escape")

do_sample = input('Als je alles wil verwerken druk [a]\nof als enkel een staal wil nemen druk [s].')

start = time.time()
cc=0
tags_currently_open=0
chunk = 1
tag = ''
data=''
tag_context = ''
tags_read = 0
interesting_tags_encountered = 0
inside_tag=False
interesting_records={ 'RRNIdentification': []
                      , 'KBONumberIdentification': []
                     }
do_record=False
all_tags = []
all_data = []
while True:
    f.seek(cc)
    #print(f'position:{cc}')
    cc += 1
    read_data = f.read(chunk)
    if read_data == '<' or inside_tag:
        tag += read_data
    else:
        data += read_data
    #print(f'read:{read_data}')
    if read_data == '>':
        tag_context += tag
        all_tags.append(tag)
        actual_tag=tag.strip('<>/')
        interesting=False
        if actual_tag in interesting_records.keys():
            interesting=True
            interesting_tags_encountered += 1
        if tag[1] == '/':
            tags_currently_open -= 1
            if interesting:
                print(f'interesting {tag=} is a closing tag.')
                do_record=False
        else:
            tags_currently_open += 1
            if interesting:
                print(f'interesting {tag=} is an opening tag.')
                do_record=True
        tag = ''
        #print(tag_context[-50:])
        tags_read += 1
        inside_tag = False
    elif read_data == '<':
        all_data.append(data)
        actual_data = data
        if do_record:
            interesting_records[actual_tag].append(actual_data)
        data = ''
        inside_tag = True
    if 's' == do_sample.lower() and ( interesting_tags_encountered == 3 or tags_read == 5 ):
        break
f.close()
if f.closed:
    print(f"Input bestand {input_file} werd gesloten.")
stop = time.time()
delta = stop - start
print(f"After {delta} seconds we counted {cc} characters and {interesting_tags_encountered} interesting tag occurrences.")
print(interesting_tags_encountered)
print(interesting_records)
interesting_tags = []
if 'j' == input('Do you want to collect interesting tags?').lower():
    for tag in all_tags:
        if 'j' == input(f'Is {tag} an interesting tag?').lower():
            interesting_tags.append(tag)
print(interesting_tags)
            
