import time
from app.worker.celery_app import celery_app


@celery_app.task(name="send_booking_confirmation_email")
def send_booking_confirmation_email(email: str, booking_id: str):
    """
    Simulates sending an email notification.
    Executed asynchronously by Celery.
    """
    print(f"📨 START sending email to {email} for booking {booking_id}...")

    # Simulating network delay
    time.sleep(5)

    print(f"✅ EMAIL SENT to {email} successfully!")
    return f"Email sent to {email}"
