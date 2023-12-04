from flask import Flask, jsonify, request, abort
import json
import pytest

app = Flask(__name__)

# Load tweet data from the file
with open('100tweets.json', 'r', encoding='utf-8', errors='ignore') as file:
    # Use json.loads to handle decoding manually
    tweets_data = json.loads(file.read())







@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/tweets', methods=['GET'])# ... (previous code)

@app.route('/tweets', methods=['POST'])
def create_tweet():
    data = request.get_json()

    if 'text' not in data:
        print("Bad or incomplete request detected. Returning 400.")
        return jsonify({'error': 'Bad or incomplete request'}), 400

    # Process the tweet creation here

    return jsonify({'message': 'Tweet created successfully'}), 201

# ... (rest of the code)

def get_all_tweets():
    query_param = request.args.get('filter')
    if query_param:
        filtered_tweets = [tweet for tweet in tweets_data if query_param.lower() in tweet['text'].lower()]
        return jsonify(filtered_tweets)
    else:
        return jsonify(tweets_data)


@app.route('/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet_by_id(tweet_id):
    try:
        tweet = next(tweet for tweet in tweets_data if tweet['id'] == tweet_id)
        return jsonify(tweet)
    except StopIteration:
        abort(404)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5001)


# Unit tests for the POST endpoint

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_create_tweet_success(client):
    data = {'text': 'This is a new tweet'}
    response = client.post('/tweets', json=data)
    assert response.status_code == 201
    assert response.json['message'] == 'Tweet created successfully'


def test_create_tweet_missing_text(client):
    data = {}
    response = client.post('/tweets', json=data)
    assert response.status_code == 400
    assert response.json['error'] == 'Bad or incomplete request'

def test_create_tweet_excessive_length(client):  # Add the 'client' fixture as an argument
    data = {'text': 'This tweet is too long. It exceeds the maximum length of 280 characters.'}
    response = client.post('/tweets', json=data)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
