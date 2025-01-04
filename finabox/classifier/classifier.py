from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC


class ClassifierAI:
    def __init__(self, x_data: list, y_target: list):
        self._binarizer = MultiLabelBinarizer()
        self._vectorizer = CountVectorizer()
        self._model = OneVsRestClassifier(LinearSVC())

        self.__train(x_data, y_target)

    def __train(self, *args):
        x = self._vectorizer.fit_transform(args[0])
        y = self._binarizer.fit_transform(args[1])
        self._model.fit(x, y)

    def predict_classification(self, data: list):
        data_to_classify = self._vectorizer.transform(data)
        target_classification = self._model.predict(data_to_classify)
        classification = self._binarizer.inverse_transform(
            target_classification
        )

        return classification
