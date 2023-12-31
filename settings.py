"""
Django settings for WebsmartunityQR project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$^g$-rn84_x3x6q-#e1fbcvv4h^9c9yvpjqw@^+x0$rp#dcjr+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'WebsmartunityQR',
    'bootstrap5'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WebsmartunityQR.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_filters': 'WebsmartunityQR.custom_filters',
                # แทน your_app_name ด้วยชื่อแอปพลิเคชันของคุณ
            },
        },
    },
]

WSGI_APPLICATION = 'WebsmartunityQR.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Django settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'onemail.one.th'  # ชื่อโฮสต์ SMTP ของคุณ
EMAIL_PORT = 465  # พอร์ต SMTP ของคุณ
EMAIL_USE_SSL = True  # ใช้ SSL หรือไม่ (ถ้าใช้ SSL, ให้เปลี่ยนเป็น True)
EMAIL_HOST_USER = 'auth@nidec-precision.co.th'  # ชื่อผู้ใช้ SMTP ของคุณ
EMAIL_HOST_PASSWORD = 'Nis_2022'  # รหัสผ่าน SMTP ของคุณ
EMAIL_USE_TLS = False  # ไม่ใช้ TLS

DEFAULT_FROM_EMAIL = 'auth@nidec-precision.co.th'  # ที่อยู่อีเมลเริ่มต้นสำหรับการส่ง
SERVER_EMAIL = 'notify@nidec-precision.co.th'  # ที่อยู่อีเมลของเซิร์ฟเวอร์ (สำหรับการแจ้งเตือนข้อผิดพลาด)

# แนะนำ: ใส่ค่าของคุณในไฟล์ .env เพื่อเก็บความลับและไม่เผยแพร่รหัสผ่าน
# คุณสามารถใช้ python-decouple หรือ python-dotenv เพื่อดำเนินการนี้
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smart_un_ch_list',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5433',
    },
    'user_list': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'user_list',  # ชื่อฐานข้อมูลของคุณ
        'USER': 'postgres',  # ชื่อผู้ใช้ของฐานข้อมูล user_list
        'PASSWORD': 'postgres',  # รหัสผ่านของฐานข้อมูล user_list
        'HOST': 'localhost',  # หรือโฮสต์อื่น ๆ ที่คุณใช้
        'PORT': '5433',  # หรือพอร์ตที่คุณใช้
    }
}
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'smart_un_ch_list',
#         'USER': 'user_setup',
#         'PASSWORD': 'user_setup',
#         'HOST': '172.30.1.15',
#         'PORT': '5432',
#         'OPTIONS': {
#             'timezone': 'UTC',
#         },
#     },
#
#     'user_list': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'user_list',  # ชื่อฐานข้อมูลของคุณ
#         'USER': 'user_setup',  # ชื่อผู้ใช้ของฐานข้อมูล user_list
#         'PASSWORD': 'user_setup',  # รหัสผ่านของฐานข้อมูล user_list
#         'HOST': '172.30.1.15',  # หรือโฮสต์อื่น ๆ ที่คุณใช้
#         'PORT': '5432',  # หรือพอร์ตที่คุณใช้
#         'OPTIONS': {
#                     'timezone': 'UTC',
#                 },
#         }
#     }
# TIME_ZONE = 'UTC'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
