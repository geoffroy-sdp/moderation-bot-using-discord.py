from flask import Flask, render_template
from webpage.app_banned_word.app_word import banned_word_bp
from webpage.app_history.app_history import history_bp
from webpage.app_history_commands.app_commands import commands_bp
from webpage.app_role.app_role import roles_bp

app = Flask(__name__, template_folder="webpage")

# Register blueprints
app.register_blueprint(banned_word_bp, url_prefix='/banned_word')
app.register_blueprint(history_bp, url_prefix='/history')
app.register_blueprint(commands_bp, url_prefix='/commands')
app.register_blueprint(roles_bp, url_prefix='/roles')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
