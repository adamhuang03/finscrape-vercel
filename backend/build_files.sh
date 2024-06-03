echo "BUILD START"
echo "Installing Reqs"
python3 -m pip install -r requirements.txt

# echo "Making migrations"
# python3 manage.py makemigrations --noinput
# python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput
echo "BUILD END"