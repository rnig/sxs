"""

This  module unifies  several functions  related to  file &  directory
processing.

"""

import csv
import datetime
import fnmatch
import glob
import hashlib
import os
import platform
import pprint
import shutil
import sys



def where_am_i(p_debug=False):
    """

    Show the current directory where processing will happen.

    """
    current_directory = os.getcwd()
    if p_debug:
        print('Enter hfs.where_am_i.')
        print('Current directory : %s.' % current_directory)
        print('Exit hfs.where_am_i.')
    return current_directory


def get_base_dir(p_file_path=None):
    """
    
    Return the directory part of a full file path.

    """
    return str(os.path.dirname(p_file_path))


def get_file_name(p_file_path):
    """
    
    Return the file name part of a full file path.

    """
    return str(os.path.basename(p_file_path))


def get_current_directory():
    """

    Return the current working directory.

    """
    return str(os.getcwd())


def get_path(p_path_parts=[ 'tmp', 'test', 'file.txt' ]
             , p_platform=None
             , p_absolute=False
             , p_debug=False):
    """
    Return either a relative or absolute  path based in the path parts
    given in p_path_parts.
    """
    return_path = None
    separator = os.sep
    platforms = [ 'windows', 'unix' ]
    if p_debug:
        print('platform:', platform.platform())
        print('os path separator:', separator)
        print('known platforms:', ', '.join(platforms))
    if p_platform:
        if p_debug:
            print('p_platform:', p_platform)
        if p_platform.lower() in platforms:
            windows_specifics = { 'path_separator':'\\', 'root':'C:' }
            unix_specifics = { 'path_separator':'/', 'root':'/' } 
            platform_specifics = { 'WINDOWS':windows_specifics, 'UNIX':unix_specifics } 
            root = platform_specifics[p_platform]['root']
            separator = platform_specifics[p_platform]['path_separator']
            if p_debug:
                print('p_platform is a known platform.')
                print('windows_specifics:', windows_specifics)
                print('unix_specifics:', unix_specifics)
                print('platform_specifics:', platform_specifics)
                print('root:', root)
                print('separator:', separator)
    if p_absolute:
        part_list = [ root, separator ] + p_path_parts
    else:
        part_list = p_path_parts
    if p_debug:
        print('part_list:', part_list)
    return_path = separator.join([ part.replace('/',separator) for part in part_list ])
    return return_path
    

def path_exists(p_path=None):
    """

    Check if a path exists.

    """
    result = False
    if os.path.exists(p_path):
        print('%s exists.' % p_path)
        result = True
    else:
        print('%s is non existant.' % p_path)
    return result


def list_directory(p_path='.'
                   , p_pattern='*'
                   , p_debug=False):
    if path_exists(p_path):
        return glob.glob(os.path.join(p_path, p_pattern))
    return None

    
def create(p_dir='tmp', p_debug=False):
    if p_debug:
        print('Enter hfs.create.')
        print('p_dir: %s .' % p_dir)
    if os.path.exists(p_dir):
        if p_debug:
            print('Directory %s exists already.' % p_dir)
    else:
        if p_debug:
            print('Directory %s does not exist yet, creating...' % p_dir)
        os.makedirs(p_dir)
        if p_debug:
            print('... Done.')
    if p_debug:
        print('Exit hfs.create.')


def load(p_file_path='tmp/tmp.txt', p_debug=False):
    if p_debug:
        print('Loading %s.' % p_file_path)
    r_data = []
    fo = open(p_file_path, 'r', encoding='unicode_escape')
    try:
        r_data = fo.readlines()
    finally:
        fo.close()
    return r_data


