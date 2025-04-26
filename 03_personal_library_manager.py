import streamlit as st
import pandas as pd
import os

# File to store book data
DATA_FILE = 'library.csv'

# Initialize data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Title", "Author", "Year", "Genre"])

# --- Sidebar: Add Book ---
st.sidebar.header("➕ Add a New Book")
with st.sidebar.form("add_book_form"):
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Genre")
    submitted = st.form_submit_button("Add Book")

    if submitted and title:
        new_book = pd.DataFrame([[title, author, year, genre]], columns=df.columns)
        df = pd.concat([df, new_book], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success(f"📘 '{title}' added!")

# --- Main: Library Manager ---
st.title("📚 Personal Library Manager")

search = st.text_input("🔍 Search by title or author").lower()

# Filter results
if search:
    filtered_df = df[df['Title'].str.lower().str.contains(search) | df['Author'].str.lower().str.contains(search)]
else:
    filtered_df = df

st.write(f"Showing {len(filtered_df)} books:")
st.dataframe(filtered_df)

# --- Delete a book ---
st.subheader("🗑️ Delete a Book")
book_to_delete = st.selectbox("Select book title to delete", df["Title"].unique() if not df.empty else [])
if st.button("Delete Selected Book"):
    df = df[df["Title"] != book_to_delete]
    df.to_csv(DATA_FILE, index=False)
    st.success(f"✅ '{book_to_delete}' deleted.")
