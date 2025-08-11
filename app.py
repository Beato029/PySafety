from flask import Flask, jsonify

app = Flask(__name__)

# Dati di esempio: lista di news
news = [
    {
        "id": 1,
        "title": "Aggiornamento 1",
        "description": "Descrizione dell'aggiornamento 1",
        "image_url": "https://tuoserver.com/images/news1.jpg",
        "video_url": "https://tuoserver.com/videos/news1.mp4",
        "date": "2025-08-10T12:00:00Z"
    },
    {
        "id": 2,
        "title": "Aggiornamento 2",
        "description": "Descrizione dell'aggiornamento 2",
        "image_url": "https://tuoserver.com/images/news2.jpg",
        "video_url": "",
        "date": "2025-08-11T15:00:00Z"
    }
]

# Endpoint API per tutte le news
@app.route('/api/news', methods=['GET'])
def get_news():
    return jsonify(news)

# Endpoint API per una news specifica
@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_item(news_id):
    for item in news:
        if item['id'] == news_id:
            return jsonify(item)
    return jsonify({"error": "News not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
