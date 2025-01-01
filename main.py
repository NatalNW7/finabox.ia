from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MultiLabelBinarizer
from json import load
from os.path import join

with open(join('resources', 'categories-mapping.json'), 'r') as file:
    categories_mapping: dict = load(file)


categories = list(categories_mapping.values())
estabilishments = list(categories_mapping.keys())

multiLabelBinarizer = MultiLabelBinarizer()
y_categories = multiLabelBinarizer.fit_transform(categories)

vectorizer = CountVectorizer()
x_estabilishments = vectorizer.fit_transform(estabilishments)

model = OneVsRestClassifier(LinearSVC())
model.fit(x_estabilishments, y_categories)


new_estabilishments = ['Cinemark WestPlaza', '99App']
matrix_document = vectorizer.transform(new_estabilishments)
predict = model.predict(matrix_document)
predicted_category = multiLabelBinarizer.inverse_transform(predict)

print(f'Estabilishments: {new_estabilishments}\nPredicted Category: {predicted_category}')
