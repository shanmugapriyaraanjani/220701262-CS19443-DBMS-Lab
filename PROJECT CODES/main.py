from cryptography.fernet import Fernet
import smtplib
from email.message import EmailMessage
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# Set up the email details
login_mail = "220701262@rajalakshmi.edu.in"
password = "shpriya05"
sender_email = login_mail
receiver_email = "220701216@rajalakshmi.edu.in"
subject = input("Enter subject:") 
message_body = input("Enter your message:")

# Generate a 256-bit (32-byte) AES key
key = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    iterations=100000,
    salt=b'salt_value',
    length=32  # AES-256 key length
).derive(b'password')

# Ensure the message body is a multiple of 16 bytes (AES block size)
message_body = message_body.ljust((len(message_body) // 16 + 1) * 16)

# Encrypt the message using AES


cipher = Cipher(algorithms.AES(key))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(message_body.encode()) + encryptor.finalize()

# Create an EmailMessage object
message = EmailMessage()
message.set_content(ciphertext.decode('latin-1'))  # Ensure it's a str, not bytes
message['Subject'] = subject
message['From'] = sender_email
message['To'] = receiver_email

# Send the email
try:
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login(login_mail, password)
    smtp_obj.send_message(message)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
finally:
    smtp_obj.quit()

