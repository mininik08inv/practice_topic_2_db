from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Session
from sqlalchemy.sql import func
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = "genres"
    genre_id = Column(Integer, primary_key=True)
    name_genre = Column(String(50), nullable=False, unique=True)
    books = relationship("Book", back_populates="genre")


class Author(Base):
    __tablename__ = "authors"
    author_id = Column(Integer, primary_key=True)
    name_author = Column(String(100), nullable=False, unique=True)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    amount = Column(Integer, nullable=False, default=0)

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")


class City(Base):
    __tablename__ = "cities"
    city_id = Column(Integer, primary_key=True)
    name_city = Column(String(50), nullable=False, unique=True)
    delivery_days = Column(Integer, nullable=False, default=1)  # Срок доставки в днях
    clients = relationship("Client", back_populates="city")


class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, primary_key=True)
    name_client = Column(String(100), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.city_id'), index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)

    city = relationship("City", back_populates="clients")
    purchases = relationship("Buy", back_populates="client")


class Buy(Base):
    __tablename__ = "buy"
    buy_id = Column(Integer, primary_key=True)
    buy_description = Column(String(200))
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    client = relationship("Client", back_populates="purchases")
    steps = relationship("BuyStep", back_populates="buy")
    books = relationship("BuyBook", back_populates="buy")


class Step(Base):
    __tablename__ = "steps"
    step_id = Column(Integer, primary_key=True)
    name_step = Column(String(50), nullable=False, unique=True)


class BuyStep(Base):
    __tablename__ = "buy_steps"
    buy_step_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'), nullable=False, index=True)
    step_id = Column(Integer, ForeignKey('steps.step_id'), nullable=False, index=True)
    date_step_beg = Column(DateTime, nullable=False, server_default=func.now())
    date_step_end = Column(DateTime)

    buy = relationship("Buy", back_populates="steps")
    step = relationship("Step")


class BuyBook(Base):
    __tablename__ = "buy_book"
    buy_book_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), nullable=False, index=True)
    amount = Column(Integer, nullable=False, default=1)
    price = Column(DECIMAL(10, 2), nullable=False)  # Цена на момент покупки

    buy = relationship("Buy", back_populates="books")
    book = relationship("Book")


Base.metadata.create_all(engine)
