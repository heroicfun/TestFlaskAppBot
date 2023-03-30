import sqlite3
from flask import Flask, redirect, render_template, send_from_directory
from middlewares.MethodOverrideMiddleware import HTTPMethodOverrideMiddleware

app = Flask(__name__)
method_override = HTTPMethodOverrideMiddleware(app.wsgi_app)


# Define the homepage route handler
@app.route('/')
def index():
    return render_template('index.html')


# Define the registration endpoint
@app.route('/register-with-bot', methods=['GET'])
def register_with_bot():
    return redirect('https://t.me/TestFlaskAppBot')


# Define the account page
@app.route('/account/<nickname>')
def account(nickname):
    # Get the user data from the database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    select_query = "SELECT * FROM users WHERE nickname = ?"
    data = (nickname,)
    cursor.execute(select_query, data)
    result = cursor.fetchone()
    if result:
        user_id, username, nickname, phone_number, avatar_path = result
        return render_template('account.html', username=username, nickname=nickname,
                               phone_number=phone_number, avatar_path=avatar_path)
    else:
        return "User not found"


@app.route("/avatars/<avatar_path>")
def view_image(avatar_path):
    return send_from_directory('avatars', avatar_path)


if __name__ == '__main__':
    app.run()
