import os
import pandas as pd

from autoviz.AutoViz_Class import AutoViz_Class
from io import BytesIO
from uuid import uuid4

from MinIO import MinIO

av = AutoViz_Class()


def visualization(minio: MinIO, minio_input: str, minio_output: str):
    bucket, filename = minio_input.split("/", 1)

    print(bucket, filename)

    response = minio.get_object(bucket, filename)
    buffer = BytesIO(response.read())
    buffer.seek(0)
    df = pd.read_csv(buffer)
    plot_dir = f"/tmp/{uuid4().hex}"

    print("Saving plot to", plot_dir)

    av.AutoViz(
        filename="",
        sep=",",
        depVar="",
        dfte=df,
        header=0,
        verbose=2,
        lowess=False,
        chart_format="html",
        max_rows_analyzed=150000,
        max_cols_analyzed=30,
        save_plot_dir=plot_dir,
    )

    plot_av_dir = os.path.join(plot_dir, "AutoViz")

    for f in os.listdir(plot_av_dir):
        if not f.endswith(".html"):
            continue

        print("Visualizing file", f)

        with open(os.path.join(plot_av_dir, f), "r") as plot_file:
            plot = plot_file.read().encode("utf-8")
            plot_size = len(plot)
            plot = BytesIO(plot)
            plot.seek(0)
            bucket, filename = minio_output.split("/", 1)
            minio.put_object(bucket, f"{filename}/visualization_{f}", plot,
                             plot_size)
