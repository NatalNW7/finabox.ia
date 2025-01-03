from finabox.classifier import ClassifierAI
from json import load
from os.path import join
import pandas as pd

if __name__ == "__main__":
    # with open(join('resources', 'categories-mapping.json'), 'r') as file:
    #     categories_mapping: dict = load(file)


    # categories = list(categories_mapping.values())
    # estabilishments = list(categories_mapping.keys())
    # classifier = ClassifierAI(estabilishments, categories)

    # new_estabilishments = ['Cinemark WestPlaza', '99App']
    # predicted_category = classifier.predict_classification(new_estabilishments)

    # print(f'Estabilishments: {new_estabilishments}\nPredicted Category: {predicted_category}')

    data = {
        'description': ['mercadolivre*comp', 'sheinbr']
    }
    df = pd.DataFrame(data)

    with open(join('resources', 'estabilishments-mapping.json'), 'r') as file:
        estabilishments_mapping: dict = load(file)

    estabilishments = list(estabilishments_mapping.values())
    description = list(estabilishments_mapping.keys())
    classifier = ClassifierAI(description, estabilishments)

    values = list(df['description'].values)
    predicted_estabilishments = classifier.predict_classification(values)

    print(f'Description: {values}\nPredicted Estabilishments: {predicted_estabilishments}')

    df['label'] = predicted_estabilishments

    print(df.head())