def load_inventory(p_path, p_debug=False):
    if p_debug:
        print('Enter load_inventory.')
        print('p_path:%s.' % p_path)
    dataset = []
    consistent = False
    candidate_separators = [ '|', ';', ',' ]
    while True:
        while candidate_separators and not consistent:
            if p_debug:
                print('The following separator candidates are left to try %s.' % candidate_separators)
            cs = candidate_separators.pop()
            if p_debug:
                print('Print trying to separate fields using "%s".' % cs)
            f = open(p_path, 'r')
            reader = csv.reader(f
                                , delimiter=cs
                                , dialect='excel')
            candidate_dataset = []
            actual_row_length = -1
            rc = 1
            for row in reader:
                rc += 1
                if not len(row) > 1:
                    if p_debug:
                        print('The number of fields is %d in row %s,\nhence the candidate separator "%s" fails to separate fields.' % (len(row),row,cs))
                    break
                if p_debug:
                    print('Row %s has %d fields.' % (row,len(row)))
                if -1 == actual_row_length:
                    actual_row_length = len(row)
                    if p_debug:
                        print('Setting row length to %d.' % len(row))
                if len(row) != actual_row_length:
                    if p_debug:
                        print('The number of fields in row %s with number %d, seems inconsistent.' % (row,rc))
                    consistent = False
                    break
                else:
                    consistent = True
                    candidate_dataset.append([ f.strip() for f in row])
        break
    dataset = candidate_dataset
    if p_debug:
        print('Exit load_inventory.')
        print('dataset:%s.' % dataset)
    if consistent:
        return dataset
    return None


def mini_store(p_data=[ 'a', 'b', 'c' ], p_file_path='tmp/tmp.txt', p_append=False, p_binary=False, p_debug=False):
    rc = False
    write_mode = 'w'
    if p_append:
        if p_debug:
            print('Appending.')
        write_mode = 'a'
    if p_binary:
        print('Writing binary.')
        write_mode += 'b'
    with open(p_file_path, write_mode , encoding='utf-8') as fo:
        for i in p_data:
            fo.write(i)
        rc = True
    return rc    


def store(p_data=[[ 'a', 'b', 'c' ],[ 'd', 'e', 'f' ],[ 'g', 'h', 'i' ]], p_file_path='tmp/tmp.txt', p_separator=',', p_append=False, p_binary=False, p_debug=False):
    rc = False
    write_mode = 'w'
    if p_append:
        write_mode = 'a'
    if p_binary:
        print('Writing binary.')
        write_mode += 'b'
    fo = open(p_file_path, write_mode)
    try:
        for d in p_data:
            line = p_separator.join([str(s).strip() for s in d])+'\n'
            if p_debug:
                print(line)
            fo.write(line)
    finally:
        fo.close()
        rc = True
    return rc    


def remove(p_path='tmp/tmp.txt', p_debug=False):
    rc = False
    if p_debug:
        print('%s will be removed.' % p_path)
    try:
        os.remove(p_path)
        rc = True
    except Exception as e:
        print ('Exception %s occurred.' % e)
    return rc


def stream(p_file_path='tmp/tmp.txt', p_chunksize=100, p_debug=False):
    """
    Large files might better be treated differently.

    This stream method can be called like so : 

        for chunk in stream('/path/to/large/file'):
            do_something_with(chunk)
    """
    fo = open(p_file_path, 'rb')
    try:
        while True:
            chunk = fo.read(p_chunksize)
            if not chunk:
                break
            # do processing on chunk
            yield chunk
    finally:
        fo.close()


