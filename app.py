# app.py

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample tweet data
tweets_data = []

MAX_TWEET_LENGTH = 280

@app.route('/tweets', methods=['POST'])
def create_tweet():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({'error': 'Bad or incomplete request'}), 400

    tweet_text = data['text']

    if len(tweet_text) > MAX_TWEET_LENGTH:
        return jsonify({'error': 'Tweet exceeds the maximum length of 280 characters'}), 400

    new_tweet = {
        'id': len(tweets_data) + 1,
        'text': tweet_text
    }

    tweets_data.append(new_tweet)

    return jsonify({'message': 'Tweet created successfully'}), 201

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/tweets', methods=['GET'])
def get_all_tweets():
    return jsonify(tweets_data)

@app.route('/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet_by_id(tweet_id):
    tweet = next((tweet for tweet in tweets_data if tweet['id'] == tweet_id), None)

    if tweet is None:
        abort(404)

    return jsonify(tweet)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
