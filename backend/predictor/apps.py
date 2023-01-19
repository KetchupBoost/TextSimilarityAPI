import os.path
from django.apps import AppConfig
from django.conf import settings
from gensim.models.doc2vec import Doc2Vec


class PredictorConfig(AppConfig):
    # Create Path to Models
    path = os.path.join(settings.MODELS, 'doc2vec_model')

    # Load models
    d2v_model = Doc2Vec.load(path)

    default_auto_field = "django.db.models.BigAutoField"
    name = "predictor"
