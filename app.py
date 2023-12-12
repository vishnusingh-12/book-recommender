# importing modules
import numpy as np
import streamlit as st
import pickle

# loading datasets
books = pickle.load(open('books.pkl', 'rb'))
books_users = pickle.load(open('books_users.pkl', 'rb'))
popular_books = pickle.load(open('popular_books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))


def recommend_book(book):
    """
    Recommends and shows images, names and buying links of 5 similar books
    :param book: book name for recommending books
    """
    # If no book selected then show the message
    if book == 'Select or Type a Book Name':
        st.markdown('### Please select or type a book name and click on Recommend ')
    # shows recommended books
    else:
        # empty books and author lists
        book_list = []
        author_list = []

        # getting index of the book from pivot table
        index = np.where(books_users.index == book)[0][0]

        # indices and similarity scores of top 5 similar books
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
        for b in similar_items:
            # getting titles of top 5 similar books
            book_list.append(books_users.index[b[0]])

            # getting author names of top 5 similar books
            author_list.append(books.loc[books['Book-Title'] == book_list[-1], 'Book-Author'].values[0])

        # creating a list of amazon search urls with book titles and author names
        url = [f"https://www.amazon.in/s?k=" + book_list[_].replace(' ', '+') + author_list[_].replace(' ', '+') for _
               in range(0, 5)]

        # making columns for book images like divs
        columns = st.columns([1, 1, 1, 1, 1])

        # showing the image and titles of books (which are hyperlinks to amazon store)
        for c in range(5):
            columns[c].image(books.loc[books['Book-Title'] == book_list[c], 'Image-URL-M'].values[0])
            columns[c].write(f"[{book_list[c]}-{author_list[c]}]({url[c]})")


def top_rated_books():

    # writing a heading
    st.markdown('### Top Rated Books')

    # getting titles images and authors of top 50 books
    for i in range(0, 50, 5):

        # getting titles of first five most popular books(then next 5 and so on)
        titles = [popular_books.iloc[j, 0].strip() for j in range(i, i + 5)]

        # getting authors of first five most popular books(then next 5 and so on)
        authors = [popular_books.iloc[g, 4].strip() for g in range(i, i + 5)]

        # making a list of urls for the 5 books fetched
        urls = [f"https://www.amazon.in/s?k=" + titles[k].replace(' ', '+') + authors[k].replace(' ', '+') for k in
                range(0, 5)]

        # making divs
        column = st.columns([1, 1, 1, 1, 1])

        # showing books with images tiles and buying links
        for m in range(0, 5):
            column[m].image(popular_books.loc[popular_books['Book-Title'] == titles[m], 'Image-URL-M'].values[0])
            column[m].write(f"[{titles[m]}-{authors[m]}]({urls[m]})")


# Heading of the webapp
st.markdown("## Book Recommender")

# creating a select box
book_name = st.selectbox('Type or Select Book Name ', ['Select or Type a Book Name'] + list(books_users.index.unique()))

# creating the recommend button
button = st.button('Recommend')

# if button clicked then call recommend book
if button:
    recommend_book(book_name.strip())

# else keep showing top-rated books
else:
    top_rated_books()