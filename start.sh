echo "Django"
python manage.py runserver 0.0.0.0:8001 &

echo "Worker"
celery -A MishooEPP_EPPNode worker --pool=solo --loglevel=info --purge &

echo "Beat"
celery -A MishooEPP_EPPNode beat  --loglevel=info