# Jun 3-25  SBJ

import pika
import json
from datetime import datetime, timezone
import os

ARCHIVE_PATH = "archive/Y_archive.tsv"

def triage(e):
    assert e["event_type"] == "e_NewTicket"
    category = e["category"]
    priority = e["priority"]

    # Simple routing rule
    if category == "Software Issue" and priority == "High":
        assigned_to = "senior.tech@company.com"
    elif category == "Hardware Issue":
        assigned_to = "hardware.team@company.com"
    else:
        assigned_to = "helpdesk@company.com"

    y = {
        "schema": "y_TicketAssigned",
        "ticket_id": f"TKT-{hash(e['timestamp']) % 100000}",
        "assigned_to": assigned_to,
        "submitted_by": e["submitted_by"],
        "priority": priority,
        "description": e["description"],
        "status": "Open",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return y

def write_to_archive(y):
    os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)
    with open(ARCHIVE_PATH, "a") as f:
        f.write(f"{y['timestamp']}\t{json.dumps(y)}\n")

def callback(ch, method, properties, body):
    e = json.loads(body)
    if e.get("event_type") == "e_NewTicket":
        y = triage(e)
        write_to_archive(y)
        print(f"Processed ticket from {e['submitted_by']} → {y['assigned_to']}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='eventz_queue')
    channel.basic_consume(queue='eventz_queue', on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for events. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
