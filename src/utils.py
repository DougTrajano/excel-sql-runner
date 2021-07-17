import os
import pathlib
import base64
import logging
import numpy as np
import pandas as pd
from io import BytesIO


def setup_logger():
    # Create logger instance
    logger = logging.getLogger(__name__)

    if not logger.handlers:
        # Define formatter
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s :: %(message)s')

        # Define handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    
    return logger


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
    except Exception:
        pass

    return value


def try_int(value):
    try:
        value = int(value)
    except Exception:
        pass

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
        except Exception:
            pass

        # Ints
        if dtype is None:
            try:
                df[col] = [try_int(i) for i in df[col]]
                dtype = "int"
            except Exception:
                pass

        # Datetime
        if dtype is None:
            try:
                df[col] = pd.to_datetime(
                    df[col], infer_datetime_format=True, utc=True).astype('datetime64[ns]')
                dtype = "datetime"
            except Exception:
                pass

    df.fillna(np.nan, inplace=True)
    return df

def remove_files_by_extension(path: str = None, extension: str = ".sqlite"):
    """Remove files from a given path based on a given extension."""
    if path is None:
        path = pathlib.Path(__name__).parent.resolve() 
    
    for file in os.listdir(path):
        if file.endswith(extension):
            logger.info(f'Removing file {file}')
            os.remove(os.path.join(path, file))

logger = setup_logger()