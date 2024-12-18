import random
import json
import string
from fastapi import Depends
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from database.database import engine, db_session
from util.hashing import get_hashed_password, verify_password
from sqlalchemy.orm import Session
import database.models as models
from flask_cors import CORS
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from util.config import *

app = Flask(__name__)
CORS(app)
# app.config.from_pyfile("settings.py")

# Mail configuration
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
app.config["MAIL_USE_SSL"] = MAIL_USE_SSL
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

mail = Mail(app)
BASE_URL = "http://localhost:5000"


def schedule_price_drop_alert():
    """
        Schedules price drop alerts for all registered users.

        This function queries all users from the database and sends a POST request 
        to the price-drop-alert API endpoint with the user's username as payload.
        The function is executed periodically using a scheduler.

        Raises:
            Exception: If an error occurs during the execution of the API call or database query.
    """

    try:
        users = db_session.query(models.Users).all()
        for user in users:
            payload = {"username": user.username}
            response = requests.post(f"{BASE_URL}/api/price-drop-alert", json=payload)
            print(response.text)
    except Exception as e:
        print(f"Error sending price drop alert: {e}")


# Scheduler for price drop alerts
scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_price_drop_alert, trigger="interval", seconds=180)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def index():
    """
        Default route to confirm the application and scheduler are running.

        Returns:
            str: A message indicating the scheduler is active.
    """

    return "Scheduler is running!"


@app.route("/postings/<username>", methods=["GET"])
def get_postings(username):
    """
        Retrieves product postings created by a specific user.

        This endpoint validates the given username, fetches the associated user 
        from the database, and retrieves all product postings made by the user.

        Args:
            username (str): The username of the user whose postings are being retrieved.

        Returns:
            JSON: A response containing either:
                - A success message with the list of postings.
                - An error message if the user does not exist.
    """

    validation1 = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    if validation1 is None:
        return jsonify(
            content={"status": "error", "message": f"User {username} does not exist"}
        )
    products = (
        db_session.query(models.ProductPostings)
        .filter(models.ProductPostings.posted_by == validation1.id)
        .all()
    )
    return jsonify(
        content={
            "status": "success",
            "data": [
                {
                    "name": product.name,
                    "date_posted": product.date_posted,
                    "description": product.description,
                    "price": product.price,
                    "currency": product.currency,
                    "sold": product.sold,
                    "posted_by": f"{validation1.first_name} {validation1.last_name}",
                }
                for product in products
            ],
        }
    )


def extract_price(price_str):
    """
        Extracts the numeric price from a given price string.

        Args:
            price_str (str): The string containing the price.

        Returns:
            float: The numeric price if found, otherwise None.
    """

    if not price_str[0].isdigit():
        prices = re.findall(r"\d+\.\d+", price_str)
        if prices:
            return float(prices[0])
        return None
    else:
        return float(price_str)


@app.route("/api/search", methods=["GET"])
def search_items_API():
    """
        API endpoint to search items across different platforms.

        Query Parameters:
            site (str): The site to search on ('walmart', 'ebay', 'bestbuy', 'target', or 'all').
            item_name (str): The name of the item to search for (required).
            min_price (float): Minimum price filter (default: 0).
            max_price (float): Maximum price filter (default: 10000).
            currency (str): Currency format (default: 'USD($)').

        Returns:
            Response: JSON response containing the filtered search results or error message.
    """

    site = request.args.get("site", "all")
    item_name = request.args.get("item_name")
    min_price = float(request.args.get("min_price", 0))
    max_price = float(request.args.get("max_price", 10000))
    currency = request.args.get("currency", "USD($)")

    if not item_name:
        return jsonify({"message": "Item name is required"}), 400

    # Scrapers based on the site
    scrapers = {
        "walmart": scrape_walmart,
        "ebay": scrape_ebay,
        "bestbuy": scrape_bestbuy,
        "target": scrape_target,
    }

    # Get the appropriate scraper or all
    if site in scrapers:
        scraper_funcs = [scrapers[site]]
    else:
        scraper_funcs = scrapers.values()

    results = []
    for scraper in scraper_funcs:
        try:
            results.extend(scraper(item_name))
        except Exception as e:
            print(f"Error scraping {site}: {e}")

    # Filter results based on price range
    # filtered_results = [item for item in results if min_price <= float(item['price'].replace('$', '').replace(',', '')) <= max_price]
    postings = get_product_postings(item_name.lower())
    results.extend(postings)

    try:
        filtered_results = [
            item
            for item in results
            if (price := extract_price(item["price"])) is not None
            and min_price <= price <= max_price
        ]
    except Exception as e:
        print(f"Error filtering results: {e}")
        return jsonify({"error": "Error filtering results"}), 500

    return jsonify(filtered_results)

