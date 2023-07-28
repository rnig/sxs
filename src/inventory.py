import csv
import hy_io # hfs
import hy_is # his
import hy_ds # hls
import os
import sys



def read(p_mode='regular'
         , p_path='inventory.csv'
         , p_newline=''
         , p_delimiter=','
         , p_quotechar='"'
         , p_debug=False):
    header = []
    dataset = []
    if p_debug:
        print('p_mode:%s.' % p_mode)
    with open(p_path
              , newline=p_newline) as csvfile:
        if 'regular' == p_mode:
            inventoryreader = csv.reader(csvfile
                                         , delimiter=p_delimiter
                                         , quotechar=p_quotechar)
            try:
                for row in inventoryreader:
                    if p_debug:
                        print(', '.join(row))
                    dataset.append(row)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(p_path
                                                       , inventoryreader.line_num
                                                       , e))
            header = dataset[0]
        elif 'dictionary' == p_mode:
            inventoryreader = csv.DictReader(csvfile)
            header = inventoryreader.fieldnames
            if p_debug:
                print(header)
            for row in inventoryreader:
                if p_debug:
                    print('-----')
                    for f in inventoryreader.fieldnames:
                        print(row[f])
                    print('-----')
                dataset.append(row)
        else:
            print('Unknown mode.')
        return header, dataset

            
def write(p_mode='regular'
          , p_path='inventory.csv'
          , p_newline=''
          , p_delimiter=','
          , p_quotechar='"'
          , p_fieldnames=[ 'a', 'b', 'c' ]
          , p_dataset=[ [ 'a', 'b', 'c' ]
                        , [ 0, 1, 2 ]
                        , [ 3, 4, 5 ] ]
          , p_debug=False):
    if p_debug:
        print('p_mode:%s.' % p_mode)
    with open(p_path
              , 'w'
              , newline=p_newline) as csvfile:
        if 'regular' == p_mode:
            inventorywriter = csv.writer(csvfile
                                         , delimiter=p_delimiter
                                         , quotechar=p_quotechar
                                         , quoting=csv.QUOTE_MINIMAL)
        elif 'dictionary' == p_mode:
            inventorywriter = csv.DictWriter(csvfile, fieldnames=p_fieldnames)
            inventorywriter.writeheader()
        else:
            print('Unknown mode.')
        for data_row in p_dataset:
            inventorywriter.writerow(data_row)

            
def demo(p_mi='./tmp/mi.csv'):
    print('hallo')
    # TODO:  do this  using the  same  logic as  meant to  by in  'def
    # interact()':
    write(p_mode='regular'
              , p_path=p_mi)
    # TODO:  do this  using the  same  logic as  meant to  by in  'def
    # interact()':
    write(p_mode='dictionary'
          , p_path=p_mi
          , p_fieldnames=[ 'first_name', 'last_name' ]
          , p_dataset=[ {'first_name': 'Baked', 'last_name': 'Beans'}
                        , {'first_name': 'Lovely', 'last_name': 'Spam'}
                        , {'first_name': 'Wonderful', 'last_name': 'Spam'} ])
    reading_modes = [ 'regular'
                      , 'dictionary' ]
    reading_list = [ 'inventory-regular.csv'
                     , 'inventory-dictionary.csv' ]
    for mode in reading_modes:
        print('====================')
        for item in reading_list:
            print('***************')
            if mode in item:
                print('Reading %s in %s mode.' % (item,mode))
                # TODO: do this using the same logic as meant to by in
                # 'def interact()':
                read(p_mode=mode
                     , p_path=os.path.join('.','ttt'
                                          ,item)
                     , p_debug=True)


def interactive_read(p_mi='/path/to/inventory.csv'
                     , p_debug=True):
    # TODO: use grep.py to fill this up.
    item_types = hy_io.list_directory(hy_is.query_path('naar de NBB dumps'))
    item_type_question = '''
Wat do you want to read ?
+------------------/
|'''
    itq = '\n|\t'.join([ item_type_question ] + item_types + [ '\n+-->'] )
    item_type = str(hy_is.ask_input(itq)).lower()            
    header, datas = read(p_mode='regular'
                         , p_path=item_type
                         , p_delimiter=hy_is.ask_input('Geef een scheidingsteken op voor de velden en elk record aub ?')) #os.path.join(p_mi,item_type+'.csv'))
    #datas = hy_io.load_inventory(item_type, p_debug)
    if p_debug:
        print(datas)
        hy_is.confirm_to_continue('Shall we stride forward ?')
    return header, datas #return datas[0], datas[1:]


