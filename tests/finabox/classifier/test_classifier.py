from json import load
from os.path import join

import pytest

from finabox.classifier import ClassifierAI


@pytest.fixture
def classifier():
    with open(join('resources', 'categories-mapping.json'), 'r') as file:
        categories_mapping: dict = load(file)

    categories = list(categories_mapping.values())
    estabilishments = list(categories_mapping.keys())
    classifier = ClassifierAI(estabilishments, categories)

    return classifier


def test_classifier_predict(classifier):
    new_estabilishments = ['Cinemark WestPlaza', '99App']
    predicted_category = classifier.predict_classification(new_estabilishments)
    expected_category = [('Cinema',), ('Transporte',)]

    assert predicted_category == expected_category
