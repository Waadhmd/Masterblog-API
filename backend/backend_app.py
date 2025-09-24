from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def find_post_by_id(posts,post_id):
     return next((post for post in posts if post['id'] == post_id), None)

@app.route('/api/posts', methods=['GET','POST'])
def handle_posts():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title') if data else None
        content = data.get('content') if data else None
        # Validate required fields
        missing_fields = []
        if not title.strip():
            missing_fields.append("title")
        if not content.strip():
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

    sort = request.args.get('sort')
    direction = request.args.get('direction','asc')
    if (sort and sort not in ['title','content']) or (direction and direction not in ['asc','desc']):
        return jsonify({'error':'invalid sort fields or direction'}),400
    if sort in ['title','content']:
        reverse = (direction == 'desc')
        sorted_list = sorted(POSTS,key=lambda post:post[sort].lower(),reverse=reverse)
        return jsonify(sorted_list),200

    return jsonify(POSTS),200


@app.route('/api/posts/<int:post_id>' , methods=['DELETE'])
def delete_post(post_id):
    # Find the post by ID
    post_to_delete = find_post_by_id(POSTS,post_id)
    if post_to_delete:
        POSTS.remove(post_to_delete)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"message": "Requested post doesn't exist!"}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_to_update = find_post_by_id(POSTS,post_id)
    if post_to_update:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if title is not None and isinstance(title, str) and title.strip():
          post_to_update['title'] = title.strip()
        if content is not None and isinstance(content, str) and content.strip():
          post_to_update['content'] = content.strip()

        return jsonify({
        "id": post_id,
        "title": f"{post_to_update['title']}",
        "content": f"{post_to_update['content']}"
        }),200
    return jsonify({"message": "Requested post doesn't exist!"}), 404

@app.route('/api/posts/search',methods=['GET'])
def handle_search():
    title = request.args.get('title', '').strip()
    content = request.args.get('content', '').strip()
    if not title and not content:
        return jsonify([]), 200

    results = [
        post for post in POSTS
        if (title and title.lower() in post['title'].lower())
        or (content and content.lower() in post['content'].lower())
             ]
    return jsonify(results),200


@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error':'bad request , missing some data'}),400



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
