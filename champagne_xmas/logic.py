import smtplib
from getpass import getpass
from email.mime.text import MIMEText



def send_email( email, roomname, vipcode ):
    sender = 'champagnexmas@gmail.com'
    receiver = email
    content = f"""Üdv,

A nemrég létrehozott szoba neve: {roomname}
és a VIP kód: {vipcode}
Oszd meg a kódot azzal akit meg akarsz hívni a névhúzásra:)

Ha nem tudod mi ez töröld nyugodtan a levelet.
Légyszi ne válaszolj, automatikus cucc.

Boldog karit!
Champagne xmas csapat"""
    
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Champagne xmas szoba létrehozás'
    smtp_server_name = 'smtp.gmail.com'
    port = '465'
    server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))

    pw = "ChampagneXmas11"
    server.login(sender, pw)
    server.send_message(msg)
    server.quit()