def get_product_postings(item_name: str) -> list[dict[str]]:
    """
        Retrieves product postings from the database for the given item name.

        Args:
            item_name (str): The name of the item to search for.

        Returns:
            list[dict]: A list of dictionaries containing product details.
    """

    products = (
        db_session.query(models.ProductPostings)
        .filter(models.ProductPostings.name == item_name)
        .all()
    )
    data = list()

    for product in products:
        user = db_session.query(models.Users).filter(models.Users.id == product.posted_by).first()
        data.append(
            {
                "title": product.name,
                "price": str(product.price),
                "posted_by": f"{user.username}",
            }
        )

    return data

def scrape_walmart(item_name: str) -> list[dict]:
    """
        Scrapes Walmart's website for item details based on the search query.

        Args:
            item_name (str): The name of the item to search for.

        Returns:
            list[dict]: A list of dictionaries containing product details scraped from Walmart.
    """

    url = f"https://www.walmart.com/search/?q={item_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    if script_tag is not None:
        json_blob = json.loads(script_tag.get_text())
        product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"][
            "itemStacks"
        ][0]["items"]
        base_url = "https://www.walmart.com"

        for product in product_list:
            results.append(
                {
                    "title": product.get("name", "N/A"),
                    "price": product.get("priceInfo", {}).get("linePrice", "N/A"),
                    "link": base_url + product.get("canonicalUrl", ""),
                    "img_link": product.get("imageInfo", {}).get("thumbnailUrl", "N/A"),
                    "website": "Walmart",
                }
            )

    return results


def scrape_target(item_name):
    """Scrapes Target for item details."""
    url = f"https://www.target.com/s?searchTerm={item_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    products = soup.select(
        'div[data-test="product-grid"] section[class^="styles__StyledRowWrapper"] div[class^="styles__StyledCardWrapper"]'
    )
    for item in products:
        title = item.select_one(
            'div[data-test="product-details"] a[data-test="product-title"]'
        )
        price = item.select_one(
            'div[data-test="product-details"] span[data-test="current-price"]'
        )
        link = item.select_one(
            'div[data-test="product-details"] a[data-test="product-title"]'
        )

        if title and price and link:
            results.append(
                {
                    "title": title.text.strip(),
                    "price": price.text.strip(),
                    "link": "https://www.target.com" + link["href"],
                    "website": "Target",
                }
            )
    return results


def scrape_ebay(item_name):
    """
        Scrapes eBay for item details.

        Args:
            item_name (str): The name of the item to search for on eBay.

        Returns:
            list[dict]: A list of dictionaries, each containing details about an item,
                        such as title, price, link, image link, and the website.
    """

    url = f"https://www.ebay.com/sch/i.html?_nkw={item_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = []

    for item in soup.select(".s-item"):
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        link = item.select_one(".s-item__link")
        image_tag = item.select_one("img")
        if title and price and link:
            if title.get_text(strip=True) != "Shop on eBay":
                results.append(
                    {
                        "title": title.get_text(strip=True),
                        "price": price.get_text(strip=True),
                        "link": link["href"],
                        "img_link": image_tag["src"] if image_tag else None,
                        "website": "eBay",
                    }
                )
    return results


def scrape_bestbuy(item_name):
    """Scrapes Best Buy for item details."""
    url = f"https://www.bestbuy.com/site/searchpage.jsp?str={item_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = []

    for item in soup.select(".sku-item"):
        title = item.select_one("h4.sku-title a")
        price = item.select_one("div.priceView-customer-price span")
        link = item.select_one(".sku-header a")
        img_link = item.select_one("div.shop-sku-list-item div div a img")

        if title and price and link:
            results.append(
                {
                    "title": title.get_text(strip=True),
                    "price": price.get_text(strip=True),
                    "link": "https://www.bestbuy.com" + link["href"],
                    "img_link": img_link["src"] if img_link else None,
                    "website": "BestBuy",
                }
            )
    return results


