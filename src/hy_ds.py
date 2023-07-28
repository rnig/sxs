"""

@module: 
    hls.py

@author: 
    Erwin Geeraerts <erwin@rnig.be>

@maintainer : 
    Erwin Geeraerts iov RNIG BV 

@backup-maintainer:
    <TODO prio=high>@team:who?</TODO>

@team: 
    RNIG SxS

@original-creation-date: 
    Tue Oct 13 

@purpose: 
    Provide helper methods useful for allround data massaging.

"""



from optparse import OptionParser
import hy_io
import os
import sys



def dedupe(p_list=[], p_debug=False):
    if p_debug:
        print('Enter dedupe.')
        print('p_list : %s.' % p_list)
    processed = set()
    process = processed.add
    if p_debug:
        print('Exit dedupe.')
    return [i for i in p_list if not (i in processed or process(i))]


def unlist(p_list=[['a'],['b'],['c']],p_debug=False):
    if p_debug:
        print('Enter unlist.')
        print('p_list : %s.' % p_list)
    unlisted = []
    for i in p_list:
        unlisted += i
    if p_debug:
        print('unlisted : %s.' % unlisted)
        print('Exit unlist.')
    return unlisted


def show_list(p_list=[], p_debug=False):
    if p_debug:
        print('Enter show_list.')
        print('p_list : %s.' % p_list)
    rc = 0
    for item in p_list:
        if p_debug:
            print('List item %s : %s.' % (rc, str(item).strip()))
        else:
            print('%s' % str(item).strip())
        rc += 1
    if p_debug:
        print('Exit show_list.')
        

def list_to_csv(p_list=[ 'a', 'b', 'c' ]
                , p_item_separator=', '):
    return p_item_separator.join(p_list) 


def dict_to_csv(p_dict={ 'a':0, 'b':1, 'c':2 }
                , p_item_separator='; '
                , p_tuple_item_separator='| '):
    return list_to_csv([str(x) for i,x in enumerate(p_dict.items())], p_item_separator).replace(', ',p_tuple_item_separator)


def init_matrix(p_row_dim=0,p_col_dim=0, p_debug=False):
    if p_debug:
        print('Enter init_matrix.')
        print('p_row_dim : %s.' % p_row_dim)
        print('p_col_dim : %s.' % p_col_dim)
    om = []
    for i in range(p_row_dim):
        om.append([])
        for j in range(p_col_dim):
            om[i].append(0)
    if p_debug:
        show_list(om,p_debug)
        print('Exit init_matrix.')
    return om


def intersect_lists(p_list_1=[], p_list_2=[], p_debug=False):
    if p_debug:
        print('Enter intersect_lists.')
        print('p_list_1 : %s.' % str(p_list_1))
        print('p_list_2 : %s.' % str(p_list_2))
    my_isect_idxs = []
    my_isect_vals = []
    for a_item in p_list_1:
        if p_debug:
            print('Evaluating item %s in p_list_1.' % a_item)
        my_isect_idxs += [i for i,x in enumerate(p_list_2) if str(x).lower().strip() == str(a_item).lower().strip()]
        my_isect_vals += [x for i,x in enumerate(p_list_2) if str(x).lower().strip() == str(a_item).lower().strip()]
    if p_debug:
        print('Intersect indexes of p_list_1 and p_list_2 is : %s.' % my_isect_idxs)
        print('Intersect values of p_list_1 and p_list_2 is : %s.' % my_isect_vals)
        print('Exit intersect_lists.')
    return my_isect_idxs, my_isect_vals


def complement_lists(p_list_1=[], p_list_2=[], p_debug=False):
    if p_debug:
        print('Enter complement_lists.')
        print('p_list_1 : %s.' % str(p_list_1))
        print('p_list_2 : %s.' % str(p_list_2))
    r_complement = []
    for a_item in p_list_1:
        if p_debug:
            print('Evaluating item %s in p_list_1.' % a_item)
        if a_item not in p_list_2:
            r_complement.append(a_item)
    if p_debug:
        print('Exit complement_lists.')
        print('r_complement :%s.' % r_complement)
    return r_complement


