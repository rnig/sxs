import hy_io
import hy_is

MAXIMUM_BATCH_SIZE = 100 # NBB specification is 10000



def process_data(data_path, batch_size=-1, data_has_header=True):
    global MAXIMUM_BATCH_SIZE
    batches = []
    data_start_index = 0
    if batch_size < 0:
        batch_size = MAXIMUM_BATCH_SIZE
    full_payload = hy_io.load_inventory(data_path, True)
    if full_payload and len(full_payload) > 0:
        header = None
        if data_has_header:
            header =full_payload[0]
            data_start_index = 1
        batch_index = 0
        while batch_index <= (len(full_payload) - data_start_index)//batch_size:
            data = full_payload[batch_index * batch_size:(batch_index + 1) * batch_size]
            if header and batch_index > 0:
                data.insert(0, header)
            batches.append(data)
            batch_index += 1
    return batches
    


if __name__ == '__main__':
    qp = hy_is.query_path('naar het bestand met de gegevens')
    fn = hy_io.get_file_name(qp).split('.')[0]
    batches = process_data(qp
                           , int(hy_is.ask_input('Hoeveel dossiers per batch?')))
    out_path = hy_is.query_path('naar het weergave bestand')
    bc = 0
    for b in batches:
        hy_io.mini_store([ ';'.join(l)+'\n' for l in b ], hy_io.get_path([ out_path, fn + '-batch-' + str(bc) + '.csv']))
        bc += 1
    
                         
