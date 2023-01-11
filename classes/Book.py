class Book:
    def __init__(self, title, author, pages, position=0, id_=None):
        self.__title = title
        self.__author = author
        self.__pages = pages
        self.__position = position
        self.__id = id_

    def __str__(self):
        return F"{self.id}, {self.__title}, {self.__author.first_name} {self.__author.last_name}, {self.__pages}, {self.__position}"

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def pages(self):
        return self.__pages

    @property
    def position(self):
        return self.__position

    @property
    def id(self):
        return self.__id