def extract_data(p_data=[], p_all_attrs=[], p_scope_attrs=[], p_filter={} , p_debug=False):
    if p_debug:
        print('Enter extract_data.')
        print('p_data    : %s.' % str(p_data))
        print('p_all_attrs   : %s.' % str(p_all_attrs))
        print('p_scope_attrs   : %s.' % str(p_scope_attrs))
        print('p_filter  : %s.' % p_filter)
    # Given a list of required attributes,
    # give corresponding positions of those in a data set.
    attr_idxs, attr_vals = intersect_lists(p_scope_attrs,p_all_attrs,p_debug)
    if p_debug:
        print('Attributes in scope:')
        print('attr_idxs : %s.' % attr_idxs)
        print('attr_vals : %s.' % attr_vals)
    # Given a list of filter attributes,
    # give corresponding positions of those in a data set.
    filt_idxs, filt_vals = intersect_lists(list(p_filter.keys()),p_all_attrs,p_debug)
    filt_nbr = len(filt_idxs)
    if p_debug:
        print('Filtering by...')
        print('filt_idxs : %s.' % filt_idxs)
        print('filt_vals : %s.' % filt_vals)
        print('filt_nbr  : %s.' % filt_nbr)
    extracted_data = []
    excluded_data = []
    for data_row in p_data:
        if p_debug:
            print('=======================')
        # filter rows
        filt_cnt = 0
        for filt_i in filt_idxs:
            # Compare the value of a given filter attribute
            # with the value of the corresponding data row attribute.
            if p_debug:
                print('filt_i:%d.' % filt_i)
                print('pp_all_attrs[filt_i]:%s.' % p_all_attrs[filt_i])
                print('p_filter:%s.' % p_filter)
            filt_attr_vals = p_filter[p_all_attrs[filt_i].lower().strip()]
            data_row_attr_val = str(data_row[filt_i]).lower().strip()
            if p_debug:
                print('data row          : %s.' % data_row)
                print('filt_cnt          : %s.' % filt_cnt)
                print('filt_i            : %s.' % filt_i)
                print('filt_attr_vals     : %s.' % filt_attr_vals)
                print('data_row_attr_val : %s.' % data_row_attr_val)
            for filt_attr_val in filt_attr_vals:
                norm_filt_attr_val = str(filt_attr_val).lower()
                if p_debug:
                    print('norm_filt_attr_val  : %s.' % norm_filt_attr_val)
                if norm_filt_attr_val == data_row_attr_val:
                    if p_debug:
                        print('Attribute match ! ')
                        print('filt_cnt          : %s.' % filt_cnt)
                        print('-----------------------')
                    filt_cnt += 1
                    break
        if filt_cnt == filt_nbr:
            if p_debug:
                print('Row match ! ')
                print('filt_cnt          : %s.' % filt_cnt)
                print('-----------------------')
            a_row = []
            for i in attr_idxs:
                a_row.append(data_row[i])
                if p_debug:
                    print('-----------------------')
                    print('Appending      : %s.' % data_row[i])
                    print('-----------------------')
            extracted_data.append(a_row)
        else:
            if p_debug:
                print('Row skip.')
                print('filt_cnt          : %s.' % filt_cnt)
                print('-----------------------')
            excluded_data.append(data_row)
        if p_debug:
            print('=======================')
    if p_debug:
        print('extracted_data   : %s.' % extracted_data)
        print('excluded_data   : %s.' % excluded_data)
        print('Exit extract_data.')
    return extracted_data, excluded_data
    

        
