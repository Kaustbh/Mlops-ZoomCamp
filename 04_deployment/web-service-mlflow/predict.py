import pickle
from flask import Flask, request, jsonify
import mlflow
from mlflow.tracking import MlflowClient


tracking_uri="sqlite:////home/kaustubh/mlops_zoomcamp/Mlops-ZoomCamp/04_deployment/web-service-mlflow/mlflow.db"
mlflow.set_tracking_uri(tracking_uri)
run_id="af618559e8f9430482c5aa9b543b8294"

# client = MlflowClient(tracking_uri=tracking_uri)

# path = client.download_artifacts(run_id=run_id,path="vectorizer.bin")
# print(f"Downloading the dict vectorizer to {path}")


# with open(path,'rb') as f:
#     dv=pickle.load(f)



# Load model as a PyFuncModel.
logged_model = f'runs:/{run_id}/model'
model = mlflow.pyfunc.load_model(logged_model)



def prepare_features(ride):
    features={}
    features['PU_DO'] = '%s_%s' % (ride['PULocation'],ride['DOLocation'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    return preds[0]

app = Flask("duration-prediction")


@app.route('/')
def home():
    return "Welcome to the Flask App!"


@app.route('/predict',methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration':pred,
        "model_version":run_id
    }

    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=9696)