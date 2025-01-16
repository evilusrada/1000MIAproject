@echo off
echo Iniciando la aplicacion...

:: Activar el entorno virtual
call venv\Scripts\activate

:: Iniciar FastAPI en una nueva ventana
start cmd /k "venv\Scripts\activate && uvicorn api.main:app --reload"

:: Esperar 2 segundos para que FastAPI inicie
timeout /t 10

:: Iniciar Streamlit en una nueva ventana
start cmd /k "venv\Scripts\activate && streamlit run frontend/streamlit_app.py"

echo Aplicacion iniciada! Las ventanas de FastAPI y Streamlit se han abierto.