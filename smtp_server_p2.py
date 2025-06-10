# Import needed tools
import socket  # For network connection
import base64  # For encoding username/password
import ssl     # For secure connection
import email.utils  # For proper email formatting

def send_email(server, port, from_addr, to_addr, username, password, subject, body):
    # Set up connection and error handling
    connection = None
    try:
        # STEP 1: Connect to the email server
        # Create network socket (like opening a phone line)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(10)  # Don't wait forever
        
        # Connect to server (like dialing the number)
        connection.connect((server, port))
        print("Server said:", connection.recv(1024).decode().strip())

        # Helper function to send commands
        def send_command(command, expected_code):
            # Send command and check response
            connection.sendall((command + "\r\n").encode())
            reply = connection.recv(1024).decode()
            if not reply.startswith(str(expected_code)):
                raise Exception(f"Oops! Expected {expected_code}, got: {reply}")
            return reply

        # STEP 2: Start conversation
        send_command(f"EHLO {socket.gethostname()}", 250)
        
        # STEP 3: Make connection secure
        send_command("STARTTLS", 220)
        connection = ssl.create_default_context().wrap_socket(
            connection, 
            server_hostname=server
        )
        
        # Say hello again securely
        send_command(f"EHLO {socket.gethostname()}", 250)

        # STEP 4: Login
        send_command("AUTH LOGIN", 334)
        # Encode username/password (like secret code)
        send_command(base64.b64encode(username.encode()).decode(), 334)
        send_command(base64.b64encode(password.encode()).decode(), 235)

        # STEP 5: Set up email
        send_command(f"MAIL FROM: <{from_addr}>", 250)
        send_command(f"RCPT TO: <{to_addr}>", 250)
        send_command("DATA", 354)

        # STEP 6: Build email content
        # Important headers to avoid spam
        email_content = f"Date: {email.utils.formatdate()}\r\n"
        email_content += f"From: <{from_addr}>\r\n"
        email_content += f"To: <{to_addr}>\r\n"
        email_content += f"Subject: {subject}\r\n"
        email_content += f"Message-ID: {email.utils.make_msgid()}\r\n"  # Unique ID
        email_content += "Content-Type: text/plain; charset=utf-8\r\n\r\n"  # Text format
        
        # Fix body formatting
        safe_body = body.replace("\n", "\r\n")
        safe_body = safe_body.replace("\r\n.\r\n", "\r\n..\r\n")  # Stop early endings
        email_content += safe_body + "\r\n.\r\n"  # End marker

        # STEP 7: Send everything
        connection.sendall(email_content.encode())
        print("Last reply:", connection.recv(1024).decode().strip())

        # STEP 8: Clean exit
        send_command("QUIT", 221)
        connection.close()
        print("Email sent! Check inbox!")

    except Exception as error:
        print(f"Uh oh! Problem: {error}")
        if connection:
            connection.close()

# Usage remains the same
send_email(
    server="smtp.gmail.com",
    port=587,
    from_addr="zeiosfifa234@gmail.com",
    to_addr="ahmedhisham3k2@gmail.com",
    username="zeiosfifa234@gmail.com",
    password="tirdgjwnigybyqxc",
    subject="Important: Inbox Test",
    body=("This is a test email that should appear in the inbox\n")
)