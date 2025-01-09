
class Config:
    DEBUG = False
    SECRET_KEY = 'dev'

    #Database config
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:P3drobutt1e$@postgres:5432/bit_videoanalisis"

    #CKEditor para ingresar texto
    CKEDITOR_PKG_TYPE = 'standard'