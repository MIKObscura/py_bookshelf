class Author:
    def __init__(self, f_name, l_name, birth=None, death=None, nationality=None):
        self.__first_name = f_name
        self.__last_name = l_name
        self.__birth_year = birth
        self.__death_year = death
        self.__nationality = nationality

    def __eq__(self, other):  # added so that the class can work with the in operator
        if not isinstance(other, Author):
            raise TypeError
        return self.__first_name == other.first_name and self.__last_name == other.last_name

    def __str__(self):
        return F"{self.__last_name}, {self.__first_name}, {self.__birth_year}, {self.__death_year}, {self.__nationality}"

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def birth_year(self):
        return self.__birth_year

    @property
    def death_year(self):
        return self.__death_year

    @property
    def nationality(self):
        return self.__nationality
