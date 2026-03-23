#!/usr/bin/env python3
import os, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER     = os.environ["GMAIL_USER"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]
CHAT_LINK      = "https://claude.ai"
RECIPIENTS     = ["lucascasamento@alyssagrayrealty.com","drewyaffe@alyssagrayrealty.com"]

def get_reminder_date(year, month):
    the_15th = datetime.date(year, month, 15)
    return the_15th - datetime.timedelta(days=the_15th.weekday())

def should_send_today():
    today = datetime.date.today()
    return today == get_reminder_date(today.year, today.month)

def send_reminder():
    today = datetime.date.today()
    month_str = today.strftime("%B %Y")
    prev_month = (today.replace(day=1) - datetime.timedelta(days=1)).strftime("%B %Y")
    prev_month_short = (today.replace(day=1) - datetime.timedelta(days=1)).strftime("%B")

    prompt = f"""I am dropping 3 files for the monthly Outstanding Balance Report at Alyssa Gray Realty. Please build the report automatically.

FILES I AM DROPPING:
1. Outstanding Balances CSV
2. Leases / Rent Roll CSV
3. {prev_month_short} Excel report (last month)

REPORT RULES:
- Include only tenants where Balance > 1.25x their monthly rent (match by account number from rent roll)
- Sort highest balance to lowest
- Columns: Tenants | Unit | More than 1 month? | Balance | Responsible | Comments {month_str} | Comments {prev_month}
- Comments {month_str} = blank
- Comments {prev_month} = pulled from prior month Excel matched by account number
- Rows where Responsible = Pappas: highlight light gray
- No other row shading, left/top aligned, dark blue header and total row, Arial font, balance in dollar format
- Sheet name: OutstandingLeaseBalances_YYYYMM

AFTER BUILDING:
Email the Excel file as attachment to lucascasamento@alyssagrayrealty.com and drewyaffe@alyssagrayrealty.com
Gmail SMTP: user=lucascasamento33@gmail.com, app password=zfvkpooevppebuyt, smtp.gmail.com:465
Subject: Outstanding Balance Report - {month_str}"""

    body_html = f"""<div style="font-family:Georgia,serif;max-width:600px;margin:0 auto;padding:24px;background:#f5f0e8">
  <div style="border-bottom:3px double #1a1410;padding-bottom:16px;margin-bottom:20px;text-align:center">
    <div style="font-family:sans-serif;font-size:36px;font-weight:900;letter-spacing:4px">BALANCE <span style="color:#1F4E79">REPORT</span></div>
    <div style="font-size:12px;color:#7a7060;margin-top:6px;font-style:italic">{month_str} - Monthly Reminder</div>
  </div>
  <p style="font-size:15px;line-height:1.7;color:#1a1410;margin-bottom:16px">Hey guys - time to run the <strong>{month_str} Outstanding Balance Report</strong>.</p>
  <p style="font-size:14px;color:#1a1410;margin-bottom:6px"><strong>Step 1</strong> &mdash; Gather these 3 files:</p>
  <div style="background:#ede8e0;border-left:4px solid #1F4E79;padding:16px 20px;margin-bottom:20px;font-family:sans-serif;font-size:13px;color:#1a1410;line-height:2">
    <div>1. Outstanding Balances CSV</div>
    <div>2. Leases / Rent Roll CSV</div>
    <div>3. {prev_month_short} Excel report (last month)</div>
  </div>
  <p style="font-size:14px;color:#1a1410;margin-bottom:6px"><strong>Step 2</strong> &mdash; Open a new Claude chat:</p>
  <a href="{CHAT_LINK}" style="display:block;background:#1F4E79;color:white;text-align:center;padding:14px;font-size:16px;text-decoration:none;letter-spacing:2px;font-family:sans-serif;font-weight:700;margin-bottom:20px">OPEN CLAUDE CHAT</a>
  <p style="font-size:14px;color:#1a1410;margin-bottom:8px"><strong>Step 3</strong> &mdash; Drop the 3 files then copy and paste this prompt:</p>
  <div style="background:#fffdf0;border:2px solid #c8a800;border-radius:4px;margin-bottom:16px">
    <div style="background:#c8a800;padding:10px 16px;font-family:sans-serif;font-size:11px;font-weight:700;color:#fff;letter-spacing:1px">COPY THIS PROMPT &darr;</div>
    <div style="padding:16px;font-family:monospace;font-size:12px;color:#1a1410;line-height:1.9;white-space:pre-wrap">{prompt}</div>
  </div>
  <p style="font-size:12px;color:#7a7060;text-align:center">The report will be built and emailed to you and Drew automatically.</p>
  <div style="margin-top:24px;padding-top:16px;border-top:1px solid #d8d0c0;font-size:11px;color:#c8c0b0;text-align:center">Alyssa Gray Realty &mdash; {month_str}</div>
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

def main():
    if should_send_today():
        send_reminder()
    else:
        today = datetime.date.today()
        r = get_reminder_date(today.year, today.month)
        print(f"Not reminder day. Next: {r.strftime('%A, %B %-d, %Y')}")

if __name__ == "__main__":
    main()
