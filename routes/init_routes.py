from routes.books_routes import book_bp

def init_routes(app):
    app.register_blueprint(book_bp, url_prefix='/books')