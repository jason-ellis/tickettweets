#!venv/bin/python
from app import app
from multiprocessing import Process

p2 = Process(target=app.run(debug=True))
p2.daemon = True
p2.start()