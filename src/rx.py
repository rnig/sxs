import hy_io
import hy_is
import math

mode_map = { 'aan' : 'add'
             , 'af' : 'close' }

def load_template_map(template_path, template_map='template.map'):
    puzzle = {}
    print(f"{template_path=}, {template_map=}.")
    for mapping in hy_io.load(hy_io.get_path([ template_path, template_map ])):
        multiplicity, reference = mapping.strip().split(':')
        print(f"{mapping=}, {multiplicity=}, {reference=}.")
        reference_template = hy_io.get_path([ template_path, reference ])
        if '.' == multiplicity:
            puzzle[reference] = hy_io.load(reference_template)
        else:
            puzzle[reference] = [ hy_io.load(reference_template) ]
    return puzzle
    
    
def generate_declaration():
    pass
    


if __name__ == '__main__':
    output = []
    modus = None
    while modus not in [ 'aan', 'af' ]:
        modus = hy_is.ask_input("Wil je aanmelden [typ: 'aan'] of afmelden [typ: 'af']?").lower()
    data_path = hy_is.query_path('naar het bestand met de gegevens')
    template_puzzle = load_template_map(hy_is.query_path('naar de template folder'))
    print(f"{template_puzzle=}.")
    output = generate_declaration()
    output_folder = hy_is.query_path('naar de weergave folder')
    output_file = hy_is.ask_input('Hoe wil je het bestand benoemen?')
    if output:                              
        hy_io.mini_store(output, hy_io.get_path([ output_folder, output_file ]))
