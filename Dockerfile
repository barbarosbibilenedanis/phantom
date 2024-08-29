# Temel imaj olarak Python 3.9 kullanıyoruz
FROM python:3.10

# Çalışma dizini oluşturuyoruz
WORKDIR /app

# Gereken Python bağımlılıklarını kopyalıyoruz
COPY requirements.txt .

# Bağımlılıkları yüklüyoruz
RUN pip install -r requirements.txt

# Uygulama dosyalarını kopyalıyoruz
COPY . .


# Statik dosyaları topluyoruz
RUN python manage.py collectstatic --noinput

# Uygulama başlatma komutu
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
