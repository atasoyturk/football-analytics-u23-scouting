from selenium import webdriver  # selenium modülünden webdriver sınıfını içe aktarır.
from selenium.webdriver.chrome.service import Service  # selenium modülünden Chrome tarayıcısını kontrol etmek için gerekli olan Service sınıfını içe aktarır.
from selenium.webdriver.chrome.options import Options  # selenium modülünden Chrome tarayıcısının seçeneklerini ayarlamak için gerekli olan Options sınıfını içe aktarır.
from webdriver_manager.chrome import ChromeDriverManager  # webdriver_manager modülünden ChromeDriverManager sınıfını içe aktarır.
from config import BRAVE_PATH  # Brave tarayıcısının kurulu olduğu dosya yolunu içe aktarır.


def setup_browser():

    chrome_options = Options()  # Options fonksiyonu, Chrome tarayıcısının seçeneklerini ayarlamak için kullanılır.
    chrome_options.add_argument('--headless')  # browser kullanıcı arayüzü olmadan arkaplanda çalışır, daha az kaynak tüketir.
    
    chrome_options.add_argument('--no-sandbox')  # sandbox, tarayıcıyı izole eden bir güvenlik özelliğidir. Bu seçenek, sandbox'u devre dışı bırakır.
    # fakat bu komut dosyalara erişim izni verebilir, bu yüzden dikkatli kullanılmalıdır.
    # genellikle güvenlik riski taşıdığı için tavsiye edilmeyen bir ayardır, o yüzden genelde sandbox tercih edilir.
    
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # browser çalışırken /dev/shm (shared memory) kullanımı devre dışı bırakır.
    # shared memory, tarayıcıların hızlı veri iletimi için kullandığı bir bellek alanıdır. (Linux sistemlerde)
    # fakat Windows sistemlerde bu seçenek genellikle gerekli değildir.
    
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.55 Safari/537.36'
    )
    # Bir web tarayıcısı (veya herhangi bir HTTP istemcisi), bir web sitesine bağlanırken kendini tanıtan özel bir metin dizisi gönderir. Bu dizeye User-Agent denir.
    # User-Agent, web sitesine tarayıcının türü, sürümü, işletim sistemi ve bazen de CPU mimarisi gibi bilgileri sağlar.
    # Bu user agent, tarayıcının Windows 10 işletim sistemi üzerinde çalışan Chrome 141 sürümünü temsil eder.
    # Bu, web sitelerinin tarayıcıyı tanımasına ve uygun içerik sunmasına yardımcı olur.
    
    chrome_options.binary_location = BRAVE_PATH  # Brave tarayıcısının kurulu olduğu yolu belirtir.
    CHROME_DRIVER_PATH = r"C:\Users\User\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    service = Service(CHROME_DRIVER_PATH)

    # webdriver.Chrome, Chrome (veya Brave) tarayıcısını başlatır.
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver
