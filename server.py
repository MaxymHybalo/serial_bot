from flask import Flask
from flask import render_template
import handlers
from utils.configurator import Configurator

app = Flask(__name__)

CONFIG_FILE = 'config.yml'

def load_config():
    return Configurator(CONFIG_FILE).from_yaml()

config = load_config()

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/buff', methods=['POST'])
def buff(name=None):
    params=[]
    handlers.set_buff(params, config)
    handlers.set_mode('buff', CONFIG_FILE)
    handlers.run_bot()
    return render_template('buff', name=name)