### Flask Application README

# Setup Instructions

Follow these steps to set up and run the Flask application.

**1. Creating a Virtual Environment**
Open a terminal or command prompt and navigate to the directory where you want to create your project. Then, run the following command:
```
python3 -m venv myenv
source myenv/bin/activate
```
NOTE: 
for deactivate 

```
deactivate
```

**2. Install Dependencies**
Install the required Python packages using pip:

```
pip install -r requirements.txt
```
**3. Configuration**
Configure the application using the config.ini file. Update the configuration parameters as needed.
- configure the .ini file note: samples provided

**4. Run the Application**
Run the Flask application:

```
python app.py
```
The application will start running on http://localhost:5000 by default.

**5. Run Api's**

- Get Access Token from login-api 
_ Postman curl calls provided in postman folder

# File Structure
- app.py: Main Python file to run the Flask application.
- config.ini: Configuration file for the application settings.
- requirements.txt: List of Python packages required for the application.
- src/: Directory containing the source code of the Flask application.
-- auth/: Authentication-related files (if applicable).
-- product/: Product-related files (if applicable).
...: Other modules or components of the application.

# Additional Notes
- Make sure to update the configuration file (config.ini) with the appropriate settings for your environment.
- Customize the application routes, controllers, and models as needed based on your requirement