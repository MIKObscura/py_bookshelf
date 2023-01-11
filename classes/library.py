import sqlite3
from classes.Author import Author
from classes.Book import Book


class Library:
    def __init__(self):
        self.__books = self.__get_books()
        self.__authors = self.__get_auth()

    def update(self):  # best way to update the Library when the db gets updated
        self.__init__()

    @property
    def books(self):
        return self.__books

    @property
    def authors(self):
        return self.__authors

    def __str__(self):
        books = []
        for i in self.__books:
            books.append(F"{i.id}, {i.title}, {i.author.first_name} {i.author.last_name}, {i.pages}, {i.position}")
        return "\n".join(books)

    @staticmethod
    def add_book(book):
        """
        adds a book to the database
        :param book: Book object
        :return: None
        """
        db = sqlite3.connect("library.db")
        db_cur = db.cursor()
        test_auth = db_cur.execute(F"select * from tbAuthors where first_name = '{book.author.first_name}' and last_name = '{book.author.last_name}'").fetchall()
        if len(test_auth) == 0:
            db_cur.execute(F"insert into tbAuthors('first_name', 'last_name', 'death', 'birth', 'nationality')"
                           F" values ('{book.author.first_name}', '{book.author.last_name}', "
                           F"'{book.author.death_year}', '{book.author.birth_year}', '{book.author.nationality}')")
            db.commit()
        auth_id = db_cur.execute(F"select id from tbAuthors where first_name = '{book.author.first_name}' and last_name = '{book.author.last_name}'").fetchone()[0]
        db_cur.execute(F"insert into tbBooks('title', 'author', 'pages', 'position') values ('{book.title}', '{auth_id}', '{book.pages}', '{book.position}')")
        db.commit()

    @staticmethod
    def update_pos(id_, pos):
        """
        updates the position of a given book
        :param id_: int, selects the book in the db
        :param pos: new position to set, must be lower than the amount of pages in the book
        :return: None
        """
        db = sqlite3.connect("library.db")
        db_cur = db.cursor()
        pages = db_cur.execute(F"select pages from tbBooks where id={id_}").fetchone()[0]
        if pages < int(pos):  # the position can't be higher than the pages in the book of course
            print("Invalid Position")
            return
        db_cur.execute(F"update tbBooks set position={pos} where id={id_}")
        db.commit()

    @staticmethod
    def add_auth(author):
        """
        adds an author to the database
        :param author: Author object
        :return: None
        """
        db = sqlite3.connect("library.db")
        db_cur = db.cursor()
        # for whatever reasons this function refuses to convert None to null unless you format it like that
        db_cur.execute("insert into tbAuthors('first_name', 'last_name', 'death', 'birth', 'nationality') "
                       "values (?,?,?,?,?)", (author.first_name, author.last_name, author.death_year, author.birth_year, author.nationality))
        db.commit()

    # these 2 methods are private since they are supposed to only be executed when the Library is initialized
    # or needs to be updated, they could technically be directly in __init__ but it looks cleaner this way
    @staticmethod
    def __get_books():
        """
        fetches all the books in the database
        :return: array of Book objects containing all the books in the library
        """
        db = sqlite3.connect("library.db")
        db_cur = db.cursor()
        data = db_cur.execute("select * from tbAuthors join tbBooks on tbAuthors.id = tbBooks.author").fetchall()
        books_list = []
        for b in data:
            author = Author(b[1], b[2], b[3], b[4], b[5])
            book = Book(b[7], author, b[9], b[10], b[6])
            books_list.append(book)
        return books_list

    @staticmethod
    def __get_auth():
        """
        fetches all the authors in the database
        :return: array of Author objects containing all the authors in the library
        """
        db = sqlite3.connect("library.db")
        db_cur = db.cursor()
        data = db_cur.execute("select * from tbAuthors")
        auth_list = []
        for a in data:
            auth_list.append(Author(a[1], a[2], a[3], a[4], a[5]))
        return auth_list
