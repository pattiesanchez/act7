import os
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def sendMail(html, assunto, para):
    servidor = os.getenv("SMTP_SERVER")
    porta = int(os.getenv("SMTP_PORT", "587"))
    usuario = os.getenv("SMTP_USER")
    senha = os.getenv("SMTP_PASSWORD")
    remetente = os.getenv("SMTP_FROM", "contato@act7.test")

    if not all([servidor, usuario, senha]):
        raise ValueError("Configurações SMTP incompletas no .env")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = para
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(servidor, porta, timeout=10) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(usuario, senha)
        server.sendmail(remetente, [para], msg.as_string())