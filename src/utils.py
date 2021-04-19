import base64
import logging
import numpy as np
import pandas as pd
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='table', index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def excel_download_link(df: pd.DataFrame, file_name: str = 'extract.xlsx', link_str: str = 'Download file'):
    """Generates a link allowing the data in a given panda dataframe to be downloaded

    Arguments:
    - df: pandas.DataFrame to be converted as excel.
    - file_name: Excel's file name.
    - link_str: Link name (string).
     
    Returns:
    - HTML link tag <a></a>
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    # decode b'abc' => abc
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download={file_name}>{link_str}</a>'

def try_float(value):
    try:
        value = float(value)
    except:
        pass
    finally:
        return value

def try_int(value):
    try:
        value = int(value)
    except:
        pass
    finally:
        return value

def norm_df_dtypes(df: pd.DataFrame):
    """
    Infer Pandas dtypes.

    Arguments:
    - df: pandas.DataFrame

    Returns:
    - df with dtypes identified.
    """
    for col in df.columns:
        dtype = None

        # Floats
        try:
            df[col] = [try_float(i) for i in df[col]]
            dtype = "float"
        except:
            pass

        # Ints
        if dtype is None:
            try:
                df[col] = [try_int(i) for i in df[col]]
                dtype = "int"
            except:
                pass

        # Datetime
        if dtype is None:
            try:
                df[col] = pd.to_datetime(df[col], infer_datetime_format=True, utc=True).astype('datetime64[ns]')
                dtype = "datetime"
            except:
                pass

    df.fillna(np.nan, inplace=True)
    return df