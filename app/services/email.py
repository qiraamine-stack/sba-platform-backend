import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "qiraamine@gmail.com")

def send_new_user_notification(user_email: str, user_name: str, role: str):
    try:
        resend.Emails.send({
            "from": "BuyWithSBA <onboarding@resend.dev>",
            "to": ADMIN_EMAIL,
            "subject": f"New User Registered - {user_name}",
            "html": f"""
            <h2>New User Registration</h2>
            <p><strong>Name:</strong> {user_name}</p>
            <p><strong>Email:</strong> {user_email}</p>
            <p><strong>Role:</strong> {role}</p>
            <p><strong>Platform:</strong> buywithsba.com</p>
            """
        })
    except Exception as e:
        print(f"Email error: {e}")

def send_new_listing_notification(title: str, asking_price: float, seller_name: str, seller_email: str, industry: str):
    try:
        resend.Emails.send({
            "from": "BuyWithSBA <onboarding@resend.dev>",
            "to": ADMIN_EMAIL,
            "subject": f"New Listing Created - {title}",
            "html": f"""
            <h2>New Business Listing</h2>
            <p><strong>Title:</strong> {title}</p>
            <p><strong>Asking Price:</strong> ${asking_price:,.0f}</p>
            <p><strong>Industry:</strong> {industry}</p>
            <p><strong>Seller:</strong> {seller_name}</p>
            <p><strong>Seller Email:</strong> {seller_email}</p>
            <p><strong>Platform:</strong> buywithsba.com</p>
            """
        })
    except Exception as e:
        print(f"Email error: {e}")
