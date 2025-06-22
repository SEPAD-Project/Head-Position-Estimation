[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/Head-Position-Estimation/blob/main/README.md)
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/Head-Position-Estimation/blob/main/README.fa.md)

# برآورد موقعیت سر (Head Position Estimation)
این مخزن گیت، بخشی از پروژه SEPAD است و توسط [پارسا صفايي](https://www.github.com/parsasafaie)   به‌منظور انجام وظایف پردازش تصویر در سیستم بزرگ‌تر SEPAD توسعه داده شده است.

برای بازدید از سازمان [SEPAD](https://www.github.com/SEPAD-Project) اینجا کلیک کنید.

## کلون کردن مخزن (Repository Cloning)
برای کلون کردن این مخزن، ترمینال خود را در دایرکتوری مورد نظر باز کنید و دستور زیر را اجرا کنید:
```bash
git clone https://github.com/SEPAD-Project/Head-Position-Estimation.git
```

سپس وارد دایرکتوری مخزن شوید:
```
cd Head-Position-Estimation
```

## نصب وابستگی‌ها (Installing Dependencies)
1. ایجاد محیط مجازی:
   ```bash
   python -m venv .venv
   ```
2. فعال کردن محیط مجازی:
   
   * در ویندوز:
     ```bash
     .venv\Scripts\activate.bat
     ```

   * در macOS/لینوکس:
     ```bash
     source .venv/bin/activate
     ```
3. نصب وابستگی‌های لازم:
   ```bash
   pip install -r requirements.txt
   ``` 

## وابستگی‌های لازم برای InsightFace
* در ویندوز:
  1. ابتدا از لینک زیر ابزارهای ساخت Visual Studio را دانلود کنید:
  [vs-build-tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  1. پس از اجرای نصب، در حین نصب گزینه "C++ Desktop Development"  را انتخاب کنید.
  2. کامپیوتر خود را مجدداً راه‌اندازی کنید.

* در لینوکس:

  فقط دستور زیر را در ترمینال اجرا کنید:
  ```bash
    sudo apt-get install build-essential
  ```

## دانلود مدل‌های لازم
این پروژه نیازمند مدل‌های `InsightFace` است که برای کارکرد صحیح آن باید مدل‌ها دانلود و قرار داده شوند.
برای دانلود خودکار و قرار دادن مدل‌ها، دستور زیر را اجرا کنید:
```bash
python download_models.py
```
در صورتی که مدل‌ها به‌درستی دانلود شوند، خروجی دستور `True` خواهد بود.

## اجزای پروژه
پروژه شامل سه جزء اصلی است:
* yaw_pitch : تعیین می‌کند که آیا فرد به مانیتور نگاه می‌کند یا خیر.
* eye_status : تشخیص وضعیت باز یا بسته بودن چشم‌های فرد.
* face_recognition : مقایسه چهره تشخیص داده شده با تصویر مرجع به‌منظور تأیید هویت فرد.

همچنین، سه جزء تستی نیز وجود دارد:
* looking_result : تمامی سه جزء اصلی را در یک مجموعه ادغام می‌کند و یک کد نتیجه را برمی‌گرداند.
* فایل‌های تست : هر دایرکتوری اصلی حاوی یک فایل `test.py` است که به شما کمک می‌کند عملکرد خاصی را تست کنید.
* Graphical_output : تصویر کامل را همراه با خروجی پردازش شده نمایش می‌دهد و برای تست بصری بسیار مفید است.

## کدهای نتیجه (Result Codes)
سیستم کدهای نتیجه‌ای بین 0 تا 5 تولید می‌کند تا بازخورد دقیق‌تری فراهم کند.

معنی این کدها را می‌توانید در فایل result_codes.csv پیدا کنید.
