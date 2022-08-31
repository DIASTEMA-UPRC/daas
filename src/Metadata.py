import datetime
import pandas as pd

from typing import List

class Metadata:
    def __init__(self, features: List[str], name: str, source: str, location: str, usecase: str, samples: int, size: int, created_at: datetime.datetime=datetime.datetime.utcnow()):
        self.features   = features
        self.name       = name
        self.source     = source
        self.location   = location
        self.usecase    = usecase
        self.samples    = samples
        self.size       = size
        self.created_at = created_at
        self.updated_at = created_at


    def to_dict(self) -> dict():
        return {
            "features": self.features,
                "name": str(self.name),
              "source": str(self.source),
            "location": str(self.location),
             "usecase": str(self.usecase),
             "samples": int(self.samples),
                "size": int(self.size),
          "created_at": str(self.created_at),
          "updated_at": str(self.updated_at)
        }


    def to_new_features(self, df: pd.DataFrame):
        features = list()

        for i, x in enumerate(df.dtypes):
            column_name = str(df.columns[i])
            column_type = "str"
            
            
            if x == "int64":
                column_type = "int"
            elif x == "float64":
                column_type = "float"
            
            fc = dict()
            fc["name"] = column_name
            fc["type"] = column_type
            
            if column_type != "str":
                all_pos = True
                all_neg = True
                all_zero = True
                non_zero = False
                
                for x in df[column_name]:
                    if x > 0:
                        all_neg = False
                    if x < 0:
                        all_pos = False
                    if x != 0:
                        all_zero = False
                    if x == 0:
                        non_zero = True
                
                
                fc["positive"] = all_pos
                fc["negative"] = all_neg
                fc["non-zero"] = non_zero
                fc["all-zero"] = all_zero

            features.append(fc)

        self.features = features

    def from_dict(self, data: dict):
        self.features   = data["features"]
        self.name       = data["name"]
        self.source     = data["source"]
        self.location   = data["location"]
        self.usecase    = data["usecase"]
        self.samples    = data["samples"]
        self.size       = data["size"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


def get_metadata_of_df(df: pd.DataFrame) -> Metadata:
    metadata = Metadata(f"Dataset", "N/A", "N/A", "N/A", 0, 0, 0)
    metadata.samples += df.shape[0]
    metadata.features = df.columns.tolist()
    metadata.size += df.memory_usage(deep=True).sum()
    return metadata
