from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from lxml import etree
from gvm.protocols.gmpv208 import AlertCondition, AlertEvent, AlertMethod, ReportFormatType
from gvm.errors import GvmError
from logger import Logger
from logger import Logger_levels as lvl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import host_disc
import target_create
import base64
import io
import time
from pathlib import Path
from datetime import datetime, timedelta
import smtplib
from base64 import b64decode
from delete_task import delete_task, delete_target
import os


# Dane do logowania
email = os.environ.get('EMAIL')
# App password do maila
email_pass = os.environ.get('EMAIL_PASS')

log_obj = Logger("/opt/log/app.log", False)

def try_to_connect():
    while True:
        try:
            connection = TLSConnection(hostname="localhost",port=9390)
            log_obj.log("Connection established", lvl.INFO)
            return connection
        except GvmError | ConnectionRefusedError:
            log_obj.log("Connection failed. Retrying after 30s...", lvl.WARN)
            time.sleep(30)

def authenticate(gmp):
    response = gmp.authenticate("admin", "admin")
    if response.get('status') != '200':
        log_obj.log("Authentication failed", lvl.ERROR)
        return False
    log_obj.log("Authenticated to GVM", lvl.INFO)
    return True

def scan(target_name=None, hosts=None):
    # Połączenie z gvmd przez socket Unix
    connection = try_to_connect()
    transform = EtreeTransform()
    # Utworzenie obiektu protokołu GMP
    
    while True:
        try:
            with Gmp(connection=connection, transform=transform) as gmp:  
                authenticate(gmp)
                response = gmp.get_scanners()
                # Pobranie informacji o skanerach
                scanners_info = response.xpath('.//scanner')
                # Pobranie nazw skanerów
                scanner_names = [scanner.xpath('name/text()')[0] for scanner in scanners_info]
                for scanner in scanners_info:
                    if scanner.xpath('name/text()')[0] == 'OpenVAS Default':
                        # Pobranie ID skanera OpenVAS Default
                        default_scanner_id = scanner.get('id')
                log_obj.log(f"Id of default Openvas scanner: {default_scanner_id}", lvl.INFO)


                # Id konfiguracji 'Full and fast'
                config_response = gmp.get_scan_configs()
                # Pobranie informacji o konfiguracji skanowania
                configs_info = config_response.xpath('.//config')
                for config in configs_info:
                    if config.xpath('name/text()')[0] == 'Full and fast':
                        # Pobranie ID konfiguracji skanowania 'Full and fast'
                        config_id = config.get('id')



                # Stworzenie celu
                # Pobranie sieci z interfejsow
                inet_adresses = host_disc.get_inet_addresses()
                # Lista aktywnych hostow ze wszystkich interfejsow
                all_active_hosts = []
                for inet_adress in inet_adresses:
                    # Lista aktywnych hostow z poszczegolnych interfejsow
                    active_hosts = host_disc.get_active_hosts(inet_adress)
                    all_active_hosts.extend(active_hosts)
                target_id = target_create.create_target("New target1", all_active_hosts, gmp)
                
                # Stworzenie polecenia (task)
                response_task = gmp.create_task('Task1', config_id, target_id, default_scanner_id)
                task_id = response_task.get('id')
                log_obj.log(f"Task id: {task_id}", lvl.INFO)
                pretty_print(response_task)

                # Start skanu
                gmp.start_task(task_id=task_id)
                task_ready = False
                # Sprawdzenie, czy skan gotowy
                while not task_ready:
                    got_task = gmp.get_task(task_id)
                    status = got_task.find(".//status").text
                    if status == 'Done':
                        task_ready = True
                    now_time = datetime.now()
                    log_obj.log(f'{now_time.strftime("%H:%M:%S")}: {status}', lvl.INFO)
                    time.sleep(30)
                ready_task = gmp.get_task(task_id)
                report_id = ready_task.find(".//task").find('.//report').attrib.get("id")
                report = gmp.get_report(report_id=report_id, details=True, report_format_id=ReportFormatType.PDF,
                                        filter_string="apply_overrides=0 levels=hmlg rows=100 min_qod=70 first=1 sort-reverse=severity")
                report_element = report.find("report")
                content = report_element.find("report_format").tail
                binary_base64_encoded_pdf = content.encode('ascii')
                binary_pdf = b64decode(binary_base64_encoded_pdf)
                timestamp = int(time.time())
                path = f"/opt/reports/report_{timestamp}.pdf"
                pdf_path = Path(path).expanduser()
                log_obj.log(f"PDF path: {pdf_path}", lvl.INFO)
                # Zapis do pdf
                pdf_path.write_bytes(binary_pdf)
                delete_task(gmp)
                delete_target(gmp)
                log_obj.log("PDF report created", lvl.SUCCESS)
                send_email(email, email_pass, path)
                break
        except ConnectionRefusedError:
            log_obj.log("connection refused. Retrying after 30s...", lvl.WARN)
            time.sleep(30)
            continue

    




def send_email(email, email_pass, pdf_path):
    try:
        # Tworzenie połączenia z serwerem SMTP Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        try:
            # Logowanie do serwera
            server.login(email, email_pass)
        except smtplib.SMTPAuthenticationError:
            log_obj.log("Authentication failed. Please check your email and password.", lvl.ERROR)
            return
        except smtplib.SMTPException as e:
            log_obj.log(f"An SMTP error occurred during login: {e}", lvl.ERROR)
            return

        # Tworzenie wiadomości
        adresat = email
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = adresat
        msg['Subject'] = 'PDFtest'

        # Treść wiadomości
        body = "Arsenal winning the league (next season...)"
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Dodawanie pliku PDF
            with open(pdf_path, "rb") as attachment:
                part = MIMEApplication(attachment.read(), _subtype="pdf")
                part.add_header('Content-Disposition', 'attachment', filename=pdf_path)
                msg.attach(part)
        except FileNotFoundError:
            log_obj.log(f"The file {pdf_path} was not found.", lvl.ERROR)
            return
        except IOError as e:
            log_obj.log(f"An error occurred while reading the file {pdf_path}: {e}", lvl.ERROR)
            return

        try:
            # Wysyłanie wiadomości
            server.sendmail(email, adresat, msg.as_string())
        except smtplib.SMTPRecipientsRefused:
            log_obj.log("The recipient's email address was refused.", lvl.ERROR)
        except smtplib.SMTPSenderRefused:
            log_obj.log("The sender's email address was refused.", lvl.ERROR)
        except smtplib.SMTPDataError as e:
            log_obj.log(f"SMTP data error: {e}", lvl.ERROR)
        except smtplib.SMTPException as e:
            log_obj.log(f"An SMTP error occurred while sending the email: {e}", lvl.ERROR)
        else:
            log_obj.log("Message sent successfully.", lvl.SUCCESS)

        # Zamykanie połączenia
        server.quit()
        
    except smtplib.SMTPConnectError:
        log_obj.log("Failed to connect to the SMTP server.", lvl.ERROR)
    except smtplib.SMTPServerDisconnected:
        log_obj.log("The connection to the SMTP server was unexpectedly closed.", lvl.ERROR)
    except smtplib.SMTPException as e:
        log_obj.log(f"An SMTP error occurred: {e}", lvl.ERROR)
    except Exception as e:
        log_obj.log(f"An unexpected error occurred: {e}", lvl.ERROR)


if __name__ =='__main__':
    scan()







    