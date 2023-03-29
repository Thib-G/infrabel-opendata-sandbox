# Test Streamlit app

Follow https://towardsdatascience.com/deploying-a-streamlit-web-app-with-azure-app-service-1f09a2159743 to deploy to Azure

Deploy with

```
az login
az acr build --registry wazerailregistry --resource-group waze-rail --image streamlit-app .
```

Demo on https://streamlit-opendata-app.azurewebsites.net/
