import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import threading
import time

email = 'cs22btech11030@iith.ac.in'
password = 'ghflvekncsgrsdzt'
send_to_email = 'kvtuhil@gmail.com'
subject = 'Paper Presentation - Participation Certificate'
message = 'Thank you for your participation in the Paper Presentation event, by elan and nvision IIT Hyderabad! Please find the attached participation certificate.'
file_location = "C:/Users/kaipa/Downloads/PP, Sugar, Robo, Pro/JPEG/"

names_file_path = "C:/Users/kaipa/Desktop/Tuhil/Misc/PPParticipants.csv"
names_file = open(names_file_path, "r")
names_and_emails = [(x.split(",")[0].strip(), x.split(",")[-1].strip()) for x in names_file.readlines()]

sent = [0 for x in range(75)]

def send_mail(i):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #print(i, "starting tls")
    server.starttls()
    #print(i, "Logging in...")
    server.login(email, password)

    file_path = file_location + "Paper Presentation_" + names_and_emails[i][0] + ".jpg"
    #send_to_email = names_and_emails[i][1]

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = os.path.basename(file_path)
    attachment = open(file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    # print("reading file")
    part.set_payload(attachment.read())
    attachment.close()

    # print("encoding")
    encoders.encode_base64(part)
    # print("adding header")
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # print("attaching part to message")
    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)
    # print("done")

    text = msg.as_string()
    # print("sending...")
    print(i, "sending \"", file_path.split("/")[-1], "\" to", send_to_email)
    #server.sendmail(email, send_to_email, text)
    print(i, "- Sent")
    server.quit()
    sent[i] = 1

threads = []
number_of_threads_init = 0
while number_of_threads_init < 75:
    j = 0
    while j < len(threads):
        if not threads[j].is_alive():
            threads.pop(j)
        j += 1

    if len(threads) >= 10:
        time.sleep(1)
        continue

    thread1 = threading.Thread(target=send_mail, args=(number_of_threads_init,))
    thread1.start()
    threads.append(thread1)
    number_of_threads_init += 1

while len(threads) != 0:
    j = 0
    while j < len(threads):
        if not threads[j].is_alive():
            threads.pop(j)
        j += 1
for i in range(75):
    if sent[i]:
        print(i)
    else:
        print(i, "- not sent")