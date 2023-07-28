"""

@module: 
    hy_is.py

@author: 
    Erwin Geeraerts <erwin@rnig.be>

@maintainer : 
    Erwin Geeraerts

@backup-maintainer:
    <TODO prio=high>@team:who?</TODO>

@team: 
    <TODO/>

@original-creation-date: 
    Tue Oct 13 

@purpose: 
    Provide helper methods useful for user interaction.

"""

import hy_io
import hy_ds
import sys



def confirm_to_continue(p_question='', p_debug=False):
    choice = ''
    while 'c' != choice:
        print(p_question)
        choice = input('Press [c] to continue.')
    return choice

        
def ask_input(p_question='', p_debug=False):
    return input(p_question)
        

def confirmed(p_question='', p_debug=False):
    print(p_question)
    choice = 'zzz'
    confirmation = { 'y':True, 'j':True, 'n':False }
    while choice[:1].lower() not in [ 'y', 'n', 'j' ]:
        choice = input('Antwoord [j]a om t bevestigen of [n]ee om af te ontkennen.')
    return confirmation[choice[:1]]

        
def query_path(p_item='files'
               , p_question='Geef aub een geldig pad %s: >'
               , p_message_if_invalid='Excuus, dit is een ongeldig pad.\nProveer je even opnieuw ?'):
    path = None
    while not path:
        answer = input(p_question % p_item)
        if hy_io.path_exists(answer):
            path = answer
        else:
            print(p_message_if_invalid)
    return path


def get_attributes(p_item_attributes=[]
                   , p_question=''
                   , p_debug=False):
    if p_debug:
        print('Enter get_attributes.')
        print('p_item_attributes : %s.' % p_item_attributes)
        print('p_question : %s.' % p_question)
    attribute_list = []
    attr_choice = ''
    print('The item type has the following attributes :' )
    hy_ds.show_list(p_item_attributes)
    while 'q' != attr_choice.lower():
        attr_choice = str(input(p_question)).lower()
        if attr_choice in [a.lower().strip() for a in p_item_attributes]:
            attribute_list.append(attr_choice)
        else:
            print('Miss!')
    if p_debug:
        print('The following attributes are in scope :')
        hy_ds.show_list(attribute_list)
        print('Exit get_attributes.')
    return attribute_list    


def get_filter(p_item_attributes=[]
               , p_attributes_question=''
               , p_filter_question=''
               , p_debug=False):
    if p_debug:
        print('Enter get_filter.')
        print('p_item_attributes : %s.' % p_item_attributes)
        print('p_attributes_question : %s.' % p_attributes_question)
        print('p_filter_question        : %s.' % p_filter_question)
    attribute_list = get_attributes(p_item_attributes
                                    , p_attributes_question
                                    , p_debug=True)
    if p_debug:
        print('attribute_list : %s.' % attribute_list)
    attribute_filter = {}
    for filter_attribute in attribute_list:
        print('Specify one or more values for filter attribute %s :' % filter_attribute)
        filter_value_list = []
        filter_value_choice = ''
        while 'q' != filter_value_choice.lower():
            filter_value_choice = str(input(p_filter_question % filter_attribute)).lower()
            if 'q' != filter_value_choice:
                filter_value_list.append(filter_value_choice)
        attribute_filter[filter_attribute] = filter_value_list
    if p_debug:
        print('attribute_filter : %s.' % attribute_filter)
        for key in attribute_filter.keys():
            print('%s = %s.' % (key, attribute_filter[key]))
        print('Exit get_filter.')
    return attribute_filter


