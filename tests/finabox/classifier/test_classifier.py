from json import load
from os.path import join

import pytest

from finabox.classifier import Classifier


@pytest.fixture
def classifier():
    with open(join('resources', 'categories-mapping.json'), 'r') as file:
        categories_mapping: dict = load(file)

    classifier = Classifier(categories_mapping)

    return classifier


def test_classifier(classifier):
    new_estabilishments = ['Cinemark WestPlaza', '99App']
    predicted_category = classifier.classify(new_estabilishments)
    expected_category = [('Cinema',), ('Transporte',)]

    assert predicted_category == expected_category
