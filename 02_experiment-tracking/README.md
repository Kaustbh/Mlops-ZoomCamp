# What is experiment tracking? #

It is the process of tracking all the relevant information of machine learning experiments. Information such as
* Code
* Version
* Environment
* Data
* Model
* Artifacts
* Metrices
* Hyperparameters etc.

This helps in reproducibility, better organized way of doing the projects.

Next question could be how do we track then? Well, at a very basic level one might use excel to track the information manually but that is error prone, difficult to collaborate and does not have a standard template to cater to all the needs of tracking mechanism.

Is there are a better way of achieving this? Yes, there are many open source and proprietary tools that can be leveraged. MLFlow, Neptune, Weights and Biases, Comet.ml, Volohai, Tensorboard, SageMaker etc. In this tutorial we are not going to discuss about which one is better over the other, however, we are going to focus on MLFlow.

# What is MLFlow #

MLFlow is language-agnostic, open source and addresses all the aspects of entire machine learning life cycle including tracking, reproducibility, deployment and storage. MLFlow was open sourced by Databricks in 2018 and since then it has gained a lot of traction in adoption.

MLFlow is quite easy to use. It is just a python package that we can install using pip. It has following four elements -
* Tracking
* Projects
* Models
* Registry

## Tracking ##

MLFlow tracks all the runs or executions in an experiment. When we say run, that is basically an execution of some piece of data science code. The following information is tracked:
* Code version
* Start and end run times
* Source details
* Parameters
* Artifacts

MLFlow Tracking provides an API as well as an UI for logging required related information while running the code. It also lets you query the experiments using Python and a few other languages.

The next question is where is this tracking information is stored? For that MLFlow provides a number of options such as localhost, localhost with SQLite DB, localhost with tracking server, Remote tracking server and stores etc.

More details on MLFlow Tracking:  
https://mlflow.org/docs/latest/tracking.html

## Projects ##

It is a directory or a Git repo containing code files following a convention so that users or tools can run the project using its entry point(s). If a project contains multiple algorithms that can be run separately, in that multiple entry points are mentioned in MLProject file.

Properties of a project:
* Name - Name of the project
* Entry Points - Typically a .py or .sh file to run the entire project or some specific functionality, say an algorithm. List of entry points are mentioned in MLProject file
* Environment - Specifications such as library dependencies for the software environment for the code to run. Supported environments - conda environments, virtualenv environments, docker environments.

More details on MLFlow Projects:  
https://mlflow.org/docs/latest/projects.html

## Models ##

It is a directory where the model is saved along with a few related files denoting its properties, associated information and environment dependencies. Generally a model is served by a variety of downstream tools for serving in real time through REST API or in batch mode. And, the format or flavour of the saved model is decided based on which downstream tool is going to use for model serving. For example mlflow Sklearn library allows loading the model back as a scikit-learn pipeline object while mlflow sagemaker tool wants the model in python_function format. mlflow provides a powerful option for defining required flavours in MLmodel file.

A typical model directory contains the following files:   
* MLmodel - a YAML file describing model flavours, time created, run_id if the model was created in experiment tracking, signature denoting input and output details, input example, version of databricks runtime (if used) and mlflow version  
* model.pkl - saved model pickle file
* conda.yaml - environment specifications for conda environment manager  
* python_env.yaml - environment specification for virtualenv environment manager
* requirements.txt - list of pip installed libraries for dependencies

More details on MLFlow models:  
https://mlflow.org/docs/latest/models.html

## Model Registry ##

Enterprises conduct a lot of experiments and move the selected models to production. Having said that a lot of models are created and saved in mlflow Models. Some of them are for new requirements and rest as updated models for same requirements. We needed a versioning and stage transitioning system for the models, that is fulfilled by mlflow Model Registry.  

Model Registry serves as a collaborative hub where teams share models and work together from experimentation to testing and production. It provides a set of APIs as well as a UI to manage the entire life cycle of an mlflow model.
  
Model Registry concepts to manage life cycle of mlflow model:  
* Model - An mlflow model logged with one of the flavours ```mlflow.<model_flavour>.log_model()```
* Registered model - An mlflow model registered on Model Registry. It has a unique name, contains versions, transitional stages, model lineage and other associated metadata.
* Model Version - Version of the registered model
* Model Stage - Each distinct model version can be associated with one stage at a time. Stages supported are Staging, Production and Archived.
* Annotations and descriptions - Add useful information such as descriptions, data used, methodology etc. to the registered model.

More details on MLFlow Model Registry:  
https://mlflow.org/docs/latest/model-registry.html



## Getting Started with MLflow ##

***Note*** *Run in the local environment.*
### Prepare the environment ###
Run the following command to create a fresh new new conda virtual environment.  
```conda create -n exp-tracking-env python=3.9```
  
Next we activate the newly created environment.  
```conda activate exp-tracking-env```
  
