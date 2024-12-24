# Customer Churn Analytics Platform

An end to end analytics platform that models and visualizes customer churn. The project blends together concepts from data engineering, analytics engineering, and MLOps.

![Dashboard Preview](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/dashboard.png)

![Monitoring Dashboard](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/monitoring_dashboard.png)
# Overview

This project was developed to:
 - Employ various elements of the modern data stack
 - Be applied to a somewhat realistic business use case
 - Serve as a template for others to learn from and use via extensive documentation
# What's Next?
 - ~~Model retraining pipelines with Experiment Tracking using MLflow~~
 - ~~Automated model deployment using MLflow Model Registry~~
 - ~~Monitoring using Evidently and Grafana~~
 - Implement unit and integration tests for Airflow functions.
 - Develop SCD2 functionality for dimension tables.
 - Evaluate feasibility of incremental refresh (models) via dbt to prevent overhead.

## Project Architecture

![Architecture Diagram](https://raw.githubusercontent.com/raashidsalih/churn-pipeline/main/assets/architecture.svg)

For this project, the Telco Customer Churn data module which is a sample dataset on IBM's Cognos Analytics platform was selected because it seemed like the best representative considering the difficulty in finding a decent dataset for the use case.

The dataset is then used to train two models. The first is a Gaussian Copula Synthesizer to produce synthetic data with characteristics similar to the original. This is done since there is not much data to go around and serves as a rudimentary imitation of data entering the database, The second is the product of using FLAML's AutoML implementation on the data, and its purpose is to predict churn status for a particular user. These experiments are tracked using MLFlow for better observability and minIO is employed as an object store for the various artefacts involved.

The synthesizer model is hosted via FastAPI, while the classifier is deployed with MLFlow model registry, which dynamically exposes the latest "Champion" model for inference. Airflow is then used to orchestrate the pulling of data from the Synthesizer, obtaining churn status prediction for said data from the classification model, generating a ULID for each customer, and writing it all to a Postgres database. It then triggers dbt afterward to run tests and apply necessary transformations. Airflow is used to record model metrics at a regular frequency and also to retrain the classifier. The data is modeled after the star schema and is finally visualized as a dashboard using Metabase. The various model metrics are stored and is monitored with Grafana to proactively deal with any problems that may arise.

![Data Model Diagram](https://raw.githubusercontent.com/raashidsalih/churn-pipeline/main/assets/star.svg)

Almost all of the services above run in their own docker containers, as seen in the diagram. These containers are running on a GCP VM, provisioned via Terraform. Finally, GitHub Actions facilitates CI/CD, as the code is quickly checked for any issues using Ruff and changes made to this repo are reflected in the VM.

## Some points to consider

 1. Keep in mind that predicting customer churn is a rather sophisticated use case and is difficult to get right. AutoML was only employed to obtain a viable baseline model, and this is how it should be applied most of the time. Check out [Fighting Churn with Data](https://www.amazon.com/Fighting-Churn-Data-Carl-Gold/dp/161729652X) for a more comprehensive outlook on modelling customer churn.
 2. The original dataset has been transformed and [can be found here](https://github.com/raashidsalih/churn-pipeline/tree/main/source_data). This is the dataset the models have been trained on.
 3. As mentioned earlier, the various elements which comprise this project have tried to be documented. Most files should have accompanying comments to facilitate understanding, and more high level system design justifications can be found in the README below.

# Running pipeline yourself
If you want to run the pipeline on your own, here are some considerations:

 - The Docker Compose file is the crux of this project, so that is a good starting point.
 - Rename sample.env to .env
 - Double check the ports for the various docker services if project is run locally. Ensure it doesn't conflict with ports used by other services on the system.
 - Add path to credentials file and locally generated SSH files in the [Terraform main file (main.tf)](https://github.com/raashidsalih/churn-pipeline/blob/main/terraform/main.tf).
 - Replace variables in [variables.tf](https://github.com/raashidsalih/churn-pipeline/blob/main/terraform/variables.tf) to your liking.
 - If CD implementation is going to be used, make changes to the output filepath (if necessary), and add necessary GitHub secrets.
 - Add Postgres connection information to Airflow with name pg_conn.
 - You can use the backup under the ```assets``` folder to recreate the Grafana dashboard.
 - Beware of port forwarding if Terraform is being used to create the VM that the project runs on. If the instance external IP address is known, anyone can gain access to the running Docker containers.

# Concepts Employed
## 1. ML Models
### 1. AutoML Model
-   Used to quickly obtain a viable baseline
-   Selected Microsoft's FLAML because it had more streamlined access to core AutoML use cases.
-   Total training time facilitates a threshold for training, and can be modified.
-   Used predict_proba as a crude proxy for confidence. It can benefit from calibration for a more reliable measure.

### 2. Data Synthesizer Model
-   Went for this design to obtain something akin to realtime data
-   Ended up with a gaussian copula model from the SDVault library
-   Initially wanted to go with the popular [CTGAN model from this paper](https://arxiv.org/abs/1907.00503), but the final model was an order of magnitude bigger and performed about the same as the GCop Model
-   Size and speed of inference is important since the model going into production
-   Constraints are added such that location data is generated consistently (i.e. you don't get random city associated with random zip code)

## 2. ULID

 - Stands for Universally Unique Lexicographically Sortable IDentifier, used as primary key to uniquely identify each customer.
 - An implementation of UUID (Universally Unique IDentifier), thus inheriting its advantages over a standard autoincrementing integer based primary key, namely robust uniqueness and security.
 - In addition, since ULID is generated client side (as opposed to autoincrement), it prevents the need for going back to the primary source table to get the ID number to write to other tables.
 - ULID also overcomes one of the major drawbacks associated with using UUIDs, which is the lack of sortability. This is of course until newer versions of UUID (like v6) that solve this problem are standardized.
 - Generated using the [python-ulid](https://github.com/mdomke/python-ulid) library, and converted to UUID format to be inserted into Postgres.
 - One drawback is how the relatively large size of ULID (and UUIDs in general) affects performance, but that remains to be seen.

## 3. Modeling
-   Went with the tried and tested star schema (Kimball approach) for this project
-   Briefly considered the recent one big table implementation as that would have the consequence of reducing data transformations.
- However, we don't have close to the amount of data necessary to see any real performance gains and it seems like falling into the trap of premature optimization.
-   Plus, this approach better facilitates data integrity and ease of understanding.

## 4. CI/CD
-   Fast lint check using Ruff
-   Uses a GitHub actions module (appleboy) that SSHs into the VM and pull --rebase(s) this GitHub repo.
-   Triggered on push to repo.

## 5. Testing
-   Testing applied just for data (for now) at beginning of transformation layer via dbt.
-   Only applied at source since the subsequent transformations don't affect the conditions checked by test.
-   Plus, having redundant tests just increases performance overhead.

## 6. MLOps
-   MLflow is used to track experiments and log relevant metrics and artifacts. Since FLAML's AutoML is used to train the classifier, the best model is then entered into the model registry.
-   Deployment is automated via loading the "Champion" model from the registry for inference.
-   Model retraining is triggered at period intervals, but can also happen when performance drops beyond a set threshold.
-   Monitoring of such drops in performance is facilitated by Grafana, which can also be set up to alert you when such situations occur.

# Technologies Used
## 1. Docker Compose
- Defines services for Postgres, pgAdmin, Airflow, FastAPI server, and Metabase.
- Persistent volumes mapped to services for backup purposes.
- Use env file for environment variables available throughout.

## 2. FastAPI
 - Data synthesis and prediction models handled via one server.
 - This is done to reduce overhead in setting up and maintaining multiple servers for services.
 - Serves as an example of both serving a model for inference, and pulling from a model for synthetic data.

## 3. Postgres and pgAdmin
-   Schema and tables created on startup.
-   pgAdmin included for GUI, can also consider DBeaver.
-   ULID for primary key handled by native UUID datatype.
-   Also hosts Metabase metadata.

## 4. Airflow
-  ![Airflow UI](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/airflow.png)
- ![Airflow DAG Graph](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/airflow_dag.png)  
- Tasks are parallelized for efficiency.
-   Use jinja scripting to pull XCom data into Postgres database.

## 5. dbt
-   ![dbt DAG](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/dbt_dag.png)
- dbt Core used in Airflow container, `dbt build` triggered via `BashOperator`.
- This implementation can be dangerous if there is the potential for resource or environmental clashes between the two services, so be wary. It would be wise to utilize tools like `pyenv`, `poetry`, or the more modern `uv` by Astral to sidestep this particular problem.
- If you have the Kubernetes infrastructure handy, you can also do the same with `KubernetesPodOperator`for containerization and scalability.
- Difficult to integrate dbt Cloud with Airflow unless using something like [Astronomer's Astro CLI.](https://docs.astronomer.io/learn/airflow-dbt-cloud)
-  At a production level, the de facto method of using dbt is via:
	- dockerizing the project
	- hosting it on an image registry
	- Airflow triggers job from most recent image
	- Every github push updates the image in the registry
-  The aforementioned methods were not pursued in the interest of keeping the project (relatively) straightforward, but they can be considered.

## 6. Metabase
 - Acts as visualization layer
 - Selected because it is quick to set up and put together a decent result.
 - Dashboards developed can be shared publicly, and is therefore highly accessible.
 - However, the link does expose the system's external IP, so that is something to be kept in mind.

## 7. Terraform
-   Spin up and tear down VMs quickly and reliably for rapid experimentation.
-   Use output values for convenience and SSH capabilities.

## 8. GCP VM
-   VM instance type determined via trial and error.
-   Once again, be wary of port forwarding and general firewall settings.

## 9. MLflow
 - ![MLflow UI](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/mlflow.png)
 - The MLflow server is hosted on the same container as airflow. This was to reduce the additional overhead caused by the need for inter-container communication if the need arose.
 - [You can read more about it here](https://stackoverflow.com/questions/59035543/how-to-execute-command-from-one-docker-container-to-another). Your options are exposing the host socket (very dangerous), setting up SSH between the instances (cumbersome), or using a Flask extension and wrapping bash access around a REST API (long term support is questionable).
 - The backend store is handled by the same postgres instance, while minIO handles object store.
 - A custom FastAPI wrapper deals with deployment for flexibility with predict_proba, but one can use MLflow's native support for serving models via Flask, Seldon's ML Server, Kubernetes, or other cloud platforms.

## 10. minIO
 - ![minIO UI](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/minio.png)
 - Acts as object store for MLflow artifacts
 - Serves as a proxy for cloud native storage, think AWS S3 and its analogs
 - A single bucket deals with MLflow output. However, it can be scaled to other use cases.

## 11. Grafana
 - ![Grafana dashboard](https://github.com/raashidsalih/churn-pipeline/blob/main/assets/monitoring_dashboard.png)
 - Connects with our Postgres instance to obtain modal metric data
 - Alerts can be set at determined threshold for each metric
 - Model inference latency and other operational metrics can be considered, especially in conjunction with Prometheus
 - Dashboard layout as seen can be obtained from ```assets``` folder.
