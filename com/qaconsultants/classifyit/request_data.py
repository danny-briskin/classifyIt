from typing import List


class RequestData:
    def __init__(self, image_url: str, image_texts: List[str]) -> None:
        super().__init__()
        self.image_url = image_url
        self.image_texts = image_texts
