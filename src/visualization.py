import os
import pandas as pd

from autoviz.AutoViz_Class import AutoViz_Class
from io import BytesIO
from uuid import uuid4

from jinja2 import Environment, BaseLoader

from pymongo.typings import _DocumentType
from typing import Optional

from MinIO import MinIO

av = AutoViz_Class()

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrics</title>
</head>
<body>
    {% for metric in metrics %}
        <section>
            <h1>{{ metric.name }}</h1>
            <p>{{ metric.value }}</p>
        </section>
    {% endfor %}
</body>
</html>
"""


def visualization(minio: MinIO, minio_input: str, minio_output: str, analytics: Optional[_DocumentType]):
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

    if analytics is None:
        return

    metrics = list()
    f1 = analytics.get("f1", 0)
    metrics.append({ "name": "f1", "value": f1 })
    accuracy = analytics.get("accuracy", 0)
    metrics.append({ "name": "accuracy", "value": accuracy })
    r2 = analytics.get("r2", 0)
    metrics.append({ "name": "r2", "value": r2 })
    rmse = analytics.get("rmse", 0)
    metrics.append({ "name": "rmse", "value": rmse })

    env = Environment(loader=BaseLoader)
    template = env.from_string(BASE_HTML).render(metrics=metrics)

    with open(os.path.join(plot_dir, "metrics.html"), "w") as metrics_file:
        metrics_file.write(template)
        
    with open(os.path.join(plot_dir, "metrics.html"), "r") as metrics_file:
        metrics = metrics_file.read().encode("utf-8")
        metrics_size = len(metrics)
        metrics = BytesIO(metrics)
        metrics.seek(0)
        bucket, filename = minio_output.split("/", 1)
        minio.put_object(bucket, f"{filename}/metrics.html", metrics,
                         metrics_size)

