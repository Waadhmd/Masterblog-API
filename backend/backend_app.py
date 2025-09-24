from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder="../static")
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def find_post_by_id(posts,post_id):
     return next((post for post in posts if post['id'] == post_id), None)

@app.route('/api/posts', methods=['GET','POST'])
def handle_posts():
    """
     GET /api/posts
         - Returns all posts.
         - Supports optional query parameters:
             * sort: 'title' or 'content'
             * direction: 'asc' or 'desc'
             * page: integer page number
             * limit: integer number of posts per page
     POST /api/posts
         - Creates a new post.
         - Expects JSON body with 'title' and 'content'.
         - Returns 201 Created with the created post.
         - Returns 400 Bad Request if required fields are missing.
     """
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
    #GET request
    sort = request.args.get('sort')
    direction = request.args.get('direction','asc')

    # Validate sort params
    if (sort and sort not in ['title','content']) or (direction and direction not in ['asc','desc']):
        return jsonify({'error':'invalid sort fields or direction'}),400
    posts = POSTS[:]

    # Apply sorting if needed
    if sort in ['title','content']:
        reverse = (direction == 'desc')
        posts = sorted(posts,key=lambda post:post[sort].lower(),reverse=reverse)

    # Pagination
    page = request.args.get('page',type=int)
    limit = request.args.get('limit',type=int)
    if page and limit:
        if page < 1 and limit < 1:
            return jsonify({'error':'page and limit must be positive integers'}),400
        start_index = (page - 1) * limit
        end_index = start_index + limit
        posts = posts[start_index:end_index]


    return jsonify(posts),200


@app.route('/api/posts/<int:post_id>' , methods=['DELETE'])
def delete_post(post_id):
    """
    DELETE /api/posts/<post_id>
        - Deletes a post by ID.
        - Returns 200 OK with a success message if the post was deleted.
        - Returns 404 Not Found if the post does not exist.
    """
    # Find the post by ID
    post_to_delete = find_post_by_id(POSTS,post_id)
    if post_to_delete:
        POSTS.remove(post_to_delete)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"message": "Requested post doesn't exist!"}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    PUT /api/posts/<post_id>
        - Updates a post by ID.
        - Expects JSON body with optional 'title' and/or 'content'.
        - Returns 200 OK with the updated post if successful.
        - Returns 404 Not Found if the post does not exist.
    """
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
    """
    GET /api/posts/search
        - Searches posts by 'title' and/or 'content' query parameters.
        - Returns 200 OK with a list of posts matching the search terms.
        - Returns an empty list if no posts match.
    """
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

# Swagger setup
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
