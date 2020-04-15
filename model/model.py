import numpy as np
import pandas as pd
import seaborn as sns
from surprise import Reader, Dataset, SVD, NMF, accuracy
from surprise.model_selection import train_test_split

DATA_DIR="./data/"
RATING_DATA = DATA_DIR + "ratings.csv"
BOOK_DATA = DATA_DIR + 'books.csv'

ratings = pd.read_csv(RATING_DATA)

reader = Reader()
data = Dataset.load_from_df(ratings, reader)
train, test = train_test_split(data, test_size = 0.8)

# Singular Value decomposition
model = SVD()
model.fit(train)
preds = model.test(test)
accuracy.rmse(preds)

# Non-negative Matrix factorization
model = NMF()
model.fit(train)
preds = model.test(test)
accuracy.rmse(preds)
