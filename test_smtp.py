# test_smtp.py
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables if using .env file
load_dotenv()

# Replace with your actual credentials
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your.email@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-app-password')

print(f"Testing connection with: {EMAIL_HOST_USER} and password {EMAIL_HOST_PASSWORD}")

try:
    # Create SMTP connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  # Identify yourself to the SMTP server
    server.starttls()  # Secure the connection
    server.ehlo()  # Re-identify yourself over TLS connection
    
    # Login to the server
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("✓ SMTP authentication successful!")
    
    # Test sending an email (optional)
    try:
        sender = EMAIL_HOST_USER
        receiver = 'test@example.com'  # Change to your test email
        message = f"""Subject: SMTP Test Email
        This is a test email sent from Python."""
        
        server.sendmail(sender, receiver, message)
        print("✓ Test email sent successfully!")
    except Exception as e:
        print(f"✗ Email sending failed: {e}")
    
    # Close the connection
    server.quit()
    
except smtplib.SMTPAuthenticationError:
    print("✗ Authentication failed. Possible reasons:")
    print("  1. Incorrect email or password")
    print("  2. Less secure apps not enabled (use App Password instead)")
    print("  3. 2-factor authentication enabled but not using App Password")
    print("  4. CAPTCHA requirement - visit: https://accounts.google.com/DisplayUnlockCaptcha")
    
except Exception as e:
    print(f"✗ SMTP connection error: {e}")