if __name__ == '__main__':
    home = os.path.expanduser('~')
    operations = [ 'dedupe', 'intersect', 'extract' , 'complement', 'list' ]
     #
    #  Input Validation.
    ## -----------------
    run_mode_parser = OptionParser()
    run_mode_parser.add_option('-m'
                               , '--mode'
                               , dest='mode'
                               , help='Execution mode : [cli] for interactive\nor [bat] for batch processing.'
                               , default='cli')
    run_mode_parser.add_option('-d'
                               , '--debug_mode'
                               , dest='debug_mode'
                               , help='Add more verbouse output usefull for debugging.'
                               , default='-')
    run_mode_parser.add_option('-o'
                               , '--operation'
                               , dest='operation'
                               , help='An inventory of middleware systems in CSV Data format.'
                               , default='-')
    (run_mode_options, run_mode_args) = run_mode_parser.parse_args()

     #
    #  Decide upon execution mode.
    ## --------------------------- 
    if not run_mode_options.debug_mode == '-':
        p_debug=True
    else:
        p_debug=False
    if p_debug:
        print('Debug mode is %s.' % run_mode_options.debug_mode)
        print('Operation is %s.' % run_mode_options.operation)
    if run_mode_options.mode == 'cli':
        if p_debug:
            print('Interactive mode.')
        if '-' == run_mode_options.operation:
            operation=None
            while operation not in operations:
                operation = input('Please specify some operation first:>')
        else:
            operation = run_mode_options.operation
    elif run_mode_options.mode == 'bat':
        if p_debug:
            print('Batch mode.')
    else:
        print("Usage: python cm.py [-d <on>] -m <bat|cli>")
        sys.exit(1)

    if 'dedupe' == operation:
        dl = [ 0, 1, 2, 1, 0, 0, 0, 1, 3, 5, 7, 4, 1 ]
        print('List with redundant items\t:%s.\nList deduplicated list\t\t:%s.' % (dl,dedupe(dl)))
    elif 'intersect' == operation:
        l1 = ['a','b','d']
        l2 = ['a','c','d']
        print('The intersection of list\t%s\nand list\t\t\t%s\nis\t\t\t%s.' % (l1, l2, intersect_lists(l1, l2)))
    elif 'extract' == operation:
        print('~~~~~ First demo ~~~~~')
        data_1_header = ['a','b','c','d']
        print('data_1_header : %s.' % data_1_header)
        data_1 = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]
        print('data_1 : %s.' % data_1)
        data_1_scope = ['a','d']
        print('data_1_scope : %s.' % data_1_scope)
        data_1_filter = { 'a': [ 0, 4 ], 'd': [ 3 ] }
        print('data_1_filter : %s.' % data_1_filter)
        data_1_extract, data_1_residu = extract_data(data_1
                                                 , data_1_header
                                                 , data_1_scope
                                                 , data_1_filter
                                                 , p_debug)
        print('data_1_extract : %s.' % data_1_extract)
        print('data_1_residu : %s.' % data_1_residu)
        print('~~~~~ Second demo ~~~~~')
        data_2_header = ['a','b','c','d','e']
        print('data_2_header : %s.' % data_2_header)
        data_2 = [[0,1,2,3,4],[0,5,6,7,0],[8,9,10,11,0],[0,0,0,3,0],[0,0,0,0,0],[1,0,0,3,0]]
        print('data_2 : %s' % data_2)
        data_2_scope = [ 'c', 'd', 'e' ]
        print('data_2_scope : %s.' % data_2_scope)
        data_2_filter = {'a':[0,8],'d':[3]}
        print('data_2_Filter : %s.' % data_2_filter)
        data_2_extract, data_2_residu = extract_data(data_2
                                                 , data_2_header
                                                 , data_2_scope
                                                 , data_2_filter
                                                 , p_debug)
        print('data_2_extract : %s.' % data_2_extract)
        print('data_2_residu : %s.' % data_2_residu)
        print('~~~~~ Third demo ~~~~~')
        data_3 = [['a',1,2,'com',4]
                  ,['b',5,6,'dev',0]
                  ,['c',9,10,'dev',0]
                  ,['d',0,0,'ops',0]
                  ,['e',0,0,'ops',0]
                  ,['f',0,0,'devops',0]]
        print('data_3 : %s' % data_3)
        data_3_header = [ 'team'
                          ,'rank'
                          ,'member_count'
                          ,'department'
                          ,'e']
        print('data_3_header : %s.' % data_3_header)
        data_3_scope = [ 'team', 'department' ]
        print('Interesting attributes : %s.' % data_3_scope)
        data_3_filter = { 'department' : ['dev','ops']
                          , 'e' : [0,4] }
        print('data_3_filter applied : %s.' % data_3_filter)
        data_3_extract, data_3_residu = extract_data(data_3
                                                 , data_3_header
                                                 , data_3_scope
                                                 , data_3_filter
                                                 , p_debug)
        print('data_3_extract : %s.' % data_3_extract)
        print('data_3_residu : %s.' % data_3_residu)
    elif 'list' == operation:
        my_list = [ [ 'a' ] , [ 'b' ] , [ 'a' ] , [ 'c' ] , [ 'a' ] ]
        print('my_list : %s.' % my_list)
        my_unlist = unlist(my_list)
        print('my_unlist : %s.' % my_unlist)
        my_deduped_list = dedupe(my_unlist)
        print('my_deduped_list : %s.' % my_deduped_list)
    else:
        print('Invalid operation specified.')
        sys.exit(1)

     #
    #  Exit gradefully.
    ## ----------------
    sys.exit(0)
