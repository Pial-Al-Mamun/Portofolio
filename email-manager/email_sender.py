from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from data_manager import EmployeeDataManager

load_dotenv()

PASSWORD = os.environ.get("PASSWORD_EMAIL")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")


class EmployeeEmailSender(EmployeeDataManager):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = MIMEText(message, "plain")
        self.server = SMTP("smtp.gmail.com", port=587)
        self.server.starttls()
        self.server.login(EMAIL_SENDER, password=PASSWORD)

    def send_email(self, recipient: list) -> None:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join([emp["email"] for emp in recipient])
        msg["Subject"] = "Test Email"
        msg.attach(self.message)

        try:
            self.server.sendmail(EMAIL_SENDER, ", ".join(
                [emp["email"] for emp in recipient]), self.message)
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")
