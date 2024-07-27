from flask import Blueprint, request, jsonify, render_template
from database.banned_word import add_banned_word, remove_banned_word, get_banned_words

banned_word_bp = Blueprint('banned_word', __name__, template_folder='templates')

@banned_word_bp.route('/')
def banned_word_index():
    return render_template('banned_word.html')  # Page principale avec style

@banned_word_bp.route('/banned_words', methods=['GET'])
def banned_words():
    words = get_banned_words()
    return jsonify(words)

@banned_word_bp.route('/add', methods=['POST'])
def add_word():
    word = request.json.get('word')
    add_banned_word(word)
    return '', 200

@banned_word_bp.route('/remove', methods=['POST'])
def remove_word():
    word = request.json.get('word')
    remove_banned_word(word)
    return '', 200
