import sys
import time

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

