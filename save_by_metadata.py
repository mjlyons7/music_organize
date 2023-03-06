# This program takes a mp3, or mp4 (m4a) file as a command line argument
# extracts the metadata song name, artist, and album
# if this metadata found, renames the file to the song name, moves it to directory artist/album, under an optional main music folder
# currently designed to run on a hardrive formatted in ex-fat. Replaces restricted characters with underscores

# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND

import sys
import pathlib
from mutagen import mp3, mp4, flac

#fat32 invalid characters
fat32_bad_chars = "?<>\\:*|/\""
is_fat32 = True

# TODO: add FLAC to this list
supported_file_types = ["mp3","m4a","wav","flac"]
path_to_new_music = ["new"]

#file type error
class FileExtensionError(Exception):
    def __init__(self,message):
        self.message = message

#getting tags from mp3 file
def get_mp3_tags(file_name):
    m_handle = mp3.EasyMP3(file_name)

    song = m_handle.tags['title'][0]
    artist = m_handle.tags['artist'][0]
    album = m_handle.tags['album'][0]
    
    return (song,artist,album)


#getting tags from mp4 file
def get_mp4_tags(file_name):
    m_handle = mp4.MP4(file_name)
    
    #song, artist, album
    song = m_handle.tags['©nam'][0]
    artist = m_handle.tags['©ART'][0]
    album = m_handle.tags['©alb'][0]
    
    return (song,artist,album)

def get_flac_tags(file_name):

    m_handle = flac.FLAC(file_name)

    #song, artist, album
    song =  m_handle.tags['title'][0]
    artist = m_handle.tags['artist'][0]
    album = m_handle.tags['album'][0]


    return (song, artist, album)

#getting mp3 or mp4 tags
def get_tags(file_name,file_type):
    
    #determine if mp3 or mp4 (m4a) by extension
    if file_type == "mp3":
        return get_mp3_tags(file_name)
    
    elif file_type == "m4a":
        return get_mp4_tags(file_name)
        
    elif file_type == "wav":
        raise FileExtensionError(file_type+" is not tagged")

    elif file_type == "flac":
        return get_flac_tags(file_name)
    else:
        raise FileExtensionError(file_type+" not recognized")
    
    return
        
        
#capitalize tokenized sentence, return
def capitalize_tokens(my_str):
    my_str_list = my_str.split()
    new_str = ""
    for word in my_str_list:
        #if word is all caps leave it alone
        if word.upper() == word:
            new_str += word + " "
        else:
            new_str += word.capitalize() + " "
    #remove extra last space
    new_str = new_str[:-1]
    
    return new_str
    
    
#clean up names, to remove special characters, capitalize, etc
def clean_name(dirty_word,bad_chars):
    
    #replace slashes with dashes
    clean_word = dirty_word.replace("/"," - ")
    
    #replace other bad chars with underscore
    for char in bad_chars:
        clean_word = clean_word.replace(char,'_')
    
    #convert album and artist to capitalized versions, to standardize folder names
    clean_word = capitalize_tokens(clean_word)
        
    return clean_word
        
#saving the file, based on song, artist, album
def save_new_file(current_file_name,new_name,path_directories,file_type):

    #create new path directories for album and artist, if not already defined
    new_path_str = ""
    for next_dir in path_directories:
        new_path_str += next_dir + "/"
        path_obj = pathlib.Path(new_path_str)
        if not path_obj.exists():
            path_obj.mkdir(mode = 0o775)
        
    #save song with new file name
    song_path = pathlib.Path(current_file_name)
    song_path.rename(new_path_str + new_name + "." + file_type)
    
    return

def main(argv):
    ######## get file name and type ###########

    #if no spaces in filename, save to file_name string
    if len(argv) == 2:
        file_name = argv[1]
    
    #if spaces in file name, gets treated as multiple sys arguments, so combine sys arguments into 1 string
    elif(len(argv)) > 2:
        file_name = ""
        for i in range(1,len(argv)):
            file_name += argv[i] + ' '
        file_name = file_name[:-1] # remove final space
    else:
        print("Please pass the filename as a command line argument")
        print("System arguments:",str(argv[1:]))
        return
        
    # test existence of file
    song_path = pathlib.Path(file_name)
    if not song_path.exists():
        raise FileNotFoundError(file_name)
        return
    
    #get file type and check if supported
    file_type = file_name.split('.')[-1]
    if not (file_type in supported_file_types):
        print(argv)
        raise Exception("Unsupported file type: "+file_name)
        
    ############## get tags #############
    try:
        song,artist,album = get_tags(file_name,file_type)
    except KeyError:
        print('********',file_name,"missing",sys.exc_info()[1],'********')
        song = artist = album = None
        
    except FileExtensionError:
        print('********',file_name, sys.exc_info()[1],'********')
        song = artist = album = None
    
    #clean up names, removing restricted fat32 characters, if found metadata
    if song != None and is_fat32:
        
        song = clean_name(song,fat32_bad_chars)
        artist = clean_name(artist,fat32_bad_chars)
        album = clean_name(album,fat32_bad_chars)
    
    #save to new directory with name matching song, or save to unknown if tags not found
    if song == None:
        name_no_extension = file_name.split("/")[-1][:-(len(file_type)+1)]
        save_new_file(file_name,name_no_extension,["missing_tags"],file_type)
    else:
        save_new_file(file_name,song,path_to_new_music+[artist,album],file_type)


if __name__ == "__main__":
    main(sys.argv)
