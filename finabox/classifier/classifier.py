from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC


class ClassifierAI:
    def __init__(self, x_data: list = None, y_target: list = None):
        self._binarizer = MultiLabelBinarizer()
        self._vectorizer = CountVectorizer()
        self._model = OneVsRestClassifier(LinearSVC())

        if x_data and y_target:
            self.train(x_data, y_target)

    def train(self, x_data: list, y_target: list):
        x = self._vectorizer.fit_transform(x_data)
        y = self._binarizer.fit_transform(y_target)
        self._model.fit(x, y)

    def predict_classification(self, data: list):
        data_to_classify = self._vectorizer.transform(data)
        target_classification = self._model.predict(data_to_classify)
        classification = self._binarizer.inverse_transform(
            target_classification
        )

        return classification


class Classifier:
    def __init__(self, resource_mapping: dict = None):
        if resource_mapping:
            self.setup_resource(resource_mapping)

    def setup_resource(self, resource_mapping: dict):
        x_data = resource_mapping.keys()
        y_target = resource_mapping.values()
        self.classifie_ai = ClassifierAI(x_data, y_target)

    def classify(self, data: list):
        return self.classifie_ai.predict_classification(data)
