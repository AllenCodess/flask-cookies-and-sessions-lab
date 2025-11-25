from flask import Flask, jsonify, session, make_response
from models import db, Article, ArticleSchema
from flask_migrate import Migrate  # <-- add this

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)  # <-- add this


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views if not yet set
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views on every request
    session['page_views'] += 1

    # Enforce 3-article limit
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    # Fetch the article
    article = Article.query.get(id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    # Return JSON with guaranteed fields
    data = {
        "author": article.author or "",
        "title": article.title or "",
        "content": article.content or "",
        "preview": article.preview or "",
        "minutes_to_read": article.minutes_to_read or 0,
        "date": article.date.isoformat() if article.date else "",
    }

    return jsonify(data), 200

