# Smart Document Scanner
This is a document scanner web application along with the  feature of optical character recognition aka. image to text conversion, built using Flask.

---

### 1. Installation

#### i. Locally

1. Clone this repo
2. Create an .env file in a project root directory and add the following information

   ```
    APP_NAME="smart-document-scanner"
    SECRET_KEY="<random>"
    DEBUG=True
    SSL_DISABLE=True
   ```
3. Install `Tesseract OCR` from ![here](https://tesseract-ocr.github.io/tessdoc/Installation.html)
4. Install all the dependencies
   ```bash
   pip install -r "requirements.txt"
   ```
5. Run
   ```bash
   python manage.py
   ```
6. Check: http://localhost:5000
#### ii. Using Docker

1. Clone the repo
2. Install [docker](https://docs.docker.com/get-docker/)
3. Create an .env file in a project root directory and add the following information

   ```
    APP_NAME="smart-document-scanner"
    SECRET_KEY="<random>"
    DEBUG=True
    SSL_DISABLE=True

   ```
4. Run
   ```bash
   docker compose up
   ```
5. Check: http://0.0.0.0:8080


Happy Coding !