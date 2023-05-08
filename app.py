import json
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

countries = [
    {"name": "Noruega", "song": "Queen of kings", "artist": "Alessandra"},
    {"name": "Malta", "song": "Dance (our own party)", "artist": "The Busker"},
    {"name": "Serbia", "song": "Samo mí se spava", "artist": "Luke Black"},
    {"name": "Letonia", "song": "Sudden lights", "artist": "Sudden Lights"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        votes = []
        for country in countries:
            country_name = country['name']
            score = float(request.form[country_name + '_score'])
            description = request.form[country_name + '_description']
            votes.append({'country': country_name, 'score': score, 'description': description})
        return redirect(url_for('results', votes=json.dumps(votes)))
    return render_template('index.html', countries=countries)

@app.route('/results')
def results():
    votes = json.loads(request.args.get('votes', '[]'))
    ranked_votes = sorted(votes, key=lambda x: x['score'], reverse=True)
    return render_template('results.html', votes=ranked_votes, countries=countries)

@app.route('/download_csv', methods=['POST'])
def download_csv():
    votes = json.loads(request.args.get('votes', '[]'))
    ranked_votes = sorted(votes, key=lambda x: x['score'], reverse=True)

    # Crear el archivo CSV en memoria
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['País', 'Puntuación'])
    for vote in ranked_votes:
        writer.writerow([vote['country'], str(vote['score'])])

    # Obtener el contenido CSV codificado en UTF-8
    csv_content = csv_data.getvalue().encode('utf-8')

    # Configurar la respuesta HTTP con el archivo CSV
    response = Response(csv_content, content_type='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='resultados.csv')

    return response

if __name__ == '__main__':
    app.run()
