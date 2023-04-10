import json
from urllib.request import urlopen
from dataclasses import dataclass
import logging

logger = logging.getLogger('manga generator for obsidian')


@dataclass
class NeededInfo:
    title: str
    authors: list
    pages: int
    cover: str


template_api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"


def get_needed_info(isbn):
    request = f"{template_api}{isbn}"
    logger.info(f"EXECUTION OF REQUEST: {request}")
    response = urlopen(request)
    # parse JSON into Python as a dictionary
    book_data = json.load(response)

    if book_data["totalItems"] > 0:

        # create additional variables for easy querying
        volume_info = book_data["items"][0]["volumeInfo"]

        title = volume_info.get("title", "")
        authors = volume_info.get("authors", [])
        pages = volume_info.get("pageCount", -1)
        if "imageLinks" in volume_info:
            cover = dict(volume_info["imageLinks"]).get("thumbnail", "")
        else:
            cover = ""

        return NeededInfo(title, authors, pages, cover)
    else:
        return NeededInfo("", [], 0, "")
