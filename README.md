# Grocery Management

This project is a web app to buy grocery items, which uses Google Sheets to get information about the grocery details such as item name, image, price etc and serve it to the user for ordering, once the user buys the items an email confirmation will be sent to them.

### Languages used

**Front-end**

- HTML
- CSS

**Backend-end**

- [Python](https://www.python.org/)(version: 3.10)
- [Google Sheets](https://www.google.com/sheets/about/)

### How it works

- A python server is running in the backend which will fetch information from the Google sheets url provided in the `data\stores.json`
- All the shops nearby will be listed
- User has to select a shop
- all the items in the shop will be displayed
- user selects the items
- Checkout page is displayed
- User has to enter the personal information
- The cart details will be present to the user
- once the user places the order, using the GMAIL credentials provided in the `.env` an email confirmation about the order details will be sent to the user.

### Requirements

- Python(version 3.10 or later)
  #### Python libraries
  - [**_FastAPI_**:](https://fastapi.tiangolo.com) Web application development framework
  - [**_Pandas_**:](https://pandas.pydata.org/) to read data from google sheet url and convert them to `JSON`
  - [**_Python-dotenv_**:](https://pypi.org/project/python-dotenv/) to store GMAIL credentials from which email will be triggered
- Browser(Chrome is recommended)
- Internet connection

### How to generate GMAIL credential

- Go to [My Account settings](https://myaccount.google.com/apppasswords?rapt=AEjHL4MHSjx3xJQhfDRLJ6NB4ZmT_qBJhbWkOyFuaYF-CSWpy50iEV-7BY6MJuuI93pB1QQ2ZxiD6UlcGcnEPnLNjQz3SQoGOg) in Google
- Generate a KEY for your python app
- Create a `.env` file on the same folder as `app.py`
- In the `.env` file insert the following lines and save the file

```
GMAIL_ID="Replace_this_with_your_email_id"
GMAIL_KEY="Replace_this_with_the_key_generated_from_step2
```

- Make sure to replace the strings with your credentials

### To Run

---

**First time**

To run make sure you have python along with flask

- fill in the GMAIL credentials in the `.env` file
- ensure to install the required dependencies using the below command under `Grocery Store` folder

  ```
  python -m pip install -r requirements.txt
  ```

- once the installation of packages are complete then you can simply run

**Always**

```
python main.py
```

- open your browser and navigate to the [localhost:8000](http://127.0.0.1:8000/) (or port you configured)

---
