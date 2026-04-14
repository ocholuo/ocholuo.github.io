# selenium is picked because of the dynamically loaded content
# otherwise, you would only get the page source and not the content the javascript loads
import os
import smtplib
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email(subject, body):
    msg = MIMEText(str(body))
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(EMAIL, PASSWORD)
        smtp_server.sendmail(EMAIL, recipients, msg.as_string())
    print("Message sent!")


op = webdriver.ChromeOptions()
op.add_argument("--headless")  # fixed: was missing '--'
op.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
driver = webdriver.Chrome(options=op)


# kirkland irons
#   https://www.costco.com/kirkland-signature-7-piece-players-iron-set%2C-right-handed.product.4000236767.html
# kirkland putter
#   https://www.costco.com/kirkland-signature-ks1-putter---right-handed-.product.100645850.html

# change link here
link = "https://www.costco.com/kirkland-signature-7-piece-players-iron-set%2C-right-handed.product.4000236767.html"

# change your email to here
recipients = [""]

# change the message here
msg = ""

driver.get(link)

try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-btn"))
    )
    button_html = element.get_attribute("outerHTML")

    out_of_stock = 'value="Out of Stock"'
    in_stock = 'value="Add to Cart"'
    if out_of_stock in button_html:
        print("out of stock")
    elif in_stock in button_html:
        send_email("in_stock", msg)
    else:
        send_email("error", "incorrect link")
except Exception as e:
    send_email("error", str(e))  # fixed: convert exception to string

finally:
    driver.quit()
