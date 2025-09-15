import pendulum
from hooks.custom_postgres_hook import CustomPostgresHook

# Airflow 3.0 부터 아래 경로로 import 합니다.
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

# Airflow 2.10.5 이하 버전에서 실습시 아래 경로에서 import 하세요.
# from airflow import DAG
# from airflow.operators.python import PythonOperator

with DAG(
    dag_id='dags_python_with_custom_hook_bulk_load',
    start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
    schedule='0 7 * * *',   # 매일 07:00 실행
    catchup=False
) as dag:

    def insrt_postgres(postgres_conn_id, tbl_nm, file_nm, **kwargs):
        custom_postgres_hook = CustomPostgresHook(postgres_conn_id=postgres_conn_id)
        custom_postgres_hook.bulk_load(
            table_name=tbl_nm,
            file_name=file_nm,
            delimiter='\t',          # 🔑 CSV가 탭 구분자라서 꼭 \t 로 설정
            is_header=True,
            is_replace=True
        )

    insrt_postgres = PythonOperator(
        task_id='insrt_postgres',
        python_callable=insrt_postgres,
        op_kwargs={
            'postgres_conn_id': 'conn-db-postgres-custom',
            'tbl_nm': 'TbCorona19CountStatus_bulk2',
            'file_nm': '/opt/airflow/files/TbCorona19CountStatus/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash}}/TbCorona19CountStatus.csv'
        }
    )
