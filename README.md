# Disease Prediction Web App

A modern, multi-page Django web application for predicting diseases based on user-selected symptoms. The app uses a fully offline, rule-based engine and stores each prediction in a local MongoDB database. The UI is visually appealing, responsive, and easy to use.

## Features
- Predict diseases by selecting symptoms (no external APIs, fully offline logic)
- Modern, dark-themed, multi-page UI (Home, Predict, About, FAQ, Contact)
- Responsive, rounded navigation bar with logo
- Stores each prediction (symptoms + result) in local MongoDB

## Requirements
- Python 3.8+
- pip
- MongoDB (running locally on default port 27017)
- (Recommended) Virtualenv

## Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/yourusername/disease-prediction.git
cd disease-prediction
```

### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```
pip install django mongoengine
```

### 4. Start MongoDB
Make sure MongoDB is running locally (default: `localhost:27017`).

- On macOS (with Homebrew):
  ```
  brew services start mongodb-community
  ```
- Or use your preferred method to start MongoDB.

### 5. Run Database Migrations (for Django's SQLite DB)
```
python manage.py migrate
```

### 6. Start the Django Development Server
```
python manage.py runserver
```

### 7. Open the App
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure
- `predictor/models.py` — MongoDB models for storing symptoms and predictions
- `predictor/views.py` — Main logic and prediction engine
- `predictor/templates/predictor/` — All HTML templates (Home, Predict, About, FAQ, Contact, Result)
- `disease_prediction/settings.py` — Django and MongoDB configuration

## Notes
- All predictions are stored in MongoDB (`disease_prediction_db` database).
- No personal data is required or stored.
- For demo/educational use only. Not for medical advice.

## License
MIT License
