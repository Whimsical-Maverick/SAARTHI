from flask import Flask

def create_app():
    app = Flask(__name__,instance_relative_config=True)#this makes flask search for all the secrets in the instance folder not the root app folder
    app.config.from_object("app.config.Config")#loads the default secret params from a class Config in config.py
    app.config.from_pyfile("config.py",silent=True)#replaces the old config files with new one if present
    from app.routes.main import main_bp as main_blueprint
    from app.routes.BuddyBot import BuddyBot_bp as BuddyBot_blueprint
    from app.routes.chat import chat_bp as chat_blueprint
    from app.routes.get_emotion import get_emotion_bp as get_emotion_blueprint
    from app.routes.get_movie import get_movie_bp as get_movie_blueprint
    from app.routes.get_music  import get_music_bp as get_music_blueprint
    from app.routes.movies import movies_bp as movies_blueprint
    from app.routes.start_feed import start_feed_bp as start_feed_blueprint
    from app.routes.stop_feed import stop_feed_bp as stop_feed_blueprint
    from app.routes.talk import talk_bp as talk_blueprint
    from app.routes.video_feed import video_bp as video_blueprint
    from app.routes.welcome import welcome_bp as welcome_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(BuddyBot_blueprint)
    app.register_blueprint(chat_blueprint)
    app.register_blueprint(get_emotion_blueprint)
    app.register_blueprint(get_movie_blueprint)
    app.register_blueprint(get_music_blueprint)
    app.register_blueprint(movies_blueprint)
    app.register_blueprint(start_feed_blueprint)
    app.register_blueprint(stop_feed_blueprint)
    app.register_blueprint(talk_blueprint)
    app.register_blueprint(video_blueprint)
    app.register_blueprint(welcome_blueprint)
    return app
