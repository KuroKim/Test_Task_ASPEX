import time
from app.worker.celery_app import celery_app


@celery_app.task(name="send_booking_confirmation_email")
def send_booking_confirmation_email(email: str, booking_id: str):
    """
    Имитация отправки email.
    Celery выполняет это в отдельном процессе, не блокируя API.
    """
    print(f"📨 START sending email to {email} for booking {booking_id}...")

    # Имитируем задержку отправки (как будто соединяемся с почтовым сервером)
    time.sleep(5)

    print(f"✅ EMAIL SENT to {email} successfully!")
    return f"Email sent to {email}"
