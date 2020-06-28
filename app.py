# Imports
from flask import Flask

# App init
app = Flask(__name__)
app.debug = True

# Configs
# TO DO

# Modules
# TO DO

# Models
# TO DO

# Schema Objects
# TO DO

# Routes
# TO DO

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == 'main':
    app.run()
