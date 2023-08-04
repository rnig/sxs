from string import Template
import copy
import hy_io
import hy_is
import math

# Convention.0:
#   Templates are files enlisted in a file called 'template.map'.

# Convention.1:
mode_map = { 'aan' : 'Add'
             , 'af' : 'Close' }

# Convention.2:
template_replacing_sequence = [ 'map', 'exn' ] 

# Convention.3:
file_number = 1
state = { 'FILE_REFERENCE' : Template('$DECLARER_KBO-INC-UAT-$TODAY-$FILE_NUMBER.xml')
          , 'FILE_NUMBER' : "{0:0>3}".format(file_number)
          , 'MODUS' : 'af'
          , 'TODAY' : '20230804'
          , 'DECLARER_KBO' : '0403288089'
         }



def load_template_data(path, filename, holder_data={}):
    for m in hy_io.load(hy_io.get_path([ path, filename ])):
        place_holder, place_data = None, None
        try:
            place_holder, place_data = m.strip().split('|')
            if 'NIL' != place_holder.strip():
                holder_data[place_holder.strip()] = place_data.strip()
        except ValueError as ve:
            print(f"{m=} botst op een uitzondering.\nVoorzie enkel lijnen met een '|' als scheidingsteken aub.")
        except Exception as e:
            print(f"{m=} botst op uitzondering {e=}.")
    return holder_data
            
    
def load_template(path, filename):
    return Template(''.join(hy_io.load(hy_io.get_path([ path, filename.strip() ]))))


def generate_declaration(template_path, template_map, data):
    global state
    declaration = []
    for template in hy_io.load(hy_io.get_path([ template_path, template_map ])):
        holder_data = load_template_data(template_path, template.strip().split('.')[0]+'.map')
        if hy_io.path_exists(hy_io.get_path([ template_path, template.strip().split('.')[0]+'.exn' ])):
            holder_data = load_template_data(template_path, template.split('.')[0]+'.exn', holder_data)
        if 'Literal' == holder_data['PlaceHolder']:
            template_content = load_template(template_path, template)
            for k in holder_data.keys():
                print(k, holder_data[k])
                if 'STATE' in holder_data[k]:
                    print(state[holder_data[k].split(':')[1]])
                    holder_data[k] = state[holder_data[k].split(':')[1]]
            declaration.append(template_content.safe_substitute(holder_data))
        elif 'Data' ==  holder_data['PlaceHolder']:
            data_header = data[0].strip().split(';')
            for row in data[1:]:
                template_content = load_template(template_path, template)
                holder_data_row_copy = dict(holder_data)
                for ph in holder_data_row_copy.keys():
                    if holder_data_row_copy[ph] in data_header:
                        phi = data_header.index(holder_data_row_copy[ph])
                        phv = row.split(';')[phi]
                        holder_data_row_copy[ph] = phv
                holder_data_row_copy['Action'] = mode_map[state['MODUS']] # This is ugly but it works...
                holder_data_row_copy['Modus'] = mode_map[state['MODUS']]+'Action' # This is very ugly but it works...
                declaration.append(template_content.safe_substitute(holder_data_row_copy))
    return ''.join(declaration)
    


if __name__ == '__main__':
    output = []
    modus = None
    while modus not in mode_map.keys():
        modus = hy_is.ask_input("Wil je aanmelden [typ: 'aan'] of afmelden [typ: 'af']?").lower()
    state['MODUS'] = modus
    output = generate_declaration(hy_is.query_path('naar de template folder')
                                  , hy_is.ask_input('Welke template map wil je gebruiken?')
                                  , hy_io.load(hy_is.query_path('naar het bestand met de gegevens')))
    output_folder = hy_is.query_path('naar de weergave folder')
    output_file = hy_is.ask_input('Hoe wil je het bestand benoemen?')
    if output:                              
        hy_io.mini_store(output, hy_io.get_path([ output_folder, output_file ]))
