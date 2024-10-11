from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://www.themuse.com/api/public/jobs"

def get_jobs(page=1, keywords=None, location=None):
    params = {
        'page': page,
    }
    
    if keywords:
        params['category'] = keywords
    if location:
        params['location'] = location

    response = requests.get(API_URL, params=params)
    print(f"Request URL: {response.url}")  # Para depurar la URL de solicitud
    if response.status_code == 200:
        
        return response.json().get('results', [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        print(f"Error: {response.status_code}, Message: {response.text}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    keywords = request.args.get('keywords')
    location = request.args.get('location')
    print(f"Keywords: {keywords}, Location: {location}")  # Imprime los parámetros
    jobs = get_jobs(page=1, keywords=keywords, location=location)
    return render_template('index.html', jobs=jobs, page=1, keywords=keywords, location=location)

@app.route('/page/<int:page_number>', methods=['GET'])
def page(page_number):
    keywords = request.args.get('keywords')
    location = request.args.get('location')
    
    jobs = get_jobs(page=page_number, keywords=keywords, location=location)
    return render_template('index.html', jobs=jobs, page=page_number, keywords=keywords, location=location)

if __name__ == '__main__':
    app.run(debug=True)
