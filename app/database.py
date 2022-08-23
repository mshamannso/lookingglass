import sqlalchemy as sa

SERVER = '192.168.0.245'
SQLSERVER_DATABASE = 'lookingglass'
SQLSERVER_USER = 'thecaptain'
SQLSERVER_PASSWORD = '99Redbal00ns'
PORT = 1433
SQLSERVER_BASE_URI = 'mssql+pyodbc://{USER}:{PWD}@{SERVER}:{PORT}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'

engine = sa.create_engine(SQLSERVER_BASE_URI.format(
    SERVER=SERVER,
    DATABASE=SQLSERVER_DATABASE,
    USER=SQLSERVER_USER,
    PWD=SQLSERVER_PASSWORD,
    PORT=PORT
))
