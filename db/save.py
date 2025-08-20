import sqlite3

def save_to_sql(df, db_name, table_name):
    
    try:
        with sqlite3.connect(db_name) as conn: #with (context manager) kullanılarak veritabanı bağlantısı açılır. connect() methodunun döndürdüğü bağlantı nesnesi, conn değişkenine atanır.
            #  Bir with bloğuna girdiğinizde, kaynak (burada veritabanı bağlantısı) otomatik olarak açılır.
            # Bloğun sonuna geldiğinizde, kaynak otomatik olarak kapatılır. Bu, kaynak sızıntılarını önler. O yüzden with bloğu kullanmı çok önerilir.
           
            unnamed_cols = [col for col in df.columns if "unnamed" in str(col).lower()] #df.columns içinde "unnamed" kelimesini içeren kolonları bulur.
            if unnamed_cols:
                df.drop(columns=unnamed_cols, inplace=True) # inplace=True ile orijinal DataFrame'i günceller, yani yeni bir DataFrame oluşturmaz.
                print(f"🗑️ Kaldırılan Unnamed kolonlar: {unnamed_cols}")

            df.to_sql(table_name, conn, if_exists='replace', index=False) # to_sql() methodu, DataFrame'i belirtilen veritabanı bağlantısına yazar.
            # if_exists='replace' ile eğer tablo zaten varsa, eski tabloyu silip yeni tabloyu oluşturur.
            # index=False ile DataFrame'in indeksini veritabanına yazmaz.

        print(f"✅ '{table_name}' tablosu '{db_name}' veritabanına başarıyla kaydedildi.")

    except Exception as e:
        print(f"❌ '{table_name}' tablosu kaydedilirken hata oluştu: {e}")