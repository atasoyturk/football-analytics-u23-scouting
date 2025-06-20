import schedule
import time
from scheduler.job import job


if __name__ == '__main__':
    # İlk çalıştırma
    job()

    # Her pazar 00:00'da job'u çalışacak şekilde planla
    schedule.every().sunday.at("00:00").do(job)

    print("⏳ Scheduler çalışıyor... (Pazar 00:00'da veri çekilecek)")

    # Sonsuz döngü
    while True:
        schedule.run_pending()
        time.sleep(60)
