import sqlite3

def save_to_sql(df, db_name, table_name):
    
    try:
        with sqlite3.connect(db_name) as conn: 
            #with (context manager) kullanılarak veritabanı bağlantısı açılır. connect() methodunun döndürdüğü bağlantı nesnesi, conn değişkenine atanır.
            #  Bir with bloğuna girdiğinizde, kaynak (burada veritabanı bağlantısı) otomatik olarak açılır.
            # Bloğun sonuna geldiğinizde, kaynak otomatik olarak kapatılır. Bu, kaynak sızıntılarını önler. O yüzden with bloğu kullanmı çok önerilir.
            #con.close() ile manuel olarak kapatmaya gerek yok.
                       
            df.to_sql(table_name, conn, if_exists='replace', index=False) # to_sql() methodu, DataFrame'i belirtilen veritabanı bağlantısına yazar.
            # if_exists='replace' ile eğer tablo zaten varsa, eski tabloyu silip yeni tabloyu oluşturur.
            # index=False ile DataFrame'in indeksini veritabanına yazmaz.

        print(f"✅ '{table_name}' tablosu '{db_name}' veritabanına başarıyla kaydedildi.")

    except Exception as e:
        print(f"❌ '{table_name}' tablosu kaydedilirken hata oluştu: {e}")