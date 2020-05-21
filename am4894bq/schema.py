# AUTOGENERATED! DO NOT EDIT! File to edit: 01_schema.ipynb (unless otherwise specified).

__all__ = ['get_schema', 'dtype_to_bqtype', 'df_to_bq_schema', 'schema_diff', 'update_bq_schema', 'update_df_schema']

# Cell
#export
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from google.cloud import bigquery

# Cell


def get_schema(table_id: str) -> list:
    """
    Get schema given a table_id.
    """
    client = bigquery.Client()
    table = client.get_table(table_id)
    schema = table.schema
    return schema



# Cell


def dtype_to_bqtype(dtype, default_type: str = 'STRING') -> str:
    """
    Convert from a pandas type to BigQuery type.
    """
    bqtype = default_type
    if dtype == 'int64':
        bqtype = 'INTEGER'
    return bqtype



# Cell


def df_to_bq_schema(df: pd.DataFrame) -> list:
    """
    Read a pandas DF and return a BigQuery schema for that DF.
    """
    schema = []
    for col, dtype in df.dtypes.iteritems():
        schema.append(bigquery.SchemaField(col, dtype_to_bqtype(dtype)))
    return schema



# Cell


def schema_diff(old_schema, new_schema) -> list:
    """
    Compare two BigQuery schemas and return a list of differences.
    """
    old_schema_dict = {col.name:col for col in old_schema}
    new_schema_dict = {col.name:col for col in new_schema}
    diffs = []
    for col in new_schema_dict:
        if col not in old_schema_dict:
            diffs.append(('add', new_schema_dict[col]))
        elif new_schema_dict[col] != old_schema_dict[col]:
            diffs.append(('update', old_schema_dict[col], new_schema_dict[col]))
    for col in old_schema_dict:
        if col not in new_schema_dict:
            diffs.append(('drop', old_schema_dict[col]))
    return diffs



# Cell


def update_bq_schema(bq_client, table_id: str, diffs: list, print_info: bool = True) -> bool:
    """
    Given a list of diffs and a table_id add any new columns to table.
    """
    # only do work if some 'add's in diffs
    if 'add' in [diff[0] for diff in diffs]:
        table = bq_client.get_table(table_id)
        current_schema = table.schema
        current_schema_col_names = [col.name for col in current_schema]
        for diff in diffs:
            if diff[0] == 'add':
                bq_schema_field = diff[1]
                col_name = bq_schema_field.name
                if col_name not in current_schema_col_names:
                    if print_info:
                        print(f'adding {bq_schema_field} to {table_id}')
                    new_schema = current_schema[:]
                    new_schema.append(bq_schema_field)
                    table.schema = new_schema
                    table = bq_client.update_table(table, ["schema"])
    return True



# Cell


def update_df_schema(bq_client, table_id: str, diffs: list, df: pd.DataFrame, print_info: bool = True) -> pd.DataFrame:
    """
    Given a list of diffs add any columns expected but not found in df.
    """
    # only do work if some 'drops's in diffs
    if 'drop' in [diff[0] for diff in diffs]:
        for diff in diffs:
            if diff[0] == 'drop':
                col_name = diff[1].name
                if col_name not in df.columns:
                    if print_info:
                        print(f'adding {col_name} to df')
                    df[col_name] = None
    table = bq_client.get_table(table_id)
    bq_schema = table.schema
    bq_schema_col_names = [col.name for col in bq_schema]
    df = df[bq_schema_col_names]
    return df

