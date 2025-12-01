# Müşteri Memnuniyeti ve Hizmet Kalitesi Anket Projesi
* Github organizasyon oluşturduk
* İçine Kullanıcıları ekledik ve hepsinin pull request ve push request göndermesine izin verdik.
* Masaüstüne bir dosya oluşturduk(sediray)
* Varsa bütün dosyaları bu klasöre koyacağız
* Vs code içinde "cd" ve"ls" komutlarını kullanarak masasütündeki dosyanın içine gireriz.
* git init              # klasörü git projesine çevirir
* masaüstü klasörün içine örneğin: readme.md diye bir klasör oluştur. İlk aşamada repoyu kontrol etmek için yararlı.
* git add .             # tüm dosyaları ekler
* git commit -m "İlk commit: proje başlangıcı"
* git branch -M main (Ana branch ismini main olarak değiştirdik)
* git remote add origin https://github.com/organizasyon-adi/musteri-memnuniyeti-anket.git (Yerel bilgisayarı Github'a bağlayacağız.)
* git push -u origin main (masaüstü dosyadaki her şeyi github'a push ederiz.)


diğer kullanıcılar ne yapacak ? Bu iki komut sıra ile çalıştırılır.
*git clone https://github.com/organizasyon-adi/musteri-memnuniyeti-anket.git
*cd musteri-memnuniyeti-anket
Branch açmadan önce bunlar yapılacak
* git checkout main (son güncellemeler alınır)
* git pull origin main (son güncellemeler alınır)
*Sonra herkes kendine branch açacak, örneğin:
Kişi 1:
git checkout -b feature-anket-tanimlama
Kişi 2:
git checkout -b feature-anket-doldurma
Kişi 3:
git checkout -b feature-raporlama

* git add .
* git commit -m "İlk geliştirme"
* git push -u origin feature-anket-tanimlama
******
Özet Akış (Kafanızda netleşsin diye)
Senin taraf:
Organizasyonda repo aç
Kendi bilgisayarında:
git init
git add .
git commit -m "İlk commit"
git branch -M main
git remote add origin ...
git push -u origin main
Ekip tarafı:
git clone ...
git checkout -b feature-...
Kod yaz → git add . → git commit → git push
GitHub’da Pull Request aç
