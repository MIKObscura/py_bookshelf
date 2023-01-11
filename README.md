This is a simple command line application to manage a library, I have included a db with some data in it as an example.

To run the application, simply execute main.py with your python interpreter. Do note that you need at least python 3.10 for it to work

When run, you're greeted by a CLI with a few commands available which you can find at any time with the help command, here are all of these commands:
```
ls [options] - lists what is indicated as option
 no option: lists all the books in the library
 -a: lists all the authors in the library
 -u: lists all the unread books in the library
 -r: lists all of the books you are reading
 -f: lists all of the books you finished

add [options] - add a book or author to your library, use -b to add a book, -a to add an author. Attributes must be formatted as followed
 book: TITLE:AUTHOR_FIRST_NAME:AUTHOR_LAST_NAME:NUMBER_OF_PAGES
 author: FIRST_NAME:LAST_NAME:birth_year:death_year:nationality
 Required parameters are capitalized, non-required parameters can have none as a value if you want to omit it
 i.e.: add -b Les Mouches:Jean-Paul:Sartre:200
 add -a Victor:Hugo:none:none:France

up_pos [id] [new_pos] - updates your position (current page) in a book, you can find the id of the book with ls

nation - prints the books written by authors from the given country

rand - gives a random book that you haven't read yet

quit - exits the library
```
More may be added in the future if I have some ideas.