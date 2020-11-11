# AUTOGENERATED! DO NOT EDIT! File to edit: 03_pd.ipynb (unless otherwise specified).

__all__ = ['bq_project_id', 'clean_colnames', 'cols_to_str', 'df_to_gbq']

# Cell
# export
import os
import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery
from .schema import get_schema, df_to_bq_schema, schema_diff, update_bq_schema, update_df_schema
from .utils import does_table_exist

load_dotenv()

bq_project_id = os.getenv('BQ_PROJECT_ID')

# Cell


def clean_colnames(df: pd.DataFrame, char_default: str = '_', bad_chars: str = '#:!. ') -> pd.DataFrame:
    cols_to_rename = {}
    for col in df.columns:
        if type(col) != str:
            cols_to_rename[col] = f"{char_default}{col}"
    if len(cols_to_rename) > 0:
        df = df.rename(columns=cols_to_rename)
    df.columns = df.columns.str.replace(f'[{bad_chars}]', char_default)
    return df



# Cell


def cols_to_str(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all columns in df to string.
    """
    for col, dtype in df.dtypes.iteritems():
        if dtype != 'object':
            df[col] = df[col].astype(str)
    return df



# Cell


def df_to_gbq(
    df: pd.DataFrame, destination_table: str, project_id: str, if_exists: str = 'append',
    print_info: bool = True, mode: str = 'pandas', cols_as_str: bool = False, clean_col_names: bool = True) -> pd.DataFrame:
    """
    Save df to BigQuery enforcing schema consistency between df and destination table if it exists.
    """

    # remove bad chars that are not allowed in field names in bq
    if clean_col_names:
        df = clean_colnames(df)

    # only do anything if mode set to wrangle, otherwise just use pandas
    if mode == 'wrangle':

        table_id = f'{project_id}.{destination_table}'
        bq_client = bigquery.Client()

        # only need to handle schema's if table already exists and if_exists != 'replace'
        if does_table_exist(bq_client, table_id) and if_exists != 'replace' :

            old_schema = get_schema(table_id)
            new_schema = df_to_bq_schema(df)
            diffs = schema_diff(old_schema, new_schema)

            if len(diffs) > 0:

                # update the table schema in BigQuery
                update_bq_schema(bq_client, table_id, diffs, print_info=print_info)

                # update the df schema to be as expected by BigQuery
                df = update_df_schema(bq_client, table_id, diffs, df, print_info=print_info)

    if cols_as_str:
        df = cols_to_str(df)

    # load to BigQuery with a retry
    try:
        df.to_gbq(destination_table, project_id=project_id, if_exists=if_exists)
    except:
        df.to_gbq(destination_table, project_id=project_id, if_exists=if_exists)

    return df