def interactive_focus(p_attributes=[ 'a', 'b', 'c' ]
                      , p_data=[ [ 1, 2, 3 ], [ 4, 5, 6] ]
                      , p_debug=True):
    scope = hy_is.get_attributes(p_item_attributes=p_attributes
                               , p_question='Which attributes are in scope ?')
    filter = hy_is.get_filter(p_item_attributes=p_attributes
                            , p_attributes_question='On which attributes do you want to filter ?'
                            , p_filter_question='What values are interesting for %s ?')
    if p_debug:
        print('p_attributes:%s.' % p_attributes)
        print('p_data  :%s.' % p_data)
        print('scope :%s.' % scope)
        print('filter:%s.' % filter)
        inc_data_set,exc_data_set = hy_ds.extract_data(p_data=p_data
                                                       , p_all_attrs=p_attributes
                                                       , p_scope_attrs=scope
                                                       , p_filter=filter
                                                       , p_debug=True)
    if p_debug:
        print('Exclusion data set:%s.' % exc_data_set)
        print('Inclusion data set:%s.' % inc_data_set)
    print()
    print('  ************************************  ')
    print('****  This is currently in scope :  ****')
    print('  ************************************\n')
    print('\t%s' % scope)
    print('  ------------------------------------  ')
    for item in inc_data_set:
        print('\t%s' % item)
    print('\n  ************************************')
    return scope, filter, inc_data_set, exc_data_set


def interactive_count(p_attributes
                      , p_data
                      , p_debug=False):
    group_by_items = []
    for gbi in p_attributes:
        if hy_is.confirmed('Do you want to add %s to the group by item list ?' % gbi):
            group_by_items.append(gbi)
    for i in group_by_items:
        summary_statistics = {}
        for r in p_data:
            v = r[p_attributes.index(i)]
            if v not in summary_statistics.keys():
                summary_statistics[v] = 1
            else:
                summary_statistics[v] += 1
        print('We have %d different values for %s.' % (len(summary_statistics.keys()), i))
        print('Their occurrences :\n-----------')
        for k in summary_statistics:
            print('%s\t%d' % (k, summary_statistics[k]))


def interact(p_mi
             , p_debug=False):
    header = None
    datas = None
    scope = None
    filter = None
    inc_data_set = None
    exc_data_set = None
    while True:
        question='''
What to do ?

Choose from :
+-------/
|
|\t [d] emo
|\t [r] ead
|\t [f] ocus & filter
|\t [w] rite
|\t [c] ount
|\t [q] uit
|
+-------->'''
        mode = str(hy_is.ask_input(question))[:1].lower()
        if 'q' == mode:
            break
        elif 'd' == mode:
            demo()
        elif 'r' == mode:
            header, datas = interactive_read(p_mi)
        elif 'f' == mode:
            if not header and not datas:
                print('Please read an item 1st.')
            else:
                scope, filter, inc_data_set,exc_data_set = interactive_focus(header,datas)
        elif 'c' == mode:
            if not (inc_data_set or scope):
                print('Please read an item 1st & optionally focus on it.')
            else:
                print('\t%s counts %d items.' % (inc_data_set, len(inc_data_set)))
                interactive_count(p_attributes=scope
                                  , p_data=inc_data_set)
        elif 'w' == mode:
            if not inc_data_set:
                print('Please read an item 1st & optionally focus on it.')
            else:
                print('''
\tThanks  for  having read  an  item  type  &  having focused  on  it.
\tunfortunately we  have not  yet had the  occasion to  implement this
\tfeature.
\tStay tuned !
''')
                hy_io.mini_store( [ ';'.join(scope) + '\n' ] + [ ';'.join(row) + '\n' for row in inc_data_set]
                                  , hy_io.get_path( [ hy_is.query_path('naar folder waarin het gefilterd resultaat mag opgeslaan worden')
                                                      , hy_is.ask_input('Welke bestandsnaam heb je graag?') ] ) )
        else:
            print('Please, answer the question.')

            

if __name__ == '__main__':
    nargs = len(sys.argv)
    if nargs == 1:
        base=hy_io.get_base_dir(sys.argv[0])
        mi = os.path.join(base,'..', 'mi','actual') 
        interact(mi)
    else:
        parser = OptionParser()
        parser.add_option('-d'
                          , '--debug_mode'
                          , dest='debug'
                          , help='Show additional output.'
                          , default=False)
        (options, args) = parser.parse_args()
        # if not options.debug:
        #     parser.error('No debug mode has been specified.')
