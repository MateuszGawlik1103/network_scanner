from scanner import send_email
import os
email = os.environ.get('EMAIL')
email_pass = os.environ.get('EMAIL_PASS')
if __name__=='__main__':
    send_email(email=email, email_pass=email_pass, pdf_path="/scanner/report.pdf")