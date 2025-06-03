# app.py Jun 3-25 SBJ
from flask import Flask, render_template, request, redirect, url_for, session
import json
import pika
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change_this_to_something_random_and_secure'

RABBITMQ_QUEUE = 'eventz_queue'
ARCHIVE_PATH = 'archive/Y_archive.tsv'

def publish_event(event):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=json.dumps(event))
    connection.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect(url_for('submit_ticket'))
    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_ticket():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        event = {
            "event_type": "e_NewTicket",
            "submitted_by": session['email'],
            "category": request.form['category'],
            "priority": request.form['priority'],
            "description": request.form['description'],
            "timestamp": datetime.utcnow().isoformat()
        }
        publish_event(event)
        return redirect(url_for('tickets'))

    return render_template('submit.html', user_email=session['email'])

@app.route('/tickets')
def tickets():
    if 'email' not in session:
        return redirect(url_for('login'))

    user_email = session['email']
    tickets = []
    try:
        with open(ARCHIVE_PATH, 'r') as f:
            for line in f:
                _, y_json = line.strip().split('\t', 1)
                y = json.loads(y_json)
                if y.get('schema') == 'y_TicketAssigned' and y.get('submitted_by') == user_email:
                    tickets.append(y)
    except FileNotFoundError:
        pass

    return render_template('tickets.html', tickets=tickets, user_email=user_email)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
