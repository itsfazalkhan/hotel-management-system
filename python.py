import smtplib
 
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s.starttls()
 
# Authentication
s.login("app.hotel.management@gmail.com", "rwjahncjmzdqkzcc")
 
# message to be sent
message = "Test Message"
 
# sending the mail
s.sendmail("app.hotel.management@gmail.com", "ggl.acc007@gmail.com", message)
 
# terminating the session
s.quit()