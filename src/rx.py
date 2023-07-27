from jinja2 import Template
import hy_io


cfg_path = 'cfg'
dat_path = 'dat'
out_path = 'tmp'
pieces = [ 'declaration_header.xml'
           , 'declaration_rrn-header.xml'
           , 'declaration_close.xml'
           , 'declaration_rrn-footer.xml'
           , 'declaration_footer.xml' ]

injection_data = hy_io.load_inventory(input("Waar staat de data?"))
buffer = ''
for p in pieces:
    template = Template(''.join(hy_io.load(hy_io.get_path([ cfg_path, p ], 'WINDOWS'))))
    buffer += template.render(injection_data)
hy_io.mini_store(buffer, input("Naar welk bestand mag het gegenereerde resultaat worden geschreven?"))
