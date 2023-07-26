import sys
import time

#
# De module  xf is bedoeld om  een lange xml lijn  te herformateren in
# ietwat leesbare door regeleinden afgebakende tekst.
#
# Voorbeeld:
# (sxs) d:\sxs>py src\xf.py
# Welke file wil je verwerken?dat\out\sample-cy.txt
# Naar welke file wil je schrijven?dat\out\sample-cy.xml
# xml_line_counter=0, output_line='<?xml version="1.0" encoding="UTF-8"?>\n', nested_level=0
# xml_line_counter=1, output_line='<Extract xmlns="http://www.nbb.be/cba/2021-06/extract">\n', nested_level=0
# xml_line_counter=2, inline='____<Header>\n', nested_level=1
# xml_line_counter=3, inline='________<DeclarerId>\n', nested_level=2
# xml_line_counter=4, inline='____________<DeclarerKBONumber>\n', nested_level=3
# xml_line_counter=5, output_line='0403288089</DeclarerKBONumber>', , end_data_index=10, nested_level=3
# xml_line_counter=5, inline='________________0403288089\n', nested_level=3
# xml_line_counter=6, inline='____________</DeclarerKBONumber>\n', nested_level=3
# xml_line_counter=7, output_line='</DeclarerId>', , end_data_index=0, nested_level=2
# xml_line_counter=7, inline='________</DeclarerId>\n', nested_level=2
# xml_line_counter=8, inline='________<ExtractDate>\n', nested_level=2
# ...
#
# en het output bestand start dan als volgt:
#
# <?xml version="1.0" encoding="UTF-8"?>
# <Extract xmlns="http://www.nbb.be/cba/2021-06/extract">
# ____<Header>
# ________<DeclarerId>
# ____________<DeclarerKBONumber>
# ________________0403288089
# ____________</DeclarerKBONumber>
# ________</DeclarerId>
# ________<ExtractDate>
# ____________2023-06-05
# ________</ExtractDate>
# ________<FileNumber>
# ____________1
# ________</FileNumber>
# ________<FileReference>
# ____________0403288089-20230605-20230605-00001523-NoPeriod-00000001.xml
# ________</FileReference>
# ____</Header>
# ...
#
input_file = open(input('Welke file wil je verwerken?')) #, encoding="unicode_escape") #utf-8")
output_file = open(input('Naar welke file wil je schrijven?'), 'a', newline='') #, encoding="unicode_escape") #utf-8")

start = time.time()

nested_level = 0
chunk_counter = 0
chunk = 1
data_read = None
inside_tag = False
inside_closing_tag = False
inline = ''
output_line = ''
xml_line_counter = 0
while True:
    input_file.seek(chunk_counter)
    chunk_counter += 1
    data_read = input_file.read(chunk)
    if not data_read:
        break
    output_line += data_read
    if data_read in [ '<', '/', '>' ]:
        if data_read == '<':        
            inside_tag = True
        if inside_tag:
            if data_read == '>':
                inside_tag = False
                if inside_closing_tag:
                    inside_closing_tag = False
                    end_data_index = output_line.find('</')
                    print(f"{xml_line_counter=}, {output_line=}, , {end_data_index=}, {nested_level=}")
                    if end_data_index > 0:
                        inline = '____'*(nested_level+1)+output_line[:end_data_index]+'\n'
                        output_file.write(inline)
                        print(f"{xml_line_counter=}, {inline=}, {nested_level=}")
                        xml_line_counter += 1
                        output_line=output_line[end_data_index:]
                    inline = '____'*nested_level+output_line+'\n'
                    output_file.write(inline)
                    print(f"{xml_line_counter=}, {inline=}, {nested_level=}")
                    xml_line_counter += 1
                    nested_level -= 1
                    output_line=''
                else:
                    if output_line[1] == '?' and output_line[-2] == '?':
                        output_line += '\n'
                        output_file.write(output_line)
                        print(f"{xml_line_counter=}, {output_line=}, {nested_level=}")
                        xml_line_counter += 1
                        output_line = ''
                    elif xml_line_counter == 1:
                        output_line += '\n'
                        output_file.write(output_line)
                        print(f"{xml_line_counter=}, {output_line=}, {nested_level=}")
                        xml_line_counter += 1
                        output_line = ''
                    else:
                        nested_level += 1
                        output_line += '\n'
                        inline = '____'*nested_level+output_line
                        output_file.write(inline)
                        print(f"{xml_line_counter=}, {inline=}, {nested_level=}")
                        xml_line_counter += 1
                        output_line = ''
            elif data_read == '/' and output_line[-2] == '<':
                inside_closing_tag = True
        else:
            print(f'{data_read} not inside tag, {output_line=}.')
input_file.close()
output_file.close()

stop = time.time()
delta = stop - start
print(f"After {delta} seconds we counted {chunk_counter} characters and reformatted {xml_line_counter} lines.")

