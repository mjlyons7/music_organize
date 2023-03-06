# manager to retrieve files in local directory, and pass to save_by_metadata

import os
import save_by_metadata as sbm

def main():

    # get list of supported files, pass to sbm
    supported_file_types = sbm.supported_file_types
    
    # TODO: if filename has & symbol in it, does not get passed correctly
    for filename in os.listdir(os.getcwd()):
        if filename.split('.')[-1] in supported_file_types:
            os.system("python save_by_metadata.py "+filename)
    return

if __name__ == "__main__":
    main()