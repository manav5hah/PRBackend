from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine.base import Engine, Connection
import pandas as pd

class ConnectionHandler:
    def __init__(self, server:str, database:str, username:str, password:str):
        self._server = server
        self._database = database
        self._username = username
        self._password = password
        # self.driver = 'ODBC+Driver+17+for+SQL+Server'
        # self._server = server
        # self._database = database
        # self._username = username
        # self._password = password
        self.driver = 'ODBC+Driver+18+for+SQL+Server'
        
        DB_URL:str = f'mssql+pyodbc://{self._username}:{self._password}@{self._server}/{self._database}?driver={self.driver}&TrustServerCertificate=yes'

        self._engine:Engine = create_engine(DB_URL)

        self._conn:Connection = self._engine.connect()

    def fetch_data(self, query:str) -> pd.DataFrame:
        return pd.read_sql(query, con=self._conn)
        
    def insert_data(self, df:pd.DataFrame, tablename:str):
        df.to_sql(tablename, if_exists='append', index=False, con=self._conn)
        
    def execute_query(self, query:str):
        self._conn.execute(query)
        
    def __del__(self):
        try:
            self._conn.close()
        except:
            pass

# Base = automap_base()

# Base.prepare(engine, reflect=True, schema='production')
# Base.prepare(engine, reflect=True, schema='sales')

# ProductionBrands = Base.classes.brands
# ProductionCategories = Base.classes.categories
# ProductionProducts = Base.classes.products
# ProductionStocks = Base.classes.stocks

# SalesCustomers = Base.classes.customers
# SalesOrderItems = Base.classes.order_items
# SalesOrder = Base.classes.orders
# SalesStaff = Base.classes.staffs
# SalesStore = Base.classes.stores

# SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# session = create_session(bind=engine)

# result = session.query(ProductionBrands).all()


_server = 'UAT-DATASERVER'
_database = 'Estro'
_username = 'test'
_password = 'keyur'
driver = 'ODBC+Driver+18+for+SQL+Server'

DB_URL:str = f'mssql+pyodbc://{_username}:{_password}@{_server}/{_database}?driver={driver}&TrustServerCertificate=yes'
# DB_URL:str = URL.create('mssql+pyodbc', username=_username, password=_password, host=_server, database=_database, query={'driver': driver, 'TrustServerCertificate': 'True'})

# _engine:Engine = create_engine(DB_URL)

# _conn:Connection = _engine.connect()

# print(pd.read_sql('''
#                   select holder, cb_cmcd, name from vw_AadharK where pan in (
#         select cb_panno from client_master 
#         join client_backoffice on cm_Cd = cb_cmcd
#         where cm_blsavingcd='k086' 
#         )
#         and cb_cmcd not in (
#         select cm_Cd from client_master 
#         join client_backoffice on cm_Cd = cb_cmcd
#         where cm_blsavingcd= 'k086'
#         )
#                   ''', con=_conn))