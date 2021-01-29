def get_image_url_from_attributes(image):
    """
      Retrieves image (&lt;img&gt; tag) source URL.
      Analyzes src, srcset and data-lazy-srcUrl attributes

    :param image: image selenium element of img
    :return: url string
    """
    src_url = ""
    # try with srcset attribute for 1x or first available
    # TODO consider sorting by width desc
    src_set = image.get_attribute("srcset")
    if src_set != "":
        src_set_arr = src_set.split(",")
        if not src_set_arr:
            src_candidate = src_set_arr[0].split(" ")[0]
            for src_set_item in src_set_arr:
                if " 1x" in src_set_item:
                    first_src_in_set = src_set_item.split(" ")[0]
                    if first_src_in_set != "":
                        src_url = first_src_in_set
                    else:
                        src_url = src_candidate
    # if not found, let's try with regular src
    if src_url == "" or not src_url.startswith('http'):
        src_url = image.get_attribute("src")

    # the last chance - try with data-lazy-srcUrl (comes from WPRocket optimization)
    if src_url == "" or not src_url.startswith('http'):
        src_url = image.get_attribute("data-lazy-src")
    return src_url
