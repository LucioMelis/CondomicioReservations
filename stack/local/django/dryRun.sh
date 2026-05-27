source stack/local/local.env

echo "Appling migrations ..."
python ${WEB_APP_ROOT}manage.py migrate
echo " --- DONE ---"

echo "Loading initial data ..."
python ${WEB_APP_ROOT}manage.py loaddata ${DJANGO_INITIAL_DATA_PATH}/*
echo " --- DONE ---"

echo "Running the server ..."
python ${WEB_APP_ROOT}manage.py runserver 0.0.0.0:8000