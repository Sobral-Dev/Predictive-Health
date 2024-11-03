flask db init  # Apenas na primeira vez
flask db migrate -m "Initial migration"
flask db upgrade
