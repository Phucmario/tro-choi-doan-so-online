from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)
target_number = random.randint(1, 3)
players = {}  # Số người chơi và điểm của họ
first_guess_times = {}  # Thời điểm đoán đầu tiên của mỗi người chơi
winner = None  # Người chiến thắng
game_over = False  # Trạng thái kết thúc trò chơi
round_count = 1  # Số vòng chơi, khởi tạo là 1

@app.route('/', methods=['GET', 'POST'])
def guess_number():
    global target_number, winner, game_over, round_count  # Thêm dòng này để có thể thay đổi giá trị biến toàn cục

    if request.method == 'POST':
        guess = int(request.form['guess'])
        player = request.form['player']

        if player not in players:
            players[player] = 0
            first_guess_times[player] = None

        if guess > target_number:
            message = "Số của bạn đoán lớn hơn số cần tìm."
        elif guess < target_number:
            message = "Số của bạn đoán nhỏ hơn số cần tìm."
        else:
            message = f"Chúc mừng! Bạn đã đoán đúng số {target_number}."
            players[player] += 1

            if first_guess_times[player] is None:
                first_guess_times[player] = time.time()

            if players[player] >= 5 and winner is None:  # Kiểm tra nếu người chơi đã đạt đủ 5 điểm và chưa có người chiến thắng
                winner = player
                message += f" Người chơi {winner} đã đạt được 5 điểm và trở thành người chiến thắng!"
                game_over = True

            target_number = random.randint(1, 3)  # Sinh số mới
            round_count += 1  # Tăng số vòng chơi

        return render_template('index.html', message=message, players=players, winner=winner, game_over=game_over, round_count=round_count)

    return render_template('index.html', players=players, winner=winner, game_over=game_over, round_count=round_count)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')