@app.route("/api/wishlist", methods=["POST"])
def add_to_wishlist():
    """
        Adds an item to the user's wishlist.

        Expects a JSON payload containing:
            - item (dict): Item details including 'title', 'link', 'website', 'price', 'img_link'.
            - username (str): Username of the user.

        Returns:
            JSON response indicating success or failure.
    """

    item = request.json.get("item")
    username = request.json.get("username")
    existing_item = (
        db_session.query(models.PriceTrackProducts)
        .filter(models.PriceTrackProducts.product_url == item.get("link"))
        .first()
    )
    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    if not existing_item:
        existing_item = models.PriceTrackProducts(
            product_name=item.get("title"),
            product_url=item.get("link"),
            site=item.get("website"),
            price=float(re.sub(r"[^0-9.]", "", item.get("price")[1:])),
            currency=item.get("price"),
            img_url=item.get("img_link"),
        )
        db_session.add(existing_item)
        db_session.commit()

    wishlist_item = models.Wishlist(
        product_id=existing_item.id,
        user_id=user.id,
        product_type="online",
        date_added=datetime.now().strftime("%Y-%m-%d"),
    )
    db_session.add(wishlist_item)
    db_session.commit()
    return jsonify({"message": "Item added to wishlist successfully!"}), 200


@app.route("/api/wishlist/<product_id>", methods=["DELETE"])
def remove_from_wishlist(product_id):
    """
        Removes an item from the user's wishlist.

        Args:
            product_id (int): The ID of the wishlist item to be removed.

        Returns:
            JSON response indicating success or failure.
    """

    existing_item = (
        db_session.query(models.Wishlist)
        .filter(models.Wishlist.id == product_id)
        .first()
    )
    if not existing_item:
        return jsonify({"message": "Item not found in wishlist"}), 404

    db_session.delete(existing_item)
    db_session.commit()
    return jsonify({"message": "Item removed from wishlist successfully!"}), 200


@app.route("/api/wishlist/<username>", methods=["GET"])
def get_wishlist(username):
    """
        Fetches the user's wishlist.

        Args:
            username (str): The username of the user whose wishlist is to be retrieved.

        Returns:
            JSON response containing the list of wishlist items or an error message.
    """

    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    if not user:
        return jsonify({"message": "User not found"}), 404

    wishlist_objects = (
        db_session.query(models.Wishlist)
        .filter(models.Wishlist.user_id == user.id)
        .all()
    )
    wishlist = [
        {
            "id": w.id,
            "user_id": w.user_id,
            "title": product.product_name,
            "price": product.price,
            "link": product.product_url,
            "website": product.site,
            "img_link": product.img_url,
        }
        for w in wishlist_objects
        if (
            product := db_session.query(models.PriceTrackProducts)
            .filter(models.PriceTrackProducts.id == w.product_id)
            .first()
        )
    ]
    return jsonify(wishlist), 200


@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    """
        Adds an item to the user's cart.

        Expects a JSON payload containing:
            - item (dict): Item details including 'title', 'link', 'website', 'price', 'img_link'.
            - username (str): Username of the user.

        Returns:
            JSON response indicating success or failure.
    """

    item = request.json.get("item")
    username = request.json.get("username")
    existing_item = (
        db_session.query(models.PriceTrackProducts)
        .filter(models.PriceTrackProducts.product_url == item.get("link"))
        .first()
    )
    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    if not existing_item:
        existing_item = models.PriceTrackProducts(
            product_name=item.get("title"),
            product_url=item.get("link"),
            site=item.get("website"),
            price=float(re.sub(r"[^0-9.]", "", item.get("price")[1:])),
            currency=item.get("price"),
            img_url=item.get("img_link"),
        )
        db_session.add(existing_item)
        db_session.commit()

    cart_item = models.Cart(
        product_id=existing_item.id,
        user_id=user.id,
        product_type="online",
        date_added=datetime.now().strftime("%Y-%m-%d"),
    )
    db_session.add(cart_item)
    db_session.commit()
    return jsonify({"message": "Item added to cart successfully!"}), 200


