export HTTP_PROXY=http://proxy
export HTTPS_PROXY=http://proxy
./wget.exe -O Data_raw_punctuality_202302.csv https://fr.ftp.opendatasoft.com/infrabel/PunctualityHistory/Data_raw_punctuality_202302.csv
./wget.exe -O operationele-punten-van-het-newterk.json https://opendata.infrabel.be/api/explore/v2.1/catalog/datasets/operationele-punten-van-het-newterk/exports/json?lang=fr&timezone=Europe%2FBerlin
az login
az acr build --registry wazerailregistry --resource-group waze-rail --image streamlit-app .
