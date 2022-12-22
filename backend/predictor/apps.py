import os.path
import pickle
from django.apps import AppConfig
from django.conf import settings

class PredictorConfig(AppConfig):
    # Create Path to Models
    path = os.path.join(settings.MODELS, 'models.p')

    # Load models in separate variables
    with open(path, 'rb') as pickled:
        data = pickle.load(pickled)

    regressor = data['regressor']
    vectorizer = data['vectorizer']

    default_auto_field = "django.db.models.BigAutoField"
    name = "predictor"