@app.route("/api/cart/<product_id>", methods=["DELETE"])
def remove_from_cart(product_id):
    """
        Removes an item from the user's cart.

        Args:
            product_id (str): The ID of the product to remove from the cart.

        Returns:
            JSON response:
                - If the item is found and removed: {"message": "Item removed from cart successfully!"}, HTTP 200.
                - If the item is not found: {"message": "Item not found in cart"}, HTTP 404.
    """

    existing_item = (
        db_session.query(models.Cart).filter(models.Cart.id == product_id).first()
    )
    if not existing_item:
        return jsonify({"message": "Item not found in cart"}), 404

    db_session.delete(existing_item)
    db_session.commit()
    return jsonify({"message": "Item removed from cart successfully!"}), 200


@app.route("/api/cart/<username>", methods=["GET"])
def get_cart(username):
    """
        Fetches the items in a user's cart.

        Args:
            username (str): The username of the user whose cart is being retrieved.

        Returns:
            JSON response:
                - If the user exists: List of cart items, HTTP 200.
                - If the user does not exist: {"message": "User not found"}, HTTP 404.
    """

    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    if not user:
        return jsonify({"message": "User not found"}), 404

    cart_objects = (
        db_session.query(models.Cart).filter(models.Cart.user_id == user.id).all()
    )
    cart = [
        {
            "id": w.id,
            "user_id": w.user_id,
            "title": product.product_name,
            "price": product.price,
            "link": product.product_url,
            "website": product.site,
            "img_link": product.img_url,
        }
        for w in cart_objects
        if (
            product := db_session.query(models.PriceTrackProducts)
            .filter(models.PriceTrackProducts.id == w.product_id)
            .first()
        )
    ]
    return jsonify(cart), 200


@app.route("/api/place-order", methods=["POST"])
def place_order():
    """
        Places an order for the specified items in the user's cart.

        Request JSON:
            - items (list): List of items (dict) with product IDs to order.
            - username (str): The username of the user placing the order.

        Returns:
            JSON response:
                - {"message": "Order placed successfully!"}, HTTP 200.
    """

    items = request.json.get("items")
    username = request.json.get("username")

    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    order_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    for item in items:
        order = models.Order(
            product_id=item.get("id"),
            order_id=order_id,
            user_id=user.id,
            date_added=datetime.now().strftime("%Y-%m-%d"),
        )
        remove_from_cart(item.get("id"))
        db_session.add(order)
    db_session.commit()
    return jsonify({"message": "Order placed successfully!"}), 200


@app.route("/api/get-orders/<username>", methods=["GET"])
def get_order(username):
    """
        Retrieves all orders placed by a user.

        Args:
            username (str): The username of the user.

        Returns:
            JSON response:
                - If the user exists: List of order details, HTTP 200.
                - If the user does not exist: {"message": "User not found"}, HTTP 404.
    """

    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    orders = (
        db_session.query(models.Order).filter(models.Order.user_id == user.id).all()
    )
    orders = [
        {
            "id": o.id,
            "user_id": o.user_id,
            "order_id": o.order_id,
            "date": o.date_added,
            "title": product.product_name,
            "price": product.price,
            "link": product.product_url,
            "website": product.site,
            "img_link": product.img_url,
        }
        for o in orders
        if (
            product := db_session.query(models.PriceTrackProducts)
            .filter(models.PriceTrackProducts.id == o.product_id)
            .first()
        )
    ]
    return jsonify(orders), 200


@app.route("/add-posting", methods=["POST"])
def add_posting():
    """
        Adds a new product posting by a user.

        Request JSON:
            - username (str): The username of the user posting the product.
            - name (str): The name of the product.
            - description (str): The description of the product.
            - price (float): The price of the product.
            - currency (str): The currency of the price.
            - date_posted (str, optional): The date of posting (default: today).
            - sold (bool, optional): Whether the product is sold (default: False).

        Returns:
            JSON response:
                - If successful: {"status": "success"}.
                - If the user does not exist: {"status": "error", "message": "User {username} does not exist"}.
    """

    data = request.json
    username = data.get("username")
    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    if not user:
        return jsonify(
            content={"status": "error", "message": f"User {username} does not exist"}
        )

    new_product = models.ProductPostings(
        name=data.get("name").lower(),
        description=data.get("description"),
        price=data.get("price"),
        currency=data.get("currency"),
        date_posted=datetime.today().strftime("%Y-%m-%d"),
        posted_by=user.id,
        sold=False,
    )
    db_session.add(new_product)
    db_session.commit()

    return jsonify(content={"status": "success"})


