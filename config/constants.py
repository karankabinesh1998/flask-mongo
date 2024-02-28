import configparser
from urllib.parse import quote_plus

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Print sections to verify
print("Sections:", config.get('Server', 'ip'))

# Get MongoDB connection details
username = config['MongoDB']['username']
password = config['MongoDB']['password']
cluster_uri = config['MongoDB']['cluster_uri']

# Construct MongoDB URI with properly escaped username and password
MONGODB_URI = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{cluster_uri}/?retryWrites=true&w=majority&appName=Cluster0"


# Get values from the 'Server' section
SERVER_IP = config.get('Server', 'ip')
SERVER_PORT = config.getint('Server', 'port')  # To get integer values

# Get values from the 'JWT' section
SECRET_KEY = config.get('JWT','SECRET_KEY')
MAX_TOKENS = config.get('JWT','MAX_TOKENS')
