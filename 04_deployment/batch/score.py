#!/usr/bin/env python
# coding: utf-8

import os
import sys
import uuid
import pickle
from datetime import datetime
import pandas as pd
import mlflow
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline


mlflow.set_tracking_uri("sqlite:////home/kaustubh/mlops_zoomcamp/Mlops-ZoomCamp/04_deployment/web-service-mlflow/mlflow.db")
mlflow.set_experiment("deployment_experiment")

tracking_uri="sqlite:////home/kaustubh/mlops_zoomcamp/Mlops-ZoomCamp/04_deployment/web-service-mlflow/mlflow.db"
mlflow.set_tracking_uri(tracking_uri)
run_id="af618559e8f9430482c5aa9b543b8294"


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids


def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts

def load_model(run_id):
    logged_model = f'runs:/{run_id}/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def apply_model(input_file, run_id, output_file):
    
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)
    
    model = load_model(run_id)
    y_pred = model.predict(dicts)

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id

    df_result.to_parquet(output_file, index=False)
    

def run():

    taxi_type = sys.argv[1] # 'green'
    year = int(sys.argv[2]) # 2021
    month = int(sys.argv[3]) # 3

    input_file = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    output_file = f"output/{taxi_type}/{year:04d}-{month:02d}.parquet"

    apply_model(
        input_file=input_file,
        run_id=run_id,
        output_file=output_file
    )


if __name__ == '__main__':
    run()
