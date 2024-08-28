import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ['SENDER_EMAIL']
SENDER_PASSWORD = os.environ['SENDER_PASSWORD']

# List of recipients
RECIPIENTS = [
    "abrahamalex9684@gmail.com",
    "harriswellington61@gmail.com",
    "saniabubakarsani2018@gmail.com"
]

# File paths
INDEX_FILE = 'current_index.txt'
DATE_FILE = 'last_sent_date.txt'

def send_email(recipient, message):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = "Reminder: Time to Refill the Room Cooler with Water"
    
    msg.attach(MIMEText(message, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def get_current_index():
    try:
        with open(INDEX_FILE, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def update_index(new_index):
    with open(INDEX_FILE, 'w') as f:
        f.write(str(new_index))

def get_last_sent_date():
    try:
        with open(DATE_FILE, 'r') as f:
            date_str = f.read().strip()
            return datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
    except FileNotFoundError:
        return None

def update_last_sent_date(date):
    with open(DATE_FILE, 'w') as f:
        f.write(date.strftime('%Y-%m-%d'))

def main():
    today = datetime.now().date()
    last_sent_date = get_last_sent_date()
    
    # Check if it's time to send an email
    if last_sent_date is None or (today - last_sent_date).days >= 2:
        current_index = get_current_index()
        recipient = RECIPIENTS[current_index]
        
        message = "Hello! It's your turn to refill the water cooler today. Thank you!"
        send_email(recipient, message)
        
        next_index = (current_index + 1) % len(RECIPIENTS)
        update_index(next_index)
        update_last_sent_date(today)
        
        print(f"Email sent to {recipient}")
    else:
        print("Skipping today as the last email was sent less than two days ago.")

if __name__ == "__main__":
    main()
