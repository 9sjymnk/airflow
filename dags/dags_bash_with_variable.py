import pendulum
# Airflow 3.0 부터 아래 경로로 import 합니다.
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="dags_bash_with_variable",
    schedule="10 9 * * *",
    start_date=pendulum.datetime(2023, 4, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:

    # Airflow Variable을 실행 시점에만 불러오기 (Jinja template)
    bash_var_1 = BashOperator(
        task_id="bash_var_1",
        bash_command="echo variable:{{ var.value.sample_key | default('default_value') }}"
    )

    # 다른 태스크에서도 동일하게 적용 가능
    bash_var_2 = BashOperator(
        task_id="bash_var_2",
        bash_command="echo variable:{{ var.value.sample_key | default('default_value') }}"
    )