def send_email(email, content):
    """
        Sends an email for price drop alerts.

        Args:
            email (str): The recipient's email address.
            content (str): The content of the email.

        Returns:
            str: A success or error message indicating the result of the email sending operation.

        Exceptions:
            Exception: Catches and returns any error encountered during the email sending process.
    """

    msg = Message("Price drop alert", recipients=[email])
    msg.body = content
    try:
        mail.send(msg)
        return f"Email sent to {email}!"
    except Exception as e:
        print(str(e))
        return str(e)


@app.route("/api/price-drop-alert", methods=["POST"])
def send_price_drop_alert():
    """
        Handles sending price drop alerts to users.

        Reads the username from the JSON payload, retrieves the user's wishlist, and checks if there are any price drops
        for the items being tracked. Sends an email notification to the user if applicable.

        Request JSON:
            - username (str): The username of the logged-in user.

        Returns:
            Response: A JSON response with a success message.

        Exceptions:
            Exception: Logs and propagates any issues in processing the alert.
    """

    username = request.json.get("username")
    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    # print("Hello user: ", user.id)
    existing_wishlist = (
        db_session.query(models.Wishlist)
        .filter(models.Wishlist.user_id == user.id)
        .first()
    )
    alert_items = []
    if existing_wishlist:
        linked_products = db_session.query(models.PriceTrackProducts).filter(
            models.PriceTrackProducts.id == existing_wishlist.product_id
        )
        for product in linked_products:
            # print("Product name: ",product.product_name)
            saved_price = product.price
            # print("Product price: ", saved_price)
            current_results = scrape_ebay(product.product_name)
            # print("Current res: ", current_results)
            for item in current_results:
                curr_price = extract_price(item.get("price"))
                if curr_price is not None:
                    if curr_price < saved_price:
                        # print("Current price: ",curr_price)
                        item["price"] = str(curr_price)
                        alert_items.append(item)

        print("total alert items: ", len(alert_items))

    send_email(user.email, alert_items)
    return jsonify({"message": "User alerted about price drop successfully! "}), 200


@app.route("/login", methods=["POST"])
def login():
    """
        Logs in a user by validating their credentials.

        Request JSON:
            - username (str): The username of the user.
            - password (str): The plaintext password of the user.

        Returns:
            Response: A JSON response containing the login status and user details if successful, 
                    or an error message if the login fails.

        Exceptions:
            Exception: Handles missing or incorrect credentials during the login process.
    """

    username = request.json.get("username")
    password = request.json.get("password")

    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    if not user:
        return jsonify(content={"status": "error", "message": "User does not exist"})

    if not verify_password(password, user.hashed_password):
        return jsonify(content={"status": "error", "message": "Invalid password"})

    return jsonify(
        content={
            "status": "success",
            "message": "User successfully logged in",
            "data": {
                "username": user.username,
                "email": user.email,
                "firstname": user.first_name,
                "lastname": user.last_name,
                "role": user.role
            },
        }
    )


@app.route("/register", methods=["POST"])
def register_user():
    """
        Registers a new user in the system.

        Request JSON:
            - username (str): The username for the new user.
            - email (str): The email address for the new user.
            - firstname (str): The first name of the user.
            - lastname (str): The last name of the user.
            - password (str): The plaintext password for the new user.
            - role (str): The role assigned to the user (e.g., admin, customer).

        Returns:
            Response: A JSON response indicating the success or failure of the registration, along with user details if successful.

        Exceptions:
            Exception: Handles duplicate username or email errors.
    """

    data = request.json
    username = data.get("username")
    email = data.get("email")
    firstname = data.get("firstName")
    lastname = data.get("lastName")
    password = data.get("password")
    role = data.get("role")

    print(role)

    if db_session.query(models.Users).filter(models.Users.username == username).first():
        return jsonify(content={"status": "error", "message": "Username already taken"})
    if db_session.query(models.Users).filter(models.Users.email == email).first():
        return jsonify(content={"status": "error", "message": "Email already taken"})

    user_model = models.Users(
        username=username,
        email=email,
        first_name=firstname,
        last_name=lastname,
        hashed_password=get_hashed_password(password),
        role=role,
    )
    db_session.add(user_model)
    db_session.commit()

    return jsonify(
        content={
            "status": "success",
            "message": "User successfully created",
            "data": {
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "role": role,
            },
        }
    )


models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)
