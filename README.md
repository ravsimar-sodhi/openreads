# Book Recommendation Application
## CSE461 - Software Engineering (Spring 2020) - Final Project

To run :

- Download / Clone the repository
- Download the database from https://drive.google.com/file/d/1SDei6uYIJ-z2CbKI_29Fgc_griR1kccA/view?usp=sharing and save it inside book_recommender
- Download the model reco_model_cosine_small.pkl from https://drive.google.com/drive/folders/1ycGuhbG4OpWmKyihxQGX2soV8s32lbS8?usp=sharing and save it inside the Predictor directory within book_recommender.
- cd book_recommender (in terminal)
- python3 manage.py runserver 8081 (in terminal)
- Go to localhost or http://127.0.0.1:8081/ from any browser

For the new database with 20,000 books -  https://drive.google.com/file/d/1SDei6uYIJ-z2CbKI_29Fgc_griR1kccA/view?usp=sharing



(Added Users_Bookshelf, Users_bookshelf_book, Usergroups_groupshelf and Usergroups_groupshelf_book columns in the database)
(Made changes for the errors for bookshelves)
