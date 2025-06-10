# SMTP-server
Its an SMTP server created using python code

SMTP Project: Code Explanation (English and Arabic)
import socket
• Allows the program to communicate over the network like making a phone call. (يتيح للبرنامج التواصل عبر الشبكة مثل إجراء مكالمة هاتفية)
import base64
• Encodes sensitive data like usernames and passwords in a safer way. (يُشفر البيانات الحساسة مثل اسم المستخدم وكلمة المرور بطريقة أكثر أمانًا)
import ssl
• Adds security to the connection, similar to HTTPS on websites. (يضيف الأمان للاتصال، مثل HTTPS في المواقع الإلكترونية)
import email.utils
• Helps format email components like date and message ID. (يساعد في تنسيق مكونات البريد الإلكتروني مثل التاريخ ومعرّف الرسالة)
def send_email(server, port, from_addr, to_addr, username, password, subject, body):
• Defines a function to send an email using an SMTP server. (يُعرّف دالة لإرسال بريد إلكتروني باستخدام خادم SMTP)
    connection = None
• Creates an empty connection variable to use later. (يُنشئ متغير اتصال فارغ لاستخدامه لاحقًا)
    try:
• Starts a block of code to catch errors if something goes wrong. (يبدأ كتلة كود لمعالجة الأخطاء إذا حدث شيء خاطئ)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
• Opens a connection using IPv4 and TCP. (يفتح اتصال باستخدام IPv4 و TCP)
        connection.settimeout(10)
• Sets a timeout of 10 seconds in case of delay. (يحدد مهلة 10 ثوانٍ في حالة حدوث تأخير)
        connection.connect((server, port))
• Connects to the server using its address and port. (يتصل بالخادم باستخدام عنوانه والمنفذ)
        print("Server said:", connection.recv(1024).decode().strip())
• Shows the welcome message from the server. (يعرض رسالة الترحيب من الخادم)
        def send_command(command, expected_code):
• A helper function to send commands and check server responses. (دالة مساعدة لإرسال الأوامر والتحقق من رد الخادم)
            connection.sendall((command + "\r\n").encode())
• Sends a command to the server. (يرسل أمرًا إلى الخادم)
            reply = connection.recv(1024).decode()
• Gets the server's reply. (يحصل على رد الخادم)
            if not reply.startswith(str(expected_code)):
• Checks if the reply is what we expected. (يتحقق مما إذا كان الرد كما هو متوقع)
                raise Exception(f"Oops! Expected {expected_code}, got: {reply}")
• Raises an error if the reply isn’t correct. (يُظهر خطأ إذا لم يكن الرد صحيحًا)
        send_command(f"EHLO {socket.gethostname()}", 250)
• Introduces the client to the server. (يُعرّف العميل إلى الخادم)
        send_command("STARTTLS", 220)
• Requests to upgrade to a secure connection. (يطلب ترقية الاتصال ليصبح آمنًا)
        connection = ssl.create_default_context().wrap_socket(connection, server_hostname=server)
• Wraps the socket in SSL for encryption. (يُغلف الاتصال بالتشفير باستخدام SSL)
        send_command(f"EHLO {socket.gethostname()}", 250)
• Says hello again securely. (يقول مرحبًا مرة أخرى ولكن بأمان)
        send_command("AUTH LOGIN", 334)
• Starts login process. (يبدأ عملية تسجيل الدخول)
        send_command(base64.b64encode(username.encode()).decode(), 334)
• Sends username in encoded format. (يرسل اسم المستخدم بصيغة مشفرة)
        send_command(base64.b64encode(password.encode()).decode(), 235)
• Sends password in encoded format. (يرسل كلمة المرور بصيغة مشفرة)
        send_command(f"MAIL FROM: <{from_addr}>", 250)
• Tells the server who is sending the email. (يخبر الخادم بمن يرسل البريد)
        send_command(f"RCPT TO: <{to_addr}>", 250)
• Tells the server who will receive the email. (يخبر الخادم بمن سيتلقى البريد)
        send_command("DATA", 354)
• Prepares to send the email content. (يستعد لإرسال محتوى البريد)
        email_content = f"Date: {email.utils.formatdate()}\r\n"
• Adds the current date. (يضيف التاريخ الحالي)
        email_content += f"From: <{from_addr}>\r\n"
• Adds sender email. (يضيف بريد المرسل)
        email_content += f"To: <{to_addr}>\r\n"
• Adds recipient email. (يضيف بريد المستلم)
        email_content += f"Subject: {subject}\r\n"
• Adds the subject. (يضيف الموضوع)
        email_content += f"Message-ID: {email.utils.make_msgid()}\r\n"
• Adds unique message ID. (يضيف معرف فريد للرسالة)
        email_content += "Content-Type: text/plain; charset=utf-8\r\n\r\n"
• Sets content type to plain text. (يحدد نوع المحتوى كنص عادي)
        safe_body = body.replace("\n", "\r\n")
• Formats the message body properly. (ينسق نص الرسالة بشكل صحيح)
        safe_body = safe_body.replace("\r\n.\r\n", "\r\n..\r\n")
• Avoids early message termination. (يتجنب إنهاء الرسالة قبل الوقت)
        email_content += safe_body + "\r\n.\r\n"
• Marks the end of the message. (يحدد نهاية الرسالة)
        connection.sendall(email_content.encode())
• Sends the email to the server. (يرسل البريد الإلكتروني إلى الخادم)
        print("Last reply:", connection.recv(1024).decode().strip())
• Shows the final response from the server. (يعرض آخر رد من الخادم)
        send_command("QUIT", 221)
• Politely ends the session. (ينهي الجلسة بأدب)
        connection.close()
• Closes the connection. (يغلق الاتصال)
        print("Email sent! Check inbox!")
• Confirms the email was sent. (يؤكد أن البريد تم إرساله)
    except Exception as error:
• Handles any problems. (يعالج أي مشاكل)
        print(f"Uh oh! Problem: {error}")
• Shows the error message. (يعرض رسالة الخطأ)
        if connection:
• If connection was opened... (إذا تم فتح الاتصال...)
            connection.close()
• ...then close it. (...أغلقه)
