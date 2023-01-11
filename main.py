from classes.library import Library
from classes.Author import Author
from classes.Book import Book
from random import randrange
"""
Simple command line library app that uses a sqlite database to manage the books
This app runs under python 3.10 or newer!
"""
lib = Library()


def ls(args):
    """
    prints out a list of all the books or authors in the database
    :param args: string
    :return: None
    """
    if len(args) != 0:
        match(args[0]):
            case "-a":
                print("last_name, first_name, birth, death, nationality")
                for a in lib.authors:
                    print(a)
            case "-u":
                print("id, title, author, pages")
                unread(args)
            case "-r":
                print("id, title, author, pages, position")
                read(args)
            case "-f":
                print("id, title, author, pages")
                finished(args)
    else:
        print("id, title, author, pages, position")
        print(lib)


def unread(args):
    """
    prints out a list of all the unread books
    :param args: string
    :return: None
    """
    books = filter(lambda x: x.position == 0, lib.books)
    for i in books:
        print(F"{i.id}, {i.title}, {i.author.first_name} {i.author.last_name}, {i.pages}")


def read(args):
    """
    prints out a list of all the books that aren't unread or finished
    so the books where position != 0 or pages
    :param args: string
    :return: None
    """
    books = filter(lambda x: x.position != 0 and x.position != x.pages, lib.books)
    for i in books:
        print(i)


def finished(args):
    """
    prints out a list of all the books that are finished
    a book is considered finished when position == pages
    :param args: string
    :return: None
    """
    books = filter(lambda x: x.position == x.pages, lib.books)
    for i in books:
        print(F"{i.id}, {i.title}, {i.author.first_name} {i.author.last_name}, {i.pages}")


def nation(args):
    """
    prints out a list of all the books written by authors of a given nationality,
    prints nothing if said nationality isn't in the database
    :param args: string
    :return: None
    """
    filtered_list = list(filter(lambda x: x.author.nationality.lower() == args[0].lower(), lib.books))
    for b in filtered_list:
        print(b)


def add(args):
    """
    adds a book or author in the database
    :param args: string
    :return: None
    """
    attr = " ".join(args[1:]).split(":")
    if args[0] == "-b":
        for a in range(len(attr)):
            if attr[a].lower().strip() == "none":  # change the none strings to actual None so they can be inserted as null
                attr[a] = None
            else:
                attr[a] = " ".join(w.capitalize() for w in attr[a].split(" ")) # capitalize each word so it's not case sensitive
        author = Author(attr[1], attr[2])
        book = Book(attr[0], author, attr[3])
        lib.add_book(book)
    if args[0] == "-a":
        for a in range(len(attr)):
            if attr[a].lower().strip() == "none":
                attr[a] = None
            else:
                attr[a] = " ".join(w.capitalize() for w in attr[a].split(" "))
        author = Author(attr[0], attr[1], attr[2], attr[3], attr[4])
        if author in lib.authors:
            print("This author is already in the database")
            return
        lib.add_auth(author)
    lib.update()


def rand(args):
    """
    prints out a random book that isn't read, a book is considered unread if its position is 0
    :param args: string
    :return: None
    """
    unread_books = list(filter(lambda x: x.position == 0, lib.books))
    print(unread_books[randrange(0, len(unread_books)-1)])


def up_pos(args):
    """
    updates the position (aka current page) of a book
    :param args: string
    :return: None
    """
    id_ = args[0]
    new_pos = args[1]
    try:
        if int(new_pos) < 0:
            print("Invalid Position")
            return
    except ValueError:
        print("Invalid Position")
        return
    lib.update_pos(id_, new_pos)
    lib.update()


# this dict is used to easily and cleanly execute the different commands
commands = {
    "ls": ls,
    "nation": nation,
    "add": add,
    "rand": rand,
    "up_pos": up_pos,
}

if __name__ == "__main__":
    print("Welcome to your library!")
    print("Type help for a list of available commands\n")
    while True:
        command = input(">")
        # these 2 special commands don't interact with the db, so they are executed here
        if command.lower() == "help":
            print("ls [options] - lists what is indicated as option")
            print(" no option: lists all the books in the library")
            print(" -a: lists all the authors in the library")
            print(" -u: lists all the unread books in the library")
            print(" -r: lists all of the books you are reading")
            print(" -f: lists all of the books you finished\n")
            print("add [options] - add a book or author to your library, use -b to add a book, -a to add an author. Attributes must be formatted as followed")
            print(" book: TITLE:AUTHOR_FIRST_NAME:AUTHOR_LAST_NAME:NUMBER_OF_PAGES")
            print(" author: FIRST_NAME:LAST_NAME:birth_year:death_year:nationality")
            print(" Required parameters are capitalized, non-required parameters can have none as a value if you want to omit it")
            print(" i.e.: add -b Les Mouches:Jean-Paul:Sartre:200")
            print(" add -a Victor:Hugo:none:none:France\n")
            print("up_pos [id] [new_pos] - updates your position (current page) in a book, you can find the id of the book with ls\n")
            print("nation - prints the books written by authors from the given country\n")
            print("rand - gives a random book that you haven't read yet\n")
            print("quit - exits the library")
            continue
        if command.lower() == "quit":
            break

        # this is where the commands that interact with the db are executed
        command_args = command.split(" ")
        try:
            # first element is the command, others are the arguments
            # some commands don't use arguments, but they are all called with
            # arguments to reduce the amount of code in that section
            commands[command_args[0]](command_args[1:])
        except KeyError:
            print("Unknown command")
