# apitoken
To Startup configure .env using .env.production

```py
uvicorn app.main:app --host 0.0.0.0  --reload
```
## To execute using vscode
To Run project using uvicorn run:
- Python: Uvicorn -> Ctrl + F5

To Run project using uvicorn Run And Debug:
- Python: Uvicorn -> F5

In the TAB Run and Debug "Ctrl + Shift + D" can select, run all project or run single file

For Single File 
To Run project using uvicorn run:
- Python: Run Single File -> Ctrl + F5

To Run project using uvicorn Run And Debug:
- Python: Run Single File -> F5

> In both Cases, the file .vscode/launch.json load file .env to environment variables