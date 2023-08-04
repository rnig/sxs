from string import Template
import hy_io
import hy_is
import math

mode_map = { 'aan' : 'add'
             , 'af' : 'close' }



# def load(path, filename='template.map'):
#     map = {}
#     for mapping in 
#         section = mapping.split('.')[0]
#         map[section] = hy_io.load(get_path([ path, section + '.map' ]))
#         place_holder, data = mapping.strip().split('|')
#         map[reference] = hy_io.load(hy_io.get_path([ path, reference ]))
#     return map
    
        
def generate_declaration(template_path, template_map, data):
    declaration = []
    for template in hy_io.load(hy_io.get_path([ template_path, template_map ])):
        template_content = Template(''.join(hy_io.load(hy_io.get_path([ template_path, template.strip() ]))))
        holder_data = {}
        for m in hy_io.load(hy_io.get_path([ template_path, template.strip().split('.')[0]+'.map' ])):
            place_holder, place_data = None, None
            try:
                place_holder, place_data = m.strip().split('|')
                holder_data[place_holder.strip()] = place_data.strip()
            except ValueError as ve:
                print(f"{m=} botst op een uitzondering.\nVoorzie enkel lijnen met een '|' als scheidingsteken aub.")
            except Exception as e:
                print(f"{m=} botst op uitzondering {e=}.")
        declaration.append(template_content.safe_substitute(holder_data))
        hy_is.confirm_to_continue('Gaan we verder?')    
    return declaration
    


if __name__ == '__main__':
    output = []
    modus = None
    while modus not in [ 'aan', 'af' ]:
        modus = hy_is.ask_input("Wil je aanmelden [typ: 'aan'] of afmelden [typ: 'af']?").lower()
    output = generate_declaration(hy_is.query_path('naar de template folder')
                                  , 'template.map'
                                  , hy_io.load(hy_is.query_path('naar het bestand met de gegevens')))
    output_folder = hy_is.query_path('naar de weergave folder')
    output_file = hy_is.ask_input('Hoe wil je het bestand benoemen?')
    if output:                              
        hy_io.mini_store(''.join(output), hy_io.get_path([ output_folder, output_file ]))
