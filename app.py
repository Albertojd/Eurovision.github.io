import json
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, Response


app = Flask(__name__, static_url_path='/static')

countries = countries = [
    {"name": "Dinamarca", "song": "Breaking My Heart", "artist": "Reiley"},
    {"name": "Armenia", "song": "Future Lover", "artist": "Brunette"},
    {"name": "Rumania", "song": "D.G.T. (Off and On)", "artist": "Theodor Andrei"},
    {"name": "Estonia", "song": "Bridges", "artist": "Alika"},
    {"name": "Bélgica", "song": "Because Of You", "artist": "Gustaph"},
    {"name": "Chipre", "song": "Break A Broken Heart", "artist": "Andrew Lambrou"},
    {"name": "Islandia", "song": "Power", "artist": "Diljá"},
    {"name": "Grecia", "song": "What They Say", "artist": "Victor Vernicos"},
    {"name": "Polonia", "song": "Solo", "artist": "Blanka"},
    {"name": "Eslovenia", "song": "Carpe Diem", "artist": "Joker Out"},
    {"name": "Georgia", "song": "Echo", "artist": "Iru"},
    {"name": "San Marino", "song": "Like An Animal", "artist": "Piqued Jacks"},
    {"name": "Austria", "song": "Who The Hell Is Edgar?", "artist": "Teya & Salena"},
    {"name": "Albania", "song": "Duje", "artist": "Albina & Familja Kelmendi"},
    {"name": "Lituania", "song": "Stay", "artist": "Monika Linkytė"},
    {"name": "Australia", "song": "Promise", "artist": "Voyager"}
]
def get_country_code(country_name):
    code_mappings = {
        "Dinamarca": "dk",
        "Armenia": "am",
        "Rumania": "ro",
        "Estonia": "ee",
        "Bélgica": "be",
        "Chipre": "cy",
        "Islandia": "is",
        "Grecia": "gr",
        "Polonia": "pl",
        "Eslovenia": "si",
        "Georgia": "ge",
        "San Marino": "sm",
        "Austria": "at",
        "Albania": "al",
        "Lituania": "lt",
        "Australia": "au"
    }
    return code_mappings.get(country_name, "")

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
    return render_template('index.html', countries=countries, get_country_code=get_country_code)


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
