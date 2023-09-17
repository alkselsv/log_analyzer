from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# library for save and load scikit-learn models
import pickle

# load example data from sklearn
X, y = load_iris(return_X_y=True)

# create Random Forest Classifier
rf = RandomForestClassifier()

# fit model with all data - it is just example!
rf.fit(X, y)

# file name, I'm using *.pickle as a file extension
filename = "model.pkl"

# save model
pickle.dump(rf, open(filename, "wb"))

# load model
loaded_model = pickle.load(open(filename, "rb"))

# you can use loaded model to compute predictions
y_predicted = loaded_model.predict(X)
