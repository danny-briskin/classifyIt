import logging
import cairosvg
import requests
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
    cairosvg.svg2png(file_obj=open(folder_name + svg_filename, "rb"),
                     write_to=folder_name + file_name + '.png', unsafe=True)


def download_image(image_url: str, download_directory: str) -> None:
    """
    Download image from given URL. If image format is SVG, converts it PNG
    :param image_url: url
    :param download_directory: directory to save images
    :return:
    """
    first_pos = image_url.rfind("/")
    last_pos = len(image_url)
    image_file_name = image_url[first_pos + 1:last_pos]
    logging.info('Downloading and processing [' + image_url + ']')
    request = requests.get(image_url, allow_redirects=True)
    image_file_name_full = download_directory + image_file_name
    open(image_file_name_full, 'wb').write(request.content)
    if image_url.endswith('.svg'):
        convert_svg_to_png(image_file_name, download_directory)
