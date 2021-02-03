import csv
import logging

import torch
import pandas as pd
from PIL import Image
from numpy import loadtxt

from com.qaconsultants.classifyit.clip_processing import module_clip

global image, device, model, preprocess, probs

split_categories_numbers = []
related_categories_dict = {}
real_cat_probs = []


def splitter(n, s):
    pieces = s.split()
    return list((" ".join(pieces[i:i + n]) for i in range(0, len(pieces), n)))


def format_categories(_initial_categories_list, split_number=60):
    _categories_list = []
    added_cat_counter = 0
    for _index, initial_category in enumerate(_initial_categories_list):
        if module_clip.tokenize_attempt(initial_category) >= split_number:
            split_list = splitter(split_number - 1, initial_category)
            _categories_list.extend(split_list)
            split_length = len(split_list)
            if split_length > 1:
                split_categories_numbers.append(_index)
                related_categories_dict[_index] = list(
                    [x for x in
                     range(_index + added_cat_counter, _index + added_cat_counter + split_length)])
                added_cat_counter += split_length - 1
            else:
                related_categories_dict[_index] = [_index + added_cat_counter]
        else:
            _categories_list.append(initial_category)
            related_categories_dict[_index] = [_index + added_cat_counter]

    return _categories_list


def get_replacement_category_index(current_index):
    for key, value in related_categories_dict.items():
        for value_item in value:
            if value_item == current_index:
                return key
    return current_index


def group_list(lst):
    tup = {i: 0 for i, v in lst}
    for key, value in lst:
        if value >= tup[key]:
            tup[key] = value
        # using map
    return list(map(tuple, tup.items()))


def load_model():
    global device, model, preprocess
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = module_clip.load("ViT-B/32", device=device)


def load_image(image_path):
    global image, device
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)


def load_categories(initial_categories_list, split_words_number=60):
    global image, device, probs
    categories_list = format_categories(initial_categories_list, split_words_number)

    text = module_clip.tokenize(categories_list).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()


def process_probabilities(initial_categories_list):
    global probs
    for index in range(len(probs[0])):
        replacement_category_index = get_replacement_category_index(index)
        real_cat_probs.append((replacement_category_index, probs[0][index]))

    res = group_list(real_cat_probs)

    for index in range(len(res)):
        log_str="{:<26}".format(initial_categories_list[index]) + " : " + "{:.2%}".format(
            res[index][1])
        # print(log_str)
        logging.info(log_str)
