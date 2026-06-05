"""
Django settings for backend project.
"""

from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Application definition
INSTALLED_APPS = [
    'jazzmin',    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   
    'rest_framework',
    'django_htmx',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'backend.urls'
#ROOT_URLCONF = "Goorr_solutions_2.urls"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'templates'],
        "DIRS": [BASE_DIR / "templates"],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'goorr_db',
        'USER': 'goorr_user',
        'PASSWORD':'Laloran@2015',
        'HOST': 'localhost',
        'PORT': '5432',
       
       
         
}}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/home/lalo/Goorr_solutions_2/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#New test

LOGIN_URL = "/login/"
# LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_REDIRECT_URL = "/admin/"

LOGOUT_REDIRECT_URL = "/login/"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} — {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '//home/mcruz/Goorr_solutions_2/logs/django.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/mcruz/Goorr_solutions_2/logs/django_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file', 'error_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

JAZZMIN_SETTINGS = {
    "index_template": "admin/custom_index.html",
    "site_title": "Goorr Admin",
    "site_header": "Goorr Recruitment System",
    "site_brand": "Goorr",
    "welcome_sign": "Welcome to Goorr Admin",
    
    "custom_css": "css/custom.css",
    "custom_js": "js/dashboard.js",
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": ["auth"],
    "order_with_respect_to": ["api"],
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index"},
        {"app": "api"},
    ],
}



# JAZZMIN_SETTINGS = {

#     "custom_css": "css/custom.css",
#     "custom_js": "js/dashboard.js",
#     "index_template": "admin/custom_index.html",
#     "site_title": "Goorr Admin",
#     "site_header": "Goorr Recruitment System",
#     "site_brand": "Goorr",

#     "welcome_sign": "Welcome to Goorr Recruitment Dashboard",
#     "copyright": "Goorr Ltd",
#     "login_url": "/login/",
#     # Optional: where to go after login
#     "site_url": "/dashboard/",
#     # ✅ Top menu
#     #"topmenu_links": [
#      #   {"name": "Dashboard", "url": "admin:index"},
#     #],
#     "topmenu_links": [
#         {"name": "Dashboard", "url": "/admin/"},
#         {"model": "api.Candidate"},
#         {"model": "api.Interview"},
#     ],


#     # ✅ Sidebar behavior
#     "show_sidebar": True,
#     "navigation_expanded": True,

#     # ✅ Order apps & models (VERY useful)
#     "order_with_respect_to": [
#         "api.Candidate",
#         "api.Interview",
#         "api.CandidateDocument",
#     ],

#     # ✅ Icons (FontAwesome)
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",

#         "api.Candidate": "fas fa-user-graduate",
#         "api.Interview": "fas fa-comments",
#         "api.CandidateDocument": "fas fa-file-alt",
#     },

#     # ✅ UI Tweaks
#     "theme": "flatly",  # try: flatly, cosmo, minty, lumen
#     "dark_mode_theme": "darkly",

#     # ✅ Show change form as tabs (clean UI)
#     "changeform_format": "horizontal_tabs",

#     # ✅ Custom branding
#     "site_logo": None,  # can add later
#     "login_logo": None,

#     # 👇 Add topmenu links here
#     "topmenu_links": [
#         {"name": "Goorr Home", "url": "/", "new_window": True},  # external link
#         {"model": "api.Candidate"},  # link to model
#         {"app": "api"},              # link to app
#     ],
# }


