import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
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
        with open('current_index.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
def update_index(new_index):
    with open('current_index.txt', 'w') as f:
        f.write(str(new_index))
def main():
    current_index = get_current_index()
    recipient = RECIPIENTS[current_index]
    
    message = f"Hello! It's your turn to refill the water cooler today. Thank you!"
    send_email(recipient, message)
    
    next_index = (current_index + 1) % len(RECIPIENTS)
    update_index(next_index)
    
    print(f"Email sent to {recipient}")
if __name__ == "__main__":
    main()
