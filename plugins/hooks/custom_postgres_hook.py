from airflow.hooks.base import BaseHook
import psycopg2
import pandas as pd

class CustomPostgresHook(BaseHook):

    def __init__(self, postgres_conn_id, **kwargs):
        self.postgres_conn_id = postgres_conn_id

    def get_conn(self):
        airflow_conn = BaseHook.get_connection(self.postgres_conn_id)
        self.host = airflow_conn.host
        self.user = airflow_conn.login
        self.password = airflow_conn.password
        self.dbname = airflow_conn.schema
        self.port = airflow_conn.port

        self.postgres_conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
            port=self.port
        )
        return self.postgres_conn

    def bulk_load(self, table_name, file_name, delimiter: str = '\t', is_header: bool = True, is_replace: bool = True):
        from sqlalchemy import create_engine

        self.log.info('적재 대상파일: ' + file_name)
        self.log.info('테이블: ' + table_name)
        self.get_conn()

        header = 0 if is_header else None                 # is_header = True면 첫 행을 컬럼으로 사용
        if_exists = 'replace' if is_replace else 'append' # True면 덮어쓰기, False면 append

        file_df = pd.read_csv(file_name, header=header, delimiter=delimiter)

        for col in file_df.columns:
            try:
                # 문자열일 경우만 줄바꿈 제거
                file_df[col] = file_df[col].astype(str).str.replace('\r\n', '').str.replace('\n', '')
                self.log.info(f'{table_name}.{col}: 개행문자 제거')
            except Exception:
                continue

        self.log.info('적재 건수: ' + str(len(file_df)))

        uri = f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}'
        engine = create_engine(uri)

        file_df.to_sql(
            name=table_name,
            con=engine,
            schema='public',
            if_exists=if_exists,
            index=False
        )
