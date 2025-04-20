def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.learning import learning_bp
    from routes.chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(chatbot_bp)