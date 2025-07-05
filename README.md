1) create a python enviroments using "python -m venv .venv"
2) if pip installer exist ,than using it install requirements.py file with this "pip install -r requirements.txt"
3) create a .env file ,than add thse
4) SECRET = "YOURSECRETKEY" 
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME="your gmeail"
SMTP_PASSWORD=nrwcltyubmalirxo  # Use Gmail App Password (not your real password)
RESET_PASSWORD_URL=https://yourfrontend.com/reset-password
VERIFY_EMAIL_URL=https://yourfrontend.com/verify-email
5)now using uvicorn main:app run your code