def md5_file(p_name='tmp/tmp.txt'):
    hash_md5 = hashlib.md5()
    try:
        with open(p_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as e:
        print ('Exception %s occurred.' % e)
    return hash_md5.hexdigest()

        
def replicate_file(p_file, p_target='bkp', p_descend=False):
    fn = get_file_name(p_file)
    target_file = os.path.join(p_target,fn)
    file_exists_at_target = False
    tfp = [] # Potentially empty list of files found at target with same filename.
    if p_descend:
        tfp = search_file(p_target, fn)
        if tfp:
            file_exists_at_target = True
    else:
        if os.path.exists(target_file):
            file_exists_at_target = True
    if not file_exists_at_target:
        print("Copy to %s ." % target_file)
        shutil.copy(p_file,target_file)
        if md5_file(p_file) == md5_file(target_file):
            return (False,True,True) # Not pre-existing, Copied, Same.
        else:
            return (False,True,False) # Not pre-existing, Copied, Different.
    else:
        print("File %s exists already on %s." % (p_file,p_target))
        file_content_match = False
        if p_descend:
            for tf in tfp:
                if md5_file(p_file) == md5_file(tf):
                    file_content_match = True
                else:
                    print("source %s : %s." % (p_file, md5_file(p_file)))
                    print("target %s : %s." % (tf, md5_file(target_file)))
        elif md5_file(p_file) == md5_file(target_file):
            file_content_match = True
        else:
            print("source %s : %s." % (p_file, md5_file(p_file)))
            print("target %s : %s." % (target_file, md5_file(target_file)))
        if file_content_match:
            return (True,False,True) # Pre-existing, Not copied, Same.
        else:
            print("But their content is different, please checkt that first.")
            return (True,False,False) # Pre-existing, Not copied, Different.
        

        
def replicate_files(p_source, dir_list=[], p_target='bkp', space_count=0, p_debug=False):
    for file in dir_list:
        print("/".rjust(space_count+1) + file)
        source_file = os.path.join(p_source,file)
        target_file = os.path.join(p_target,file)
        if not os.path.exists(target_file):
            print("Copying %s to %s ." % (source_file,p_target))
            shutil.copy(source_file,target_file)
        else:
            if p_debug:
                print("File %s is already existing at target %s." % (file,p_target))
            source_md5 = md5_file(source_file)
            target_md5 = md5_file(target_file)
            if source_md5 == target_md5:
                if p_debug:
                    print("The md5 checksum is equal hence no further action required as the same content is already replicated.")
            else:
                print("Different md5 checksum, hence different content.")
                replica_timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
                versioned_replica = target_file + '.' + replica_timestamp
                print("Moving the existing replica %s to a versioned replica %s ." % (target_file,versioned_replica))
                shutil.move(target_file,versioned_replica)
                print("Replicating source file %s to replica %s ." % (source_file,target_file))
                shutil.copy(source_file,target_file)                

        
def replicate_directory(dir_entry, p_target='bkp'):
    print("Replicating directory %s ." % dir_entry[0] + "/")
    if not os.path.exists(p_target):
        create(p_target)
    else:
        print("Copy target is already existing.")
    replicate_files(dir_entry[0], dir_entry[2], p_target, len(dir_entry[0]))


def replicate(p_source='tmp',p_target='bkp',p_debug=True):
    if os.path.exists(p_source):
        if os.path.exists(p_target):
            source_base = get_base_dir(p_source)
            source_leaf = get_file_name(p_source)
            target_base = get_base_dir(p_target)
            target_leaf = get_file_name(p_target)
            replica = os.path.join(target_base,source_leaf)
            if p_debug:
                print("Source stem : %s." % source_base)
                print("Source leaf : %s." % source_leaf)
                print("Target stem : %s." % target_base)
                print("Target leaf : %s." % target_leaf)
                print("Replicating source %s to %s." % (p_source,replica))
            if os.path.exists(replica):
                if p_debug:
                    print("Replica is already existing.")
                if os.path.isfile(p_source):
                    print("Replicating file %s ." % p_source)
                    #replicate_file(p_source,p_target)
                else:
                    print("Replicating directory %s ." % p_source)
                    # tree = os.walk(p_source)
                    # for directory in tree:
                    #     replicate_directory(directory,p_target)
            else:
                if p_debug:
                    print("Replica is not yet existing.")
                if os.path.isfile(p_source):
                    print("Replicating file %s ." % p_source)
                    shutil.copyfile(p_source,replica)
                else:
                    print("Replicating directory %s ." % p_source)
                    shutil.copytree(p_source,replica)
    else:
        print("Non existing source path, nothing to replicate.")

        
def backup(p_file_path='tmp/tmp.txt', p_timestamp=None, p_backup_location=None, p_debug=True):
    if p_debug:
        print('p_file_path:', p_file_path)
        print('p_timestamp:' , p_timestamp)
        print('p_backup_location:', p_backup_location)
    if os.path.exists(p_file_path) and os.path.isfile(p_file_path):
        if p_debug:
            print(p_file_path, 'exists and is a file.')
        if not p_timestamp:
            p_timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        fn_parts = get_file_name(p_file_path).split('.')
        backup_fn = '.'.join([ fn_parts[0], p_timestamp, fn_parts[-1] ])
        if not p_backup_location:
            p_file_path_bkp = get_path([get_base_dir(p_file_path),backup_fn])
        else:
            p_file_path_bkp = get_path([p_backup_location,backup_fn])
        if p_debug:
            print('p_timestamp:' , p_timestamp)
            print('fn_parts:', fn_parts)
            print('backup_fn:', backup_fn)
            print('p_file_path_bkp:', p_file_path_bkp)
        if os.path.exists(p_file_path_bkp):
            p_file_path_rev = p_file_path + '.revert'
            if p_debug:
                print(p_file_path_bkp, "exists already, providing a '.revert'-file,", p_file_path_rev)
            shutil.copy(p_file_path_bkp,p_file_path_rev)
            # TODO: make copies read only
        shutil.copy(p_file_path,p_file_path_bkp)
        if p_debug:
            print('Backed up to %s.' % p_file_path_bkp)


def search_file(dir_path='tmp', file_name_pattern='tmp.txt', p_debug=False):
    allsizes = []
    for (thisDir, subsHere, filesHere) in os.walk(dir_path):
        if p_debug: logger(thisDir)
        for file_name in filesHere:
            if fnmatch.fnmatch(file_name, file_name_pattern):
                if p_debug: print('...', file_name_pattern)
                fullname = os.path.join(thisDir, file_name)
                allsizes.append(fullname)
    if 0 < len(allsizes):
        allsizes.sort()
    return allsizes


def crawl_file(aToken, aFile):
    print('Searching %s in %s.' % (aToken, aFile))
    hit_rows = []
    file_obj = open(aFile)
    for row in file_obj:
        if aToken.lower() in str(row).lower():
            hit_rows.append(row)
    file_obj.close()
    return hit_rows


def print_files(dirEntry, dirList, spaceCount):
    for file in dirList:
        print("/".rjust(spaceCount+1) + file)
        #aList = crawl_file(grep_token, os.path.join(dirEntry,file))
        #print("Hitted lines : %s." % aList)

        
def print_directory(dirEntry):
    print(dirEntry[0] + "/")
    printFiles(dirEntry[0], dirEntry[2], len(dirEntry[0]))


def logger(p_message, p_args='NIL'):
    if sys.version_info[0] < 3:
        import hps2
        hps2.hprint(p_message,p_args)
    else:
        import hps3
        hps3.hprint(p_message,p_args)

    
def diagnostic():
    logger('Starting a diagnostic (%s).')
    debug = True
    create(p_debug=debug)
    store(p_debug=debug)
    store(p_file_path='tmp/tmp.bin', p_binary=True, p_debug=debug)
    data = load(p_file_path='tmp/tmp.bin', p_debug=debug)
    if data:
        pprint.pprint(data)
    else:
        logger('Failed.%s')
    store(p_data=[ 'a\n','b\n','c\n' ], p_append=True, p_debug=debug)
    data = load(p_debug=debug)
    if data:
        pprint.pprint(data)
    else:
        logger('Failed.')
    store(p_data='a\nb\nc\n', p_append=True, p_debug=debug)
    data = load(p_debug=debug)
    if data:
        pprint.pprint(data)
    else:
        logger('Failed.')
    mini_store(p_data='a\nb\nc\n', p_append=True, p_debug=debug)
    data = load(p_debug=debug)
    if data:
        pprint.pprint(data)
    else:
        logger('Failed.%s')
    backup(p_debug=debug)
    for chunk in stream():
        logger('Streaming %s.',chunk)
    rc, data = search()
    if rc:
        pprint.pprint(data)
    else:
        logger('Failed.%s')
    remove(p_debug=debug)
    rc, data = search()
    if rc:
        pprint.pprint(data)
    else:
        logger('Failed.%s')
    logger('Stopping a diagnostic.%s')

        
    
if __name__ == '__main__':
    diagnostic()
