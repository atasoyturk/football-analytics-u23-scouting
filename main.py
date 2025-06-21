import schedule
import time
from scheduler.job import job

LEAGUES = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"]

if __name__ == '__main__':
    # Program açılır açılmaz tüm ligler için veriyi çek
    for league in LEAGUES:
        job(league_name=league)

    # Her pazar 00:00'da tüm ligler için veri çekme işlemini planla
    for league in LEAGUES:
        schedule.every().sunday.at("00:00").do(job, league_name=league)

    print("⏳ Scheduler çalışıyor... Her Pazar 00:00'da tüm liglerin verileri güncellenecek.")

    while True:
        schedule.run_pending()
        time.sleep(60)
