import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from typing import Any

async def send_confirmation_email( reviewer_email: EmailStr, review_id: int,):
    """
    Background task to send a confirmation email to the reviewer.
    
    Parameters:
        - review_id (int): The ID of the newly created review.
        - reviewer_email (EmailStr): The email address of the reviewer.
    """
    # Email configuration
    sender_email = ""  # Replace with your email address
    password = ""  # Replace with your app-specific password that can be generated in gmail account.
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reviewer_email
    message["Subject"] = "Review Confirmation"

    body = f"Your review with ID {review_id} has been submitted successfully."
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, str(reviewer_email), message.as_string())
        print(f"Confirmation email sent to {reviewer_email} for review ID {review_id}")
    except Exception as e:
        print(f"Failed to send confirmation email to {reviewer_email}: {e}")

