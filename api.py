import json
import requests

from api_routes import *

class LibraryAPI:
    def get_book_details(self, book_id):
        response = requests.get(url=BOOK_ID_URL.format(book_id))
        return json.loads(response.text)

    def get_books_by_category(self, category, offset=None, limit=1):
        parameters = {"offset": offset, "limit": limit}

        response = requests.get(url=BOOK_CATEGORY_URL.format(category), params=parameters)
        return json.loads(response.text)

    def get_books_by_author(self, author_id):
        response = requests.get(url=BOOK_AUTHOR_URL.format(author_id))
        return json.loads(response.text)
