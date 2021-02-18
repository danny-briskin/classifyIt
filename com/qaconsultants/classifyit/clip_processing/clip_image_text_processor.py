import logging
from typing import List

import torch
import typing
from PIL import Image

from com.qaconsultants.classifyit.clip_processing import module_clip
from com.qaconsultants.classifyit.exceptions.error_exceptions import InvalidParameter
from com.qaconsultants.classifyit.utils.string_utilities import spring_splitter_by_chunks, \
    select_maximum_value_in_list_of_tuples


class ClipImageTextProcessor:
    """
    CLIP Image Text Processor

     Attributes
    ----------

    image_holder : ImageHolder
        an image holder
    """

    def __init__(self) -> None:
        super().__init__()

        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._split_categories_numbers = []
        self.image_holder = self.ImageHolder(self)
        self._model = None
        self._preprocess = None
        self._text = None
        self._related_categories_dict = None

    def calculate_probabilities(self) -> None:
        """
        Calculates probability that the text has the same class as the image.
        self.image_holder.image and self.text must be set. Fills self.probabilities list
        """
        with torch.no_grad():
            _image_features = self._model.encode_image(self.image_holder.image)
            _text_features = self._model.encode_text(self._text)

            _logits_per_image, _logits_per_text = self._model(self.image_holder.image, self._text)
            self.image_holder.probabilities = _logits_per_image.softmax(dim=-1).cpu().numpy()

    def get_replacement_category_index(self, current_index) -> int:
        """
        If initial category was split by several chunks, it will be represented byt several category
        numbers. Use this method in order to get probability of initial category number.
        Uses self.related_categories_dict
        :param current_index: index(number) of category probability to map with real number.
        :return: real category number
        """
        for key, value in self._related_categories_dict.items():
            for value_item in value:
                if value_item == current_index:
                    return key
        return current_index

    def load_model(self) -> None:
        """
        Loads CLIP model. Clears self.related_categories_dict
        """
        self._related_categories_dict = {}
        self._model, self._preprocess = module_clip.load("ViT-B/32", device=self._device)

    def load_image(self, image_path: str):
        """
        Loads and preprocess image from given path
        :param image_path: path to the image
        :return image
        """
        try:
            _loaded_image = Image.open(image_path)
        except Exception as e:
            logging.exception('Error at %s', image_path, exc_info=e)
            raise InvalidParameter('Given image could not be processed')
        else:
            return self._preprocess(_loaded_image).unsqueeze(0).to(self._device)

    def reset_split_categories_numbers(self):
        self._split_categories_numbers = []

    def format_texts(self,
                     _initial_categories_list: List[str],
                     split_words_number=60,
                     tokenizer_number=70) -> None:
        """
        Format incoming texts. Splits each text into: 1) Words by split_words_number;
        2) If chunked text is not comply tokenizer restrictions - splits it again
        :param _initial_categories_list: list of texts
        :param split_words_number: word number to split
        :param tokenizer_number: word number for tokenizer to verify
        """
        _categories_list = []
        split_categories_list = []
        # clean self._split_categories_numbers
        self._split_categories_numbers = []
        logging.info('Text(s) list length [' + str(len(_initial_categories_list)) + ']')
        logging.info('Splitting initial text by [' + str(split_words_number) + '] words')
        # preliminary split by words, to not overflow tokenize_attempt
        added_cat_counter = 0
        for _p_index, _p_initial_category in enumerate(_initial_categories_list):
            _p_split_list = spring_splitter_by_chunks(split_words_number - 1, _p_initial_category)
            split_categories_list.extend(_p_split_list)
            split_length = len(_p_split_list)
            if split_length > 1:
                self._split_categories_numbers.append(_p_index)
                self._related_categories_dict[_p_index] = list(
                    [x for x in
                     range(_p_index + added_cat_counter,
                           _p_index + added_cat_counter + split_length)])
                added_cat_counter += split_length - 1
            else:
                self._related_categories_dict[_p_index] = [_p_index + added_cat_counter]

        logging.info(
            'Chunking text again if some part of its ['
            + str(len(split_categories_list))
            + '] preliminary chunks is not fit by tokenizers\' limit of ['
            + str(tokenizer_number) + ']')
        for _index, initial_category in enumerate(split_categories_list):
            if module_clip.tokenize_attempt(initial_category) >= tokenizer_number:
                split_list = spring_splitter_by_chunks(split_words_number - 1, initial_category)
                _categories_list.extend(split_list)
                split_length = len(split_list)
                if split_length > 1:
                    self._split_categories_numbers.append(_index)
                    self._related_categories_dict[_index].extend(list(
                        [x for x in
                         range(_index + added_cat_counter,
                               _index + added_cat_counter + split_length)]))
                    added_cat_counter += split_length - 1
                else:
                    self._related_categories_dict[_index].extend([_index + added_cat_counter])
            else:
                _categories_list.append(initial_category)

        logging.info('Text split by [' + str(len(_categories_list)) + '] chunks')
        self._text = module_clip.tokenize(_categories_list).to(self._device)

    def preprocess_probabilities(self, probabilities: List[any]) \
            -> typing.List[typing.Tuple[int, float]]:
        """
        Preprocesses probabilities list - replaces working category with real one, calculates
        the maximum probability per category
        :return: a list of maximum probabilities per category
        """
        real_cat_probabilities = []
        for index in range(len(probabilities[0])):
            replacement_category_index = self.get_replacement_category_index(index)
            real_cat_probabilities.append(
                (replacement_category_index, probabilities[0][index]))
        return select_maximum_value_in_list_of_tuples(real_cat_probabilities)

    class ImageHolder:
        """
        A holder for image and probabilities found for this image
        """

        def __init__(self, clip_image_text_processor) -> None:
            super().__init__()
            self.outer = clip_image_text_processor
            self.image = None
            self.probabilities = None

        def set_image(self, image_path: str):
            self.image = self.outer.load_image(image_path)
