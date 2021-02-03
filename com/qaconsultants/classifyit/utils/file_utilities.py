import os
import shutil
from pathlib import Path


def clean_folder(folder):
    """
    Cleans a folder
    :param folder:  path to folder
    :return:
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def find_images_in_folder(folder, list_of_extensions):
    return list(Path(folder).rglob(list_of_extensions))


def replace_text_in_file(infile, outfile, delete_list):
    with open(infile) as fin, open(outfile, "w+") as fout:
        for line in fin:
            for word in delete_list:
                line = line.replace(word[0], word[1])
            fout.write(line)
    os.rename(outfile, infile)
