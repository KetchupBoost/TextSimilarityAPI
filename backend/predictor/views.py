from django.shortcuts import render
from .apps import PredictorConfig
from django.http import JsonResponse
from rest_framework.views import APIView


class call_model(APIView):
    def get(self, request):
        if request.method == 'GET':

            # Get sound from request
            sound = request.GET.get('sound')

            # Vectorize Sound
            vector = PredictorConfig.vectorizer.transform([sound])

            # Predict based on vector
            prediction = PredictorConfig.regressor.predict(vector)[0]

            # Build Response
            response = {'dog': prediction}

            # Return Response
            return JsonResponse(response)
