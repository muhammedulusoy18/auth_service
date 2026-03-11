# FastAPI JWT Authentication Service

Bu proje, modern web uygulamaları için geliştirilmiş, güvenli bir kimlik doğrulama (Authentication) altyapısıdır. 2. sınıf bilgisayar mühendisliği öğrencisi olarak, sektör standartlarında bir mimari (FastAPI, JWT, SQLAlchemy) kullanılarak geliştirilmiştir.

## 🚀 Özellikler
* **JWT (JSON Web Token):** Bearer ve Refresh Token mekanizması ile güvenli oturum yönetimi.
* **Şifre Güvenliği:** Kullanıcı şifreleri `bcrypt` ile hashlenerek saklanır.
* **Katmanlı Mimari:** Kodlar; `Models`, `Schemas`, `CRUD` ve `API` katmanlarına ayrılarak modüler bir yapı sunar.
* **OAuth2 Standartları:** Swagger UI üzerinden doğrudan "Authorize" kilit butonuyla test edilebilir.

## 🛠️ Kurulum
1. Projeyi bilgisayarınıza klonlayın.
2. Bir sanal ortam (venv) oluşturun ve aktif edin.
3. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
