from flask import Flask, render_template, request, redirect
import threading
from spammer import start_multi_spam, stop_spam

app = Flask(__name__)
spam_thread = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global spam_thread
    if request.method == 'POST':
        if 'start' in request.form:
            if spam_thread and spam_thread.is_alive():
                return redirect('/')  # Thread sudah berjalan, jangan jalanin lagi.

            user = request.form['username'].strip().replace("https://ngl.link/", "")
            msg = [m.strip() for m in request.form['messages'].split(',') if m.strip()]
            dur = int(request.form['duration'])
            th = int(request.form['threads'])

            spam_thread = threading.Thread(target=start_multi_spam, args=(user, msg, dur, th))
            spam_thread.start()

        elif 'stop' in request.form:
            stop_spam()

        return redirect('/')
    return render_template('index.html')

from flask import send_from_directory
import os

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
