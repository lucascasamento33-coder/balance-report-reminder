#!/usr/bin/env python3
import os, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER     = os.environ["GMAIL_USER"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]
CHAT_LINK      = "https://claude.ai/chat/fab9a4af-2461-4006-b33f-95cefbef29ef"
RECIPIENTS     = ["lucascasamento@alyssagrayrealty.com", "drewyaffe@alyssagrayrealty.com"]

today = datetime.date.today()
month_str = today.strftime("%B %Y")
prev_month = (today.replace(day=1) - datetime.timedelta(days=1)).strftime("%B")

body_html = f"""
<div style="font-family:Georgia,serif;max-width:500px;margin:0 auto;padding:24px;background:#f5f0e8">
  <div style="border-bottom:3px double #1a1410;padding-bottom:16px;margin-bottom:20px;text-align:center">
    <div style="font-family:sans-serif;font-size:36px;font-weight:900;letter-spacing:4px;line-height:1">
      BALANCE <span style="color:#1F4E79">REPORT</span>
    </div>
    <div style="font-size:12px;color:#7a7060;margin-top:6px;font-style:italic">{month_str} - Monthly Reminder</div>
  </div>
  <p style="font-size:15px;line-height:1.7;color:#1a1410;margin-bottom:16px">
    Hey guys - time to run the <strong>{month_str} Outstanding Balance Report</strong>. Please drop the following 3 files in the chat:
  </p>
  <div style="background:#ede8e0;border-left:4px solid #1F4E79;padding:16px 20px;margin-bottom:20px;font-family:sans-serif">
    <div style="font-size:13px;color:#1a1410;line-height:2">
      <div>1. Outstanding Balances CSV - exported from the system</div>
      <div>2. Leases / Rent Roll CSV - current rent roll</div>
      <div>3. Last Month Report - the {prev_month} Excel file for old comments</div>
    </div>
  </div>
  <a href="{CHAT_LINK}" style="display:block;background:#1F4E79;color:white;text-align:center;padding:14px;font-size:16px;text-decoration:none;letter-spacing:2px;font-family:sans-serif;font-weight:700;margin-bottom:16px">
    OPEN CHAT TO DROP FILES
  </a>
  <p style="font-size:13px;color:#7a7060;line-height:1.7;text-align:center">
    Drop the 3 files in the chat and the report will be built and emailed back automatically.
  </p>
</div>"""

msg = MIMEMultipart("alternative")
msg["Subject"] = f"Outstanding Balance Report - {month_str} files needed"
msg["From"]    = GMAIL_USER
msg["To"]      = ", ".join(RECIPIENTS)
msg.attach(MIMEText(body_html, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
    s.login(GMAIL_USER, GMAIL_APP_PASS)
    s.sendmail(GMAIL_USER, RECIPIENTS, msg.as_string())

print(f"Reminder sent to {', '.join(RECIPIENTS)} for {month_str}")
