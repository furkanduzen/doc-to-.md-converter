# Çalıştırma rehberi

Depoyu GitHub Desktop ile bilgisayarına indirdikten sonra, aşağıdaki adımları uygula. İlk kurulumda internet bağlantısı gerekir. Python 3.11 önerilir.

## Mac

### İlk kurulum

1. Terminal uygulamasını aç.
2. Depo klasörünü Terminal'e tanıtmak için `cd ` yaz (sonunda bir boşluk bırak), Finder'dan `doc-to-.md-converter` klasörünü Terminal penceresine sürükle ve Enter'a bas.
3. Şu komutları sırayla çalıştır:

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -e 'packages/markitdown[all]'
   ```

### Her kullanımda

1. Terminal'de depo klasörüne git. Finder'dan klasörü Terminal'e sürükleyerek yine `cd ` ile açabilirsin.
2. Arayüzü başlat:

   ```bash
   ./.venv/bin/python web_app.py
   ```

3. Tarayıcıda `http://127.0.0.1:8765` açılır. Dosyanı seçip **Dönüştür ve Masaüstüne kaydet** düğmesine bas. `.md` dosyası Masaüstüne kaydedilir.
4. Bitince Terminal penceresine tıkla ve `Control (⌃) + C` tuşlarına bas.

## Windows

### İlk kurulum

1. Python 3.11'i kur. Kurulumda **Add Python to PATH** seçeneğini işaretle.
2. GitHub Desktop'ta depoyu indirdiğin klasörü Dosya Gezgini'nde aç. Adres çubuğuna `powershell` yazıp Enter'a bas.
3. PowerShell'de şu komutları sırayla çalıştır:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -e "packages/markitdown[all]"
   ```

### Her kullanımda

1. Depo klasöründe PowerShell aç: Dosya Gezgini adres çubuğuna `powershell` yaz ve Enter'a bas.
2. Arayüzü başlat:

   ```powershell
   .\.venv\Scripts\python.exe web_app.py
   ```

3. Tarayıcıda `http://127.0.0.1:8765` açılır. Dosyanı seçip **Dönüştür ve Masaüstüne kaydet** düğmesine bas. `.md` dosyası Masaüstüne kaydedilir.
4. Bitince PowerShell penceresine tıkla ve `Ctrl+C` tuşlarına bas.

Kurulumdan sonra paketleri yeniden kurman gerekmez.
