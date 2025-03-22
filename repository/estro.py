import os 
import pandas as pd
from db_config.connect import ConnectionHandler

class Estro:
    def __init__(self, database:str, username:str, password:str):
        self._server:str = os.environ['HOST']
        self._database:str = database
        self._username:str = username
        self._password:str = password
        self._connection_handler:ConnectionHandler = ConnectionHandler(self._server, self._database, self._username, self._password)

    def get_accounts(self, client_code:str) -> pd.DataFrame:
        query:str=f'''
        select holder, cb_cmcd, name from vw_AadharK where pan in (
        select cb_panno from client_master 
        join client_backoffice on cm_Cd = cb_cmcd
        where cm_blsavingcd='{client_code}' 
        )
        and cb_cmcd not in (
        select cm_Cd from client_master 
        join client_backoffice on cm_Cd = cb_cmcd
        where cm_blsavingcd= '{client_code}'
        )
        '''
        result:pd.DataFrame = self._connection_handler.fetch_data(query)
        return result

    def get_mcap_fc(self, family_code:str) -> pd.DataFrame:
        query:str=f"select * from vw_mcapsector where cm_familycd='{family_code.upper()}'"
        val:pd.DataFrame = self._connection_handler.fetch_data(query)
        cap_raw:pd.Series = val.get('Cap')
        sector_raw:pd.Series = val.get('Sector')
        cap_perc:pd.Series = cap_raw.value_counts(dropna=True)/cap_raw.size
        sector_perc:pd.Series = sector_raw.value_counts(dropna=True)/sector_raw.size
        cap_list:list = []
        sector_list:list = []
        for cap_type in set(cap_raw):
            cap_list.append({"cap": cap_type, "cap_percentage":round(cap_perc[cap_type], 4), "cap_shares": val[cap_raw == cap_type].to_dict(orient='records')})
        for sector_type in set(sector_raw):
            sector_list.append({"sector": sector_type, "sector_percentage":round(sector_perc[sector_type], 4), "sector_shares": val[sector_raw == sector_type].to_dict(orient='records')})
        result:dict = {'cap_details': cap_list, "sector_details": sector_list}
        
        return result
        
    def get_mcap_cc(self, client_code:str) -> pd.DataFrame:
        query:str=f"select * from vw_mcapsector where hld_ac_code='{client_code}'"
        val:pd.DataFrame = self._connection_handler.fetch_data(query)
        print(val)
        cap_raw:pd.Series = val.get('Cap')
        sector_raw:pd.Series = val.get('Sector')
        cap_perc:pd.Series = cap_raw.value_counts(dropna=True)/cap_raw.size
        sector_perc:pd.Series = sector_raw.value_counts(dropna=True)/sector_raw.size
        cap_list:list = []
        sector_list:list = []
        for cap_type in set(cap_raw):
            cap_list.append({"cap": cap_type, "cap_percentage":round(cap_perc[cap_type], 4), "cap_shares": val[cap_raw == cap_type].to_dict(orient='records')})
        for sector_type in set(sector_raw):
            sector_list.append({"sector": sector_type, "sector_percentage":round(sector_perc[sector_type], 4), "sector_shares": val[sector_raw == sector_type].to_dict(orient='records')})
        result:dict = {'cap_details': cap_list, "sector_details": sector_list}
        return result