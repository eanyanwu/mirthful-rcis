import os
import glob
import time
import build

# Helper method for recording the updated time for all the files
# specified by the patterns
def get_file_dict(patterns):
    file_list = []
    file_dict = {}

    [  
        file_list.extend(glob.glob(pattern, recursive=True)) 
        for pattern in patterns 
    ]

    [ 
        file_dict.setdefault(f, os.stat(f).st_mtime) 
        for f in file_list 
    ]

    return file_dict


files = {}

patterns_to_watch = [
    './html/**/*.*',
    './css/**/*.*',
    './js/**/*.*'
]

files = get_file_dict(patterns_to_watch)


while True:
    time.sleep(1)

    # Get the new file dict
    new_files = get_file_dict(patterns_to_watch)
    
    # First check to see if the file list has changed
    deleted_files = files.keys() - new_files.keys() 
    created_files = new_files.keys() - files.keys() 


    if len(deleted_files) > 0 or len(created_files) > 0:
        if len(deleted_files) > 0:
            print("Deleted File(s)...", deleted_files) 

        if len(created_files) > 0:
            print("Created File(s)...", created_files)

        build.apply_templates()

        # Since the file list changed, update it
        files = new_files

        continue

    # If there are no deleted/created files, then:
    # Check to see if any of the existing files has been modified since
    # the last time

    for key in new_files.keys():
        new_mtime = new_files[key]
        old_mtime = files[key]

        if new_mtime != old_mtime:
            # The file was modified 
            print("Modified file {}...".format(key))

            build.apply_templates()

            # Since some files were updated, update the file dict
            files = new_files

            continue
