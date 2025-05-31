from django.shortcuts import render
import os
import requests
from itertools import combinations

# Use the provided Gemini API key directly
GEMINI_API_KEY = 'AIzaSyCboD5uYE6edacftARrziAJsWXQaaWvVoc'
# Use the available Gemini model from your API key's model list
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-002:generateContent'

SYMPTOM_LIST = [
    'fever', 'cough', 'headache', 'fatigue', 'nausea', 'vomiting', 'diarrhea', 'rash'
]

def home_page(request):
    return render(request, 'predictor/home.html')

def predict_disease(request):
    if request.method == 'POST':
        symptoms = set(request.POST.getlist('symptoms'))
        # Expanded rule-based mapping for more coverage
        base_disease_map = {
            frozenset(['fever', 'cough', 'fatigue']): ('Flu', 'Common viral infection with fever, cough, and fatigue.'),
            frozenset(['fever', 'rash']): ('Measles', 'Viral infection with fever and rash.'),
            frozenset(['nausea', 'vomiting', 'diarrhea']): ('Gastroenteritis', 'Stomach flu with nausea, vomiting, and diarrhea.'),
            frozenset(['headache', 'fatigue']): ('Migraine', 'Severe headache often with fatigue.'),
            frozenset(['cough', 'fever']): ('Common Cold', 'Mild viral infection with cough and fever.'),
            frozenset(['rash']): ('Allergy', 'Skin rash, possibly due to allergy.'),
            frozenset(['fever', 'headache', 'nausea']): ('Dengue', 'Mosquito-borne viral infection with fever, headache, and nausea.'),
            frozenset(['fever', 'vomiting', 'diarrhea']): ('Typhoid', 'Bacterial infection with fever, vomiting, and diarrhea.'),
            frozenset(['fatigue', 'nausea', 'vomiting']): ('Hepatitis', 'Liver infection with fatigue, nausea, and vomiting.'),
            frozenset(['fever', 'cough', 'headache']): ('COVID-19', 'Coronavirus infection with fever, cough, and headache.'),
            frozenset(['cough', 'fatigue']): ('Bronchitis', 'Inflammation of the bronchial tubes causing cough and fatigue.'),
            frozenset(['fever', 'diarrhea']): ('Food Poisoning', 'Illness caused by contaminated food, with fever and diarrhea.'),
            frozenset(['headache', 'nausea']): ('Tension Headache', 'Common headache with nausea.'),
            frozenset(['vomiting', 'diarrhea']): ('Stomach Infection', 'Infection causing vomiting and diarrhea.'),
            frozenset(['fever', 'fatigue', 'rash']): ('Chickenpox', 'Viral infection with fever, fatigue, and rash.'),
            frozenset(['cough', 'headache']): ('Sinusitis', 'Sinus infection with cough and headache.'),
            frozenset(['fever', 'nausea', 'rash']): ('Malaria', 'Mosquito-borne disease with fever, nausea, and rash.'),
            frozenset(['fatigue', 'diarrhea']): ('Irritable Bowel Syndrome', 'Digestive disorder with fatigue and diarrhea.'),
            frozenset(['nausea', 'rash']): ('Drug Reaction', 'Possible drug allergy with nausea and rash.'),
            frozenset(['fever', 'headache', 'fatigue', 'nausea', 'vomiting', 'diarrhea', 'rash', 'cough']): ('Severe Infection', 'Multiple symptoms may indicate a severe or systemic infection.'),
        }
        # Generate all possible 1,2,3,4-symptom combinations
        disease_map = dict(base_disease_map)
        for n in range(1, 5):
            for combo in combinations(SYMPTOM_LIST, n):
                key = frozenset(combo)
                if key not in disease_map:
                    disease_map[key] = (
                        'Unknown Combination',
                        f"No specific disease found for symptoms: {', '.join(sorted(combo))}."
                    )
        # Try to find the best match (largest subset)
        best_match = None
        best_len = 0
        for key, value in disease_map.items():
            if key.issubset(symptoms) and len(key) > best_len:
                best_match = value
                best_len = len(key)
        if best_match:
            disease, explanation = best_match
        else:
            disease = 'Unknown or Non-specific'
            explanation = 'Symptoms do not match a specific disease in our database.'
        return render(request, 'predictor/result.html', {'disease': disease, 'probability': explanation})
    # Always pass symptoms to the predict template for rendering
    return render(request, 'predictor/predict.html', {'symptoms': SYMPTOM_LIST})

def list_gemini_models(request):
    """Debug view to list available Gemini models for this API key/project."""
    url = 'https://generativelanguage.googleapis.com/v1/models'
    params = {'key': GEMINI_API_KEY}
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        error_detail = f"Status: {response.status_code}\nHeaders: {response.headers}\nText: {response.text}"
        try:
            error_json = response.json()
            error_detail += f"\nJSON: {error_json}"
        except Exception as e:
            error_detail += f"\nJSON decode error: {str(e)}"
        return render(request, 'predictor/result.html', {
            'disease': 'Model list API error',
            'probability': error_detail
        })
    data = response.json()
    models = data.get('models', [])
    model_list = '\n'.join([m.get('name', '') for m in models])
    return render(request, 'predictor/result.html', {
        'disease': 'Available Gemini Models',
        'probability': model_list or 'No models found.'
    })

def about_page(request):
    return render(request, 'predictor/about.html')

def faq_page(request):
    return render(request, 'predictor/faq.html')

def contact_page(request):
    return render(request, 'predictor/contact.html')
