from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from extract_data import ExtractData
from urllib.parse import urlparse, parse_qs
from uuid import uuid4
import uvicorn
import os
from datetime import date
import jinja2

app = FastAPI()

# stores data is stored here
data_file = "data/stores.json"

static_directory = "static"
templates_directory = f"{static_directory}/templates"  # html files
assets_directory = f"{static_directory}/assets"  # image files
styles_directory = f"{static_directory}/styles"  # css files
scripts_directory = f"{static_directory}/scripts"  # java script files

templates = Jinja2Templates(directory=templates_directory)

app.mount(
    "/templates",
    StaticFiles(directory=templates_directory, html=True),
    name="templates",
)
app.mount("/assets", StaticFiles(directory=assets_directory), name="assets")
app.mount("/styles", StaticFiles(directory=styles_directory), name="styles")
app.mount("/scripts", StaticFiles(directory=scripts_directory), name="scripts")

store_data = ExtractData(data_file)
items = store_data.grocery_data()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "data": store_data.data}
    )


@app.get("/store/{id}")
def store(request: Request, id: int):
    data = [item for item in items for i in item if i["store_id"] == id]
    return templates.TemplateResponse(
        "items.html", {"request": request, "data": data[0]}
    )


def parse_items_query(store_id, queries):
    checkout_items = []
    store_items = [item for item in items for i in item if i["store_id"] == store_id][0]
    print("data", store_items)
    total = 0.00
    for k, v in queries.items():
        for item in store_items:
            if item["id"] == int(k[3:]):
                total_price = item["Price"] * int(v[0])
                checkout_items.append(
                    {
                        "name": item["Item name"],
                        "total_price": total_price,
                        "count": v[0],
                        "price": item["Price"],
                        "quantity_type": item["Quantity type"]
                    }
                )
                total += total_price
    return (checkout_items, total)


@app.get("/checkout.html/store/{id}/")
def checkout(request: Request, id: int):
    res = urlparse(str(request.url))
    queries = parse_qs(res.query)
    print(queries)
    checkout_items, total = parse_items_query(id, queries)
    print("out", checkout_items)
    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "data": checkout_items,
            "total": total,
            "cart_items": len(queries),
            "item_query": res.query,
            "store_id": id,
        },
    )


def render_template(template, **kwargs):
    """renders a Jinja template into HTML"""

    templateLoader = jinja2.FileSystemLoader(searchpath=templates_directory)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template)
    return template.render(**kwargs)


@app.get(
    "/send-email/store/{store_id}/item-query/{item_query}/", response_class=HTMLResponse
)
def send_email(
    request: Request,
    store_id: int,
    item_query: str,
    firstName: str,
    lastName: str,
    email: str,
    address: str,
    city: str,
    state: str,
    zip: str,
    address2: str | None = None,
):
    """Warning: DO NOT rename any variable as they are used in the template file"""

    checkout_items, total = parse_items_query(store_id, parse_qs(item_query))
    import smtplib

    # Import the email modules
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    from dotenv import load_dotenv

    load_dotenv()
    GMAIL_ID = os.environ["GMAIL_ID"]
    GMAIL_KEY = os.environ["GMAIL_KEY"]

    order_id = str(uuid4()).split("-")[0]
    name = f"{firstName} {lastName}"
    current_date = date.today().strftime("%b-%d, %Y")
    print("date",current_date)

    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_ID
    msg["Subject"] = "Grocery store: Your order confirmation"
    msg["To"] = email
    template = render_template(f"email_template.html", **locals())
    msg.attach(MIMEText(template, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ID, GMAIL_KEY)
        smtp.send_message(msg)
    print("email sent")
    return template


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
