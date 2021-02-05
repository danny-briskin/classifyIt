import logging
import torch
from PIL import Image
from com.qaconsultants.classifyit.clip_processing import module_clip
from com.qaconsultants.classifyit.utils.string_utilities import spring_splitter_by_chunks, \
    select_maximum_value_in_list_of_tuples

global image, device, model, preprocess, probs, text, related_categories_dict, split_categories_numbers

# TODO remove the file !
def format_categories(_initial_categories_list, split_words_number=60, tokenizer_number=70):
    global text, related_categories_dict, split_categories_numbers
    _categories_list = []
    split_categories_list = []
    logging.info('Text(s) list length [' + str(len(_initial_categories_list)) + ']')
    logging.info('Splitting initial text by [' + str(split_words_number) + '] words')

    # preliminary split by words, to not overflow tokenize_attempt
    added_cat_counter = 0
    for _p_index, _p_initial_category in enumerate(_initial_categories_list):
        _p_split_list = spring_splitter_by_chunks(split_words_number - 1, _p_initial_category)
        split_categories_list.extend(_p_split_list)
        split_length = len(_p_split_list)
        if split_length > 1:
            split_categories_numbers.append(_p_index)
            related_categories_dict[_p_index] = list(
                [x for x in
                 range(_p_index + added_cat_counter, _p_index + added_cat_counter + split_length)])
            added_cat_counter += split_length - 1
        else:
            related_categories_dict[_p_index] = [_p_index + added_cat_counter]

        logging.info('Chunking text again if some part of its [' + str(len(split_categories_list))
                     + '] preliminary chunks is not fit by tokenizers\' limit of ['
                     + str(tokenizer_number) + ']')

        for _index, initial_category in enumerate(split_categories_list):
            if module_clip.tokenize_attempt(initial_category) >= tokenizer_number:
                split_list = spring_splitter_by_chunks(split_words_number - 1, initial_category)
                _categories_list.extend(split_list)
                split_length = len(split_list)
                if split_length > 1:
                    split_categories_numbers.append(_p_index)
                    related_categories_dict[_p_index].extend(list(
                        [x for x in
                         range(_index + added_cat_counter,
                               _p_index + added_cat_counter + split_length)]))
                    added_cat_counter += split_length - 1
                else:
                    related_categories_dict[_p_index].extend([_index + added_cat_counter])
            else:
                _categories_list.append(initial_category)

    logging.info('Text split by [' + str(len(_categories_list)) + '] chunks')
    text = module_clip.tokenize(_categories_list).to(device)


def get_replacement_category_index(current_index):
    global related_categories_dict
    for key, value in related_categories_dict.items():
        for value_item in value:
            if value_item == current_index:
                return key
    return current_index





def init():
    global split_categories_numbers
    split_categories_numbers = []


def load_model():
    global device, model, preprocess, related_categories_dict
    related_categories_dict = {}
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = module_clip.load("ViT-B/32", device=device)


def load_image(image_path):
    global image, device
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)


def clean():
    global image, probs
    try:
        del image
    except NameError:
        pass
    try:
        del probs
    except NameError:
        pass
    init()


def load_categories():
    global image, device, probs, text

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()


def process_probabilities(initial_categories_list):
    global probs
    real_cat_probs = []
    for index in range(len(probs[0])):
        replacement_category_index = get_replacement_category_index(index)
        real_cat_probs.append((replacement_category_index, probs[0][index]))
    res = select_maximum_value_in_list_of_tuples(real_cat_probs)

    for index in range(len(res)):
        log_str = "{:<26}".format(
            initial_categories_list[index][:40].replace("\n", "") + ' <...> '
            + initial_categories_list[index][-20:].replace("\n", "")) + " : " + "{:.2%}" \
                      .format(res[index][1])
        logging.info(log_str)
