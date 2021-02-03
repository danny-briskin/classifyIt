from pathlib import Path

import cairosvg

from com.qaconsultants.classifyit.utils.file_utilities import replace_text_in_file


def convert_svg_to_png(svg_filename, folder_name):
    first_pos = svg_filename.rfind(".")
    file_name = svg_filename[0:first_pos]
    delete_list = [
        (
        "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\" ["
        ,
        "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\" ")
        , ("<!ENTITY ns_flows \"http://ns.adobe.com/Flows/1.0/\">", "")
        , ("]>", ">")]

    replace_text_in_file(folder_name + svg_filename, folder_name + 'outfile.tmp', delete_list)
    cairosvg.svg2png(file_obj=open(folder_name+svg_filename, "rb"),
                     write_to=folder_name + file_name + '.png', unsafe=True)
