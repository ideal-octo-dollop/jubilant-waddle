def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.learning import learning_bp
    from routes.chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/')  # Note the '/' prefix
    app.register_blueprint(learning_bp, url_prefix='/learning')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')