from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import BRAVE_PATH, CHROME_DRIVER_PATH


def setup_browser():

    chrome_options = Options()
    chrome_options.add_argument('--headless') #browser kullanıcı arayüzü olmadan arkaplanda çalısır, daha az kaynak tüketir
    chrome_options.add_argument('--no-sandbox') #sandbox, tarayıcıyı izole eden bir güvenlik özelliğidir. Bu seçenek, sandbox'u devre dışı bırakır.
    #fakat bu komut dosyalara erişim izni verebilir, bu yüzden dikkatli kullanılmalıdır.
    #genellikle güvenlik riski taşıdıgı icin tavsiye edilmeyen bir ayardır, o yüzden genelde sandbox tercih edilir.
    
    #chrome_options.add_argument('--disable-dev-shm-usage')  browser calsıırken /dev/shm (shared memory) kullanımı devre dısı bırakır
    #shared memory, tarayıcıların hızlı veri iletimi için kullandığı bir bellek alanıdır. (linux sistemlerde)
    #fakat windows sistemlerde bu seçenek genellikle gerekli değildir.
    
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36'
    )
    #Bir web tarayıcısı (veya herhangi bir HTTP istemcisi), bir web sitesine bağlanırken kendini tanıtan özel bir metin dizisi gönderir. Bu dizeye User-Agent denir.
    #User-Agent, web sitesine tarayıcının türü, sürümü, işletim sistemi ve bazen de CPU mimarisi gibi bilgileri sağlar.
    #bu user agent, tarayıcının Windows 10 işletim sistemi üzerinde çalışan Chrome 114 sürümünü temsil eder.
    #Bu, web sitelerinin tarayıcıyı tanımasına ve uygun içerik sunmasına yardımcı olur.
    
    chrome_options.binary_location = BRAVE_PATH

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
