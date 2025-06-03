# Eventz Helpdesk

**Eventz Helpdesk** is a fully functional open-source support ticket system built using the [Eventz](https://github.com/i-Technology/EventzAPI) methodology:  
> `y = F(Y, e)` — a radically simplified software architecture using immutable data tuples, zero coupling, and total traceability.

This demo proves how Eventz easily handles real-world helpdesk workflows using only:
- Flask for the GUI
- RabbitMQ for messaging
- Python Functions `F` for business logic
- Flat file archive for full auditability (no database required)

---

## 🚀 Features

✅ Email-based login (no passwords)  
✅ Submit helpdesk tickets (`e_NewTicket`)  
✅ Auto-triage & assignment (`F_TriageTicket`)  
✅ Immutable archive (`Y_archive.tsv`)  
✅ Live GUI to view submitted tickets  
✅ Decoupled architecture — Functions are short, isolated, and fully testable

---

## 📁 Project Structure

Eventz_Helpdesk/
├── app.py # Flask GUI
├── F_TriageTicket.py # Eventz Function to triage and archive tickets
├── archive/
│ └── Y_archive.tsv # Immutable data store
├── templates/ # Jinja2 HTML files
│ ├── login.html
│ ├── submit.html
│ └── tickets.html
└── .gitignore # Includes .venv and archive file

---

## 🧑‍💻 Getting Started

```bash
# Clone the repo
git clone https://github.com/i-Technology/Eventz-Helpdesk.git
cd Eventz-Helpdesk

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install flask pika

# Start the Eventz Function
python F_TriageTicket.py
# (Leave it running in a terminal)

# Start the Flask web GUI
python app.py
# Visit http://127.0.0.1:5000 in your browser

 Requirements

    Python 3.11+ (3.12+ requires pika workaround)

    RabbitMQ server running on localhost

    No SQL database needed

    No container required — Eventz is serverless-friendly

Why Eventz?

Unlike traditional ticket systems that rely on tightly coupled databases and ORM layers, Eventz uses:

    Immutable events as inputs (e)

    All past data as context (Y)

    Pure functions F to apply the rules and produce the new state (y)

    Simple. Auditable. Too simple to fail.

🙌 Contribute

This project is part of the larger EventzAPI open source effort.
Issues, pull requests, and forks are welcome!
📄 License

This project is licensed under the MIT License.