Install the required packages listed in requirements.txt file.  
```pip install -r requirements.txt```

Launch mlflow ui as well. Run the following command to start mlflow ui (a gunicorn server) connected to the backend sqlite database.  
```mlflow ui --backend-store-uri sqlite:///mlflow.db```

To access mlflow ui open `https://127.0.0.1:5000` in your browser.

This is how it looks like.  
![](https://github.com/Kaustbh/Mlops-ZoomCamp/02_experiment-tracking/images/default.png)


## Note for MLflow tracking:
An MLflow tracking server has two components for storage: a backend store and an artifact store.

The backend store is where MLflow Tracking Server stores experiment and run metadata as well as params, metrics, and tags for runs. MLflow supports two types of backend stores: file store and database-backed store.

Use `--backend-store-uri` to configure the type of backend store. You specify a file store backend as `./path_to_store` or `file:/path_to_store` and a database-backed store as SQLAlchemy database URI. 
The database URI typically takes the format `<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>`. MLflow supports the database dialects ***mysql, mssql, sqlite***, and ***postgresql***. 
Drivers are optional. If you do not specify a driver, SQLAlchemy uses a dialect’s default driver. For example, `--backend-store-uri sqlite:///mlflow.db` would use a local SQLite database.

By default `--backend-store-uri` is set to the local `./mlruns` directory (the same as when running `mlflow run` locally), but when running a server, make sure that this points to a persistent (that is, non-ephemeral) file system location.

The artifact store is a location suitable for large data (such as an S3 bucket or shared NFS file system or as our use case: HDFS ) and is where clients log their artifact output (for example, models). artifact_location is a property recorded on mlflow.entities.Experiment for default location to store artifacts for all runs in this experiment. Additional, artifact_uri is a property on mlflow.entities.RunInfo to indicate location where all artifacts for this run are stored.

Use --default-artifact-root (defaults to local ./mlruns directory) to configure default location to server’s artifact store. This will be used as artifact location for newly-created experiments that do not specify one. Once you create an experiment, --default-artifact-root is no longer relevant to that experiment.


## Experiment tracking with MLflow

![](https://github.com/Kaustbh/Mlops-ZoomCamp/02_experiment-tracking/homework/images/experiment.png)

![](https://github.com/Kaustbh/Mlops-ZoomCamp/02_experiment-tracking/homework/images/experiment2.png)

![](https://github.com/Kaustbh/Mlops-ZoomCamp/02_experiment-tracking/homework/images/experiment3.png)


##  Model management
* Load model as an artifact:
`mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")`

* Log model using the method `log_model`:
`mlflow.<framework>.log_model(model, artifact_path = "models/")`


## Model registry
[Model Registry](https://mlflow.org/docs/latest/model-registry.html) is to manage life cycle of mlflow model for improving efficiency in developing:
![model_registry.png](images%2Fmodel_registry.png)

The concepts should be known:
* Model - An mlflow model logged with one of the flavours `mlflow.<model_flavour>.log_model()`
* Registered model - An mlflow model registered on Model Registry. It has a unique name, contains versions, transitional stages, model lineage and other associated metadata. 
* Model Version - Version of the registered model 
* Model Stage - Each distinct model version can be associated with one stage at a time. Stages supported are Staging, Production and Archived. 
* Annotations and descriptions - Add useful information such as descriptions, data used, methodology etc. to the registered model.

[Two workflow](https://mlflow.org/docs/latest/model-registry.html) for it, one is from UI, the other is from API.

1). UI workflow:

2). API workflow:


## MLflow in Practice ##

Depending upon the project and number of data scientists going to collaborate, the configurational aspect of mlflow is decided. Consider the following three scenarios.

* A single data scientist participating in a competition
* A cross-functional team with single data scientist
* Multiple data scientists working together on models

**Configure MLflow**
Let us consider following architectural components of mlflow. A mlflow tracking server has two components - Backend store and Artifact store. Depending upon the requirements we may need to have both of them locally or in a local server or a remote server.

* Backend store (Used to store metadata)
  * Local file system (When one participates in competition and needs to track experiments locally)
  * SQLAlchemy compatible DB such as SQLite (Locally but in a DB and DB is must to register models)
*  Artifact Store (To store model and other artifacts)
   *  Local file system (locally store in a folder when one does not need to share with others)
   *  Remote (Say, there is a need to store the artifacts in S3 bucket)


## MLflow: benefits, limitations and alternatives ##

**Benefits**
* Share and collaborate with other members
* More visibility into all the efforts
  
**Limitations**
* Security - restricting access to the server
* Scalability
* Isolation - restricting access to certain artifacts

**When not to use**
* Authentication and user profiling is required
* Data versioning - no in-built functionality but there are work arounds
* Model/Data monitoring and alerts are required

**Alternates**
* Nepture.ai
* Comet.ai
* Weights and Biases
* etc