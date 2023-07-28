from api import LibraryAPI

class Main:
    def __init__(self):
        self.CSV_HEADER = ["Book ID", "Book Title", "Categories", "Authors Names", "Price", "Description"]
        self._library_api = LibraryAPI()

        self._books_data = {}
        self._report_data = []
        self._authors_details = []

    def execute(self):
        self.get_book_data()
        self.extract_books_details()
        self.extract_authors_details()
        self.filter_authors_name()
        self.generate_report()

    def get_book_data(self):
        with open("book_price.csv", "r") as file:
            data = file.readlines()

            for info in data[1:]:
                book_id, price = info.split(",")
                self._books_data[book_id] = price.strip("\n")
    
    def generate_report(self):
        with open("books_report.csv", "w", encoding="utf-8") as file:
            file.writelines(";".join(self.CSV_HEADER) + "\n")

            for data in self._report_data:
                parameters = (
                    data.get("book_id") or "",
                    data.get("book_title") or "",
                    data.get("categories") or "",
                    data.get("author_name") or "",
                    data.get("price") or "",
                    data.get("description") or ""
                )

                line = ";".join(parameters) + "\n"
                file.writelines(line)

    def extract_books_details(self):
        for book_id, book_price in self._books_data.items():
            book_info = {}
            details = self._library_api.get_book_details(book_id)

            try:
                book_info["book_id"] = book_id
                book_info["book_title"] = details.get("title")
                if isinstance(details.get("subjects"), list):
                    book_info["categories"] = ";".join(details.get("subjects"))
                book_info["price"] = book_price

                if details.get("authors"):
                    for author_details in details.get("authors"):
                        if author_details.get("author"):
                            book_info["author_id"] = author_details["author"]["key"].split("/")[-1]

                if details.get("description"):
                    try:
                        if details["description"].get("value"):
                            book_info["description"] = details["description"]["value"].replace("\n", " ").replace("\r", " ")
                    except AttributeError:
                        book_info["description"] = details["description"].replace("\n", " ").replace("\r", " ")
                elif details.get("excerpts"):
                    book_info["description"] = details["excerpts"][0].get("excerpt")["value"]
            except Exception as ex:
                print(ex)
                print(details)

            self._report_data.append(book_info)

    def extract_authors_details(self):
        for data in self._report_data:
            details = self._library_api.get_books_by_author(data.get("author_id"))
            self._authors_details.append(details)

    def filter_authors_name(self):
        for details in self._authors_details:
            author_id = details["key"].split("/")[-1]

            for index, data in enumerate(self._report_data):
                if data.get("author_id") == author_id:
                    self._report_data[index]["author_name"] = details["name"]
                    break


main = Main()
main.execute()