from bs4 import BeautifulSoup 
'''
Beautiful Soup Nedir?
Beautiful Soup, HTML ve XML dosyalarından veri çekmek için tasarlanmış bir Python kütüphanesidir. 
Web sayfalarının yapısını (tag'leri, ID'leri, class'ları vb.) çözümleyerek, bu yapı içindeki belirli elementlere kolayca ulaşmanızı, 
onların içeriğini okumanızı veya niteliklerini (attribute'larını) çekmenizi sağlar.
'''

import pandas as pd
from analysis.utils import clean_column_names

from selenium.webdriver.common.by import By
'''
Selenium'a web sayfasındaki elementleri nasıl bulacağınıza dair farklı stratejileri ("By" mekanizmaları) sağlar. 
Bir web elementini bulmak için genellikle onun ID'si, sınıf adı (class name), etiket adı (tag name),
CSS seçicisi (CSS selector), XPath'i veya bağlantı metni (link text) gibi özelliklerini kullanırız.
'''
from selenium.webdriver.support.ui import WebDriverWait
'''
Selenium'a belirli koşullar karşılanana kadar tarayıcıyı bekletme yeteneği kazandıran WebDriverWait sınıfını içe aktarır. 
Web sayfaları dinamiktir; bazı elementler hemen yüklenmeyebilir veya bir işlem sonucunda görünür hale gelebilir. 
Eğer Selenium, bir elementin yüklenmesini beklemeden onu bulmaya çalışırsa, NoSuchElementException gibi hatalarla karşılaşabilirsiniz.
'''
from selenium.webdriver.support import expected_conditions as EC
'''
WebDriverWait ile birlikte kullanılacak olan önceden tanımlanmış "beklenen koşullar" kümesini (expected_conditions) içe aktarır. 
expected_conditions modülü, web elementlerinin durumuyla ilgili yaygın olarak beklenen senaryolar için hazır koşullar sunar. 
Bu koşullar, bir elementin görünür olup olmadığını, tıklanabilir olup olmadığını,
sayfaya eklenip eklenmediğini veya bir metnin belirli bir elementte olup olmadığını kontrol etmek gibi işlemleri kolaylaştırır.
'''


def fetch_html(driver, url, wait_time=10):
    driver.get(url)
    print(f"Website opened: {url}")

    try:
        # WebDriverWait, belirli bir süre boyunca (wait_time) belirtilen koşul karşılanana kadar bekler.
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
    except Exception as e:
        print(f"Scraping error: {e}")

    return driver.page_source


def extract_table(html, table_id='stats_standard'):
    
    soup = BeautifulSoup(html, 'html.parser') #beatifulsoup nesnesi oluşturarak html içeriğini ayrıştırır.
    # iki adet parametre alır: html içeriği ve ayrıştırma için kullanılacak parser türü.
    # Eğer 'html.parser' kullanılırsa, Python'un yerleşik HTML ayrıştırıcısı kullanılır. lxml veya html5lib gibi alternatifler de kullanılabilir.
    # bu satırın sonunda soup nesnesi aslında HTML içeriğinin bir temsilidir. Bu sayede HTML içeriği üzerinde arama yapabilir, elementleri bulabilir ve içeriği işleyebilirsiniz.
    
    table = soup.find('table', {'id': table_id})
    #soup nesnesinin find() metodu, HTML içeriğinde belirli bir etiketi (tag) ve bu etikete ait özellikleri (attributes) arar.
    # Bu örnekte, 'table' etiketi ve 'id' özelliği 'stats_standard' olan tabloyu arar, ve eğer bulursa bu tabloyu döndürür.
    if not table:
        raise ValueError(f"{table_id} could not be found.")

    df = pd.read_html(str(table))[0] #pd.read_html() fonksiyonu, HTML içeriğinden tabloyu okur ve bir DataFrame'e dönüştürür.
    # paramtere olarak pandasın anlayabileceği standart bir HTML dizinine yani string'e ihtiyacı vardır. (bazen url de alabilir)
    #O yuzden tabloyu string'e dönüştürmek için str(table) kullanılır. ve [0] ile listedeki ilk dataframe'i alırız.

    df = clean_column_names(df)

    player_col = [col for col in df.columns if 'player' in str(col).lower()] # df.columns dataframe'in sütun adlarını içerir.
    #tüm sütun adlarını dolaşır ve 'player' kelimesini içeren sütun adlarını bulur. (str(col).lower() ile küçük harfe çevirerek yapar)
    
    if player_col:
        df = df[df[player_col[0]] != player_col[0].split('_')[-1]]
        
    #player_col[0] 'player' kelimesini içeren ilk sütun adını temsil eder. (muhtemelen 1 tane ve Player_Name gibi bir isimdir)
    #df[player_col[0]] ise bu sütündaki tüm verileri yani tum oyuncuları temsil eder.
    #player_col[0].split('_')[-1] ise split() metodu ile '_' karakterine göre ayırır ve son elemanı alır. ([-1] yani 'Name') (Player_Name)
    # yani kontrol edilen şey oyuncu adının 'Name' olup olmadığıdır. Eğer öyleyse, bu satırları kaldırırız.
    #yeni df tamamen gerçek oyuncu isimlerini içerecek şekilde güncellenir.
    
    # bu durum genellikle web'den veri çekerken (web scraping) karşılaşılan yaygın bir problemdir, o yüzden bu kontrolü yaparız.
    
    

    return df