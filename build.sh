# Install dependencies
pip install -r requirements.txt

# Collect static files into one directory
python manage.py collectstatic --no-input

# Run migrations
python3 manage.py migrate