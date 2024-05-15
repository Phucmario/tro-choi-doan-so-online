from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, send
import random
import time
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

target_number = random.randint(1, 3)
players = {}
first_guess_times = {}
winner = None
game_over = False
round_count = 1
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', players=players, winner=winner, game_over=game_over, round_count=round_count)

@app.route('/guess', methods=['POST'])
def guess_number():
    global target_number, winner, game_over, round_count

    guess = int(request.form['guess'])
    player = request.form['player']

    if player not in players:
        players[player] = 0
        first_guess_times[player] = None

    if guess > target_number:
        message = f"Số của {player} đoán lớn hơn số cần tìm! Số {player} vừa đoán là {guess}."
    elif guess < target_number:
        message = f" Số của {player} đoán nhỏ hơn số cần tìm! Số {player} vừa đoán là {guess}."
    else:
        message = f"Chúc mừng  {player}!  Đã đoán đúng số {target_number}. Chúng ta qua vòng mới nào"
        players[player] += 1

        if first_guess_times[player] is None:
            first_guess_times[player] = time.time()

        if players[player] >= 5 and winner is None:
            winner = player
            message += f" Người chơi {winner} đã đạt được 5 điểm và trở thành người chiến thắng!"
            game_over = True
            socketio.emit('refresh') 

        target_number = random.randint(1, 3)
        round_count += 1

    socketio.emit('message', message)

    return jsonify(message=message, players=players, winner=winner, game_over=game_over, round_count=round_count)

@app.route('/restart', methods=['GET'])
def restart_game():
    global target_number, winner, game_over, round_count, players, first_guess_times

    target_number = random.randint(1, 3)
    players = {}
    first_guess_times = {}
    winner = None
    game_over = False
    round_count = 1

    return render_template('index.html', players=players, winner=winner, game_over=game_over, round_count=round_count)

@socketio.on('message')
def handle_message(message):
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    print(f"Server is running at http://{host_ip}:5000")
    socketio.run(app, host='0.0.0.0')
