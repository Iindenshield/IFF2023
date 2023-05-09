from os import *
import os, sys
from os.path import *
import re
import shutil
from PIL import Image

#folder format: FILM NAME IMG

#file format: IFF23_[NomeFilm]_##(opz)_data(opz)_[NomeFile]_[dimensioni]_[lingua]

edition = 'IFF2023'

def get_image_size(image_path):
    img = Image.open(image_path)
    return str(img.width), str(img.height)


def get_file_list(directory_path):
    file_list = [file for file in listdir(directory_path) if isfile(join(directory_path, file))]
    return file_list

def create_backup_folder(dir_path):
    destination_dir = dir_path + '_backup'
    shutil.copytree(dir_path, destination_dir)
    print('\n --- DIR CONTENT --- \n')
    for content in os.listdir(dir_path):
        if 'info.txt' in content:
            continue
        print(content)
    print('\n --- END OF DIR CONTENT --- \n')
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        try:
            shutil.rmtree(file_path)
        except OSError:
            os.remove(file_path)
    return destination_dir

def camel_case(film_dir):
    film = ''
    word_list = film_dir.split(' ')
    for word in word_list:
        film += word[0].upper() + word[1:].lower()
    return film
    
def main():
    path = input("Enter the main directory path: ")
    #output: C:\Users\lindenshield\Desktop\THE SPARROW
    film = camel_case(path.split('\\')[-1])
    #output: TheSparrow
    img_ext = ".png.psd.jpg.tif"
    doc_ext = ".pdf.doc.docx.txt"
    backup_dir = create_backup_folder(path)
    for file in os.listdir(backup_dir):
        size = ''
        lang = ''
        #output: Headshot ff609cde94-headshot.jpg
        if 'info.txt' in file:
            continue
        ext = file.split('.')[-1]
        #se il file è un immagine:
        if ext in img_ext:
            img_path = backup_dir + '\\' + file
            #output: img_path = C:\Users\lindenshield\Desktop\UNIVERSAL_backup\Headshot ff609cde94-headshot.jpg
            width = get_image_size(img_path)[0]
            height = get_image_size(img_path)[1]
            size = '_' + width + 'x' + height
        description = input("Enter description for the file: ")
        if ext in doc_ext:
            lang = '_' + input("Enter doc language (es. ITA, ENG): ")
        new_name = edition + '_' + film + '_' + description + size + lang + '.' + ext
        new_path = path + '\\' + new_name
        old_path = backup_dir + '\\' + file
        os.rename(old_path, new_path)
    if input('Delete backup folder ' + backup_dir + '? Y/N ').upper() == 'Y':
        try:
            shutil.rmtree(backup_dir)
        except OSError:
            os.remove(backup_dir)
        print('Backup folder deleted successfully')
    else:
        print('Please delete backup folder if the material was sorted correctly')

    
if __name__ == '__main__':
    main() 
