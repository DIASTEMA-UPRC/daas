import uuid
import requests
import os
import io
import pandas as pd
from Metadata import Metadata, get_metadata_of_df

from MinIO import MinIO
from requests.auth import HTTPBasicAuth
from load import load_file_as_dataframe
from typing import Tuple, List
from io import StringIO

CHUNK_SIZE = 4096


def download(url: str, token: str, separator: str, first_line_labels: bool, labels: List[str], path="/tmp", name=uuid.uuid4().hex) -> Tuple[str, Metadata]:
    print(f"Starting {url} download")

    extension = url.split(".")[-1]
    f_name = os.path.join(path, f"{name}.{extension}")

    if token == "":
        auth = HTTPBasicAuth("apikey", token)
    else:
        auth = None

    data = ""

    try:
        with requests.get(url, auth=auth) as r:
            r.raise_for_status()
            data = r.content.decode("utf-8")
    except Exception as e:
        print("Failed to download")
        print(e)
        raise Exception("Failed to download!")

    df = pd.DataFrame()
    
    if first_line_labels:
        df = pd.read_csv(StringIO(data), sep=separator)
    else:
        df = pd.read_csv(StringIO(data), sep=separator, header=None, names=labels)

    metadata = get_metadata_of_df(df)

    print(f"{f_name} downloaded")

    return df, metadata, f_name


def upload(df: pd.DataFrame, name: str, minio: MinIO, minio_output: str):
    print(f"Starting {name} upload")

    output_bucket = minio_output.split("/")[0]
    output_path = minio_output.partition("/")[-1]

    f_name = f"{output_path}/{name.rsplit('/', 1)[-1]}"

    try:
        df_data = df.to_csv(index=False).encode("utf-8")
        df_length = len(df_data)
        df_data = io.BytesIO(df_data)
        df_data.seek(0)

        minio.put_object(output_bucket, f_name, df_data, df_length, content_type="application/csv")
    except Exception as e:
        print(e)
        raise Exception("Failed to download!")

    print(f"{f_name} uploaded")
