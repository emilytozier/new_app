#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

db_name = 'postgres'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'my_db'
db_port = '5432'

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
engine = create_engine(db_string)

Base = declarative_base()

class Author(Base):
   __tablename__ = 'authors'

   author_id = Column(Integer, primary_key=True)
   first_name = Column(String(length=50))
   last_name = Column(String(length=50))

   def __repr__(self):
      return "<Author(author_id='{0}', first_name='{1}', last_name='{2}'>".format(self.author_id, 
         self.first_name, self.last_name)

class Book(Base):
   __tablename__ = 'books'

   book_id = Column(Integer, primary_key=True)
   title = Column(String(length=50))
   number_of_pages = Column(Integer)

   def __repr__(self):
      return "<Book(book_id='{0}', title='{1}', number_of_pages='{2}'>".format(self.book_id, 
         self.title, self.number_of_pages)

class BookAuthor(Base):
   __tablename__ = 'bookauthors'

   bookauthor_id = Column(Integer, primary_key=True)
   author_id = Column(Integer, ForeignKey('authors.author_id'))
   book_id = Column(Integer, ForeignKey('books.book_id'))

   author = relationship("Author")
   book = relationship("Book")

   def __repr__(self):
      return '''<BookAuthor(bookauthor_id='{0}', 
         author_first_name='{1}', author_last_name='{2}',
         book_title='{3}'>'''.format(self.bookauthor_id, 
            self.author.first_name, 
            self.author.last_name, 
            self.book.title)

Base.metadata.create_all(engine)

def create_session():
   session = sessionmaker(bind=engine)
   return session()

def add_book(title, number_of_pages, first_name, last_name):
   book = Book(title=title, number_of_pages=number_of_pages)

   session = create_session()

   try:
      existing_author = session.query(Author).filter(Author.first_name == 
         first_name, Author.last_name == last_name).first()

      session.add(book)

      if existing_author is not None:
         session.flush()
         pairing = BookAuthor(author_id=existing_author.author_id,
            book_id=book.book_id)
      else:
         author = Author(first_name=first_name, last_name=last_name)
         session.add(author)
         session.flush()
         pairing = BookAuthor(author_id=author.author_id, 
            book_id=book.book_id)

      session.add(pairing)
      session.commit()
   
   except:
      session.rollback()
      raise

   finally:
      session.close()

if __name__ == "__main__":
   print("Input new book:\n")

   add_book('some title', 123, 'author first name', 'author last name')

   print("Done!")

