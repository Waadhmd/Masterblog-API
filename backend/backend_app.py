from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET','POST'])
def handle_posts():
    if request.method == 'POST':
        data = request.get_json()
        # Validate required fields
        missing_fields = []
        if not data or not data['title']:
            missing_fields.append("title")
        if not data or not data['content']:
            missing_fields.append("content")

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing": missing_fields
            }), 400

        new_post = {
            "id":max((post['id'] for post in POSTS),default=0)+1,
            "title" : data.get('title'),
            "content": data.get('content')
        }
        POSTS.append(new_post)
        return jsonify(new_post),201

    return jsonify(POSTS)

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error':'bad request , missing some data'}),400



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
