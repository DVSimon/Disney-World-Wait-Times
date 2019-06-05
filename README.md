<h1>TO RUN WEB SERVER LOCALLY: </h1>

Must install mongodb community edition.
run db: create db called rides_app_db and in that create collection parks. Import parks.json into this parks collection by using mongodb compass connecting to your local database and then click on the collection and do collection->import data and import parks.json. Importing outside of compass may lead to issues with number types such as longitude and latitude since the data was exported with compass so data can be manually entered from the parks.json if needed. From any directory, run "mongod --config /usr/local/etc/mongod.conf"  

Must pip install flask, xgboost, pandas, flask_cors, pymonogo
run flask: cd into server, run "FLASK_APP=server.py flask run"  

Must first install latest version of node and npm. Once node is installed must install angular-cli globally with npm install -g @angular/cli

run web app: cd into map-app, run "npm install" then run "ng serve"  
In order to properly render the map you must put your Google Maps API key in map-app/src/app/app.module.ts in the "apiKey" field in AgmCoreModule import. Also if you want to make api calls against your local flask server instead of the one on the ec2 change the url in the environment.ts file to localhost and the port you are running the local flask server before running ng serve. For instance if your local flask was running on port 8000 you would run set FLASK_URL in environment.ts to export 'http://localhost:8000/' Must run ng serve after making this change. If the environment.ts is not changed the url is currently set to the EC2 running the flask server.

<h1>TO RUN MACHINE LEARNING (note: Not needed, pickle files already included in server. Only to show generation of XGB pickle models): </h1>

NOTE: To view machine learning model generation(pickle files) go to MachineLearning and jupyter notebook the directory and go to ipynb file, to run you can run the ipynb file or the standalone python file.

1. Either use Jupyter notebook (install python library first) to view code implementation/run details OR run python standalone script to generate pickle models.

2. Requires XGB library installation + other basic ML libraries(sklearn, scipy, pickle), must have GPU processing power, takes a while to run as many data rows/columns.

3. All CSV's for dataset can also be found in MachineLearning Folder

<h1> Website: http://ec2-54-201-84-148.us-west-2.compute.amazonaws.com/ </h1>
