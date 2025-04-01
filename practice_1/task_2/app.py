from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    make_response,
    url_for,
)
import json

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html", products=PRODUCTS.values())


@app.get("/cart")
def cart():
    json_cart: str | None = request.cookies.get("cart")
    cart = json.loads(json_cart) if json_cart else {}

    cart_items = []
    total_sum = 0

    for product_id, quantity in cart.items():
        product = PRODUCTS.get(int(product_id))
        if product:
            total = float(product["price"]) * quantity
            cart_items.append(
                {
                    "id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity,
                    "total": round(total, 2),
                }
            )
            total_sum += total

    return render_template(
        "cart.html", cart_items=cart_items, total_sum=round(total_sum, 2)
    )


@app.post("/cart")
def add_product_to_cart():
    product_id = request.form.get("product_id", None)
    quantity = int(request.form.get("quantity", "1"))

    if product_id is None:
        return jsonify({"message": "Product not found"}), 404

    json_cart: str | None = request.cookies.get("cart")

    cart: dict[str, int] = json.loads(json_cart) if json_cart else {}
    cart[product_id] = cart.get(product_id, 0) + quantity

    json_cart = json.dumps(cart)

    res = make_response(redirect(url_for("home")))

    res.set_cookie("cart", json_cart, max_age=30 * 24 * 3600)

    return res


@app.post("/remove/<product_id>")
def remove_product_from_cart(product_id: str):

    json_cart: str | None = request.cookies.get("cart")
    cart: dict[str, int] = json.loads(json_cart) if json_cart else {}

    if product_id in cart:
        del cart[product_id]

    json_cart = json.dumps(cart)
    res = make_response(redirect(url_for("cart")))
    res.set_cookie("cart", json_cart, max_age=30 * 24 * 3600)

    return res


PRODUCTS = [
    {
        "id": 1,
        "price": "110.06",
        "name": "Tea - Herbal Orange Spice",
        "description": "Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque.\n\nQuisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus.\n\nPhasellus in felis. Donec semper sapien a libero. Nam dui.",
    },
    {
        "id": 2,
        "price": "76.48",
        "name": "Wine - Red, Metus Rose",
        "description": "Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat.\n\nCurabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.",
    },
    {
        "id": 3,
        "price": "109.09",
        "name": "Wine - White, Ej",
        "description": "Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.\n\nInteger tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.",
    },
    {
        "id": 4,
        "price": "76.85",
        "name": "Lemon Balm - Fresh",
        "description": "Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.\n\nCurabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla. Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam.",
    },
    {
        "id": 5,
        "price": "130.82",
        "name": "Dr. Pepper - 355ml",
        "description": "Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum.\n\nProin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.\n\nDuis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit.",
    },
    {
        "id": 6,
        "price": "43.16",
        "name": "Yoghurt Tubes",
        "description": "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.\n\nEtiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem.",
    },
    {
        "id": 7,
        "price": "20.34",
        "name": "Beef Flat Iron Steak",
        "description": "Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque.\n\nDuis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus.\n\nIn sagittis dui vel nisl. Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus.",
    },
    {
        "id": 8,
        "price": "58.82",
        "name": "Towel Multifold",
        "description": "Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.\n\nPraesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.\n\nMorbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem.",
    },
    {
        "id": 9,
        "price": "57.48",
        "name": "Appetizer - Assorted Box",
        "description": "Phasellus in felis. Donec semper sapien a libero. Nam dui.",
    },
    {
        "id": 10,
        "price": "145.73",
        "name": "Tea - Black Currant",
        "description": "Fusce consequat. Nulla nisl. Nunc nisl.\n\nDuis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum.",
    },
    {
        "id": 11,
        "price": "73.71",
        "name": "Island Oasis - Mango Daiquiri",
        "description": "In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.\n\nNulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.",
    },
    {
        "id": 12,
        "price": "88.95",
        "name": "Rosemary - Dry",
        "description": "In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.\n\nNulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.",
    },
    {
        "id": 13,
        "price": "130.27",
        "name": "Trout - Hot Smkd, Dbl Fillet",
        "description": "Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis.",
    },
    {
        "id": 14,
        "price": "16.38",
        "name": "Sauce - Soy Low Sodium - 3.87l",
        "description": "Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis.\n\nDuis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus.",
    },
    {
        "id": 15,
        "price": "19.70",
        "name": "Red Pepper Paste",
        "description": "In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.\n\nNulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.\n\nCras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque.",
    },
    {
        "id": 16,
        "price": "67.12",
        "name": "Puree - Pear",
        "description": "Fusce consequat. Nulla nisl. Nunc nisl.",
    },
    {
        "id": 17,
        "price": "56.75",
        "name": "Wine - Red, Cabernet Sauvignon",
        "description": "Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum.\n\nIn hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo.",
    },
    {
        "id": 18,
        "price": "136.44",
        "name": "Crackers - Graham",
        "description": "Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris.\n\nMorbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.\n\nFusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.",
    },
    {
        "id": 19,
        "price": "34.18",
        "name": "Sea Bass - Whole",
        "description": "Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis.\n\nDuis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus.",
    },
    {
        "id": 20,
        "price": "137.24",
        "name": "Milk - 1%",
        "description": "Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat.\n\nCurabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.\n\nInteger tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.",
    },
    {
        "id": 21,
        "price": "146.59",
        "name": "Tea - Apple Green Tea",
        "description": "In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.",
    },
    {
        "id": 22,
        "price": "54.88",
        "name": "Turkey - Ground. Lean",
        "description": "Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.",
    },
    {
        "id": 23,
        "price": "119.60",
        "name": "Mushroom - Enoki, Dry",
        "description": "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.\n\nEtiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem.",
    },
    {
        "id": 24,
        "price": "147.66",
        "name": "Boogies",
        "description": "Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.",
    },
    {
        "id": 25,
        "price": "105.88",
        "name": "Cheese - Mozzarella, Buffalo",
        "description": "In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.\n\nNulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.\n\nCras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque.",
    },
    {
        "id": 26,
        "price": "125.55",
        "name": "Cheese - Parmigiano Reggiano",
        "description": "Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.\n\nDuis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit.\n\nDonec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque.",
    },
    {
        "id": 27,
        "price": "134.41",
        "name": "Beer - Moosehead",
        "description": "Fusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.",
    },
    {
        "id": 28,
        "price": "88.53",
        "name": "Table Cloth 90x90 White",
        "description": "In congue. Etiam justo. Etiam pretium iaculis justo.",
    },
    {
        "id": 29,
        "price": "149.99",
        "name": "Compound - Mocha",
        "description": "Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.",
    },
    {
        "id": 30,
        "price": "61.05",
        "name": "Towels - Paper / Kraft",
        "description": "Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus.\n\nPellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus.",
    },
    {
        "id": 31,
        "price": "135.93",
        "name": "Rice - Jasmine Sented",
        "description": "Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.\n\nFusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.",
    },
    {
        "id": 32,
        "price": "145.31",
        "name": "Wine - Ej Gallo Sierra Valley",
        "description": "Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.",
    },
    {
        "id": 33,
        "price": "56.02",
        "name": "Mushroom - White Button",
        "description": "Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus.\n\nPellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus.",
    },
    {
        "id": 34,
        "price": "64.44",
        "name": "Soup - Knorr, French Onion",
        "description": "Fusce consequat. Nulla nisl. Nunc nisl.\n\nDuis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum.",
    },
    {
        "id": 35,
        "price": "100.21",
        "name": "Wine - Vidal Icewine Magnotta",
        "description": "Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum.\n\nIn hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo.",
    },
    {
        "id": 36,
        "price": "144.38",
        "name": "Juice - Cranberry 284ml",
        "description": "Sed ante. Vivamus tortor. Duis mattis egestas metus.",
    },
    {
        "id": 37,
        "price": "77.71",
        "name": "Mcgillicuddy Vanilla Schnap",
        "description": "Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.\n\nInteger tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.\n\nPraesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.",
    },
    {
        "id": 38,
        "price": "86.86",
        "name": "Container - Hngd Cll Blk 7x7x3",
        "description": "Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.",
    },
    {
        "id": 39,
        "price": "142.27",
        "name": "Wine - Lamancha Do Crianza",
        "description": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin risus. Praesent lectus.",
    },
    {
        "id": 40,
        "price": "30.12",
        "name": "Soup - Knorr, Chicken Noodle",
        "description": "Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque.\n\nQuisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus.\n\nPhasellus in felis. Donec semper sapien a libero. Nam dui.",
    },
    {
        "id": 41,
        "price": "30.97",
        "name": "Longos - Lasagna Beef",
        "description": "Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero.",
    },
    {
        "id": 42,
        "price": "34.44",
        "name": "Smirnoff Green Apple Twist",
        "description": "Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.\n\nAenean lectus. Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum.",
    },
    {
        "id": 43,
        "price": "70.40",
        "name": "Cocoa Powder - Natural",
        "description": "Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius.\n\nInteger ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.\n\nNam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.",
    },
    {
        "id": 44,
        "price": "142.10",
        "name": "Wine La Vielle Ferme Cote Du",
        "description": "In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.",
    },
    {
        "id": 45,
        "price": "74.95",
        "name": "Cheese Cheddar Processed",
        "description": "Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.\n\nQuisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.\n\nVestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat.",
    },
    {
        "id": 46,
        "price": "79.83",
        "name": "Milk 2% 500 Ml",
        "description": "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.\n\nEtiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem.\n\nPraesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.",
    },
    {
        "id": 47,
        "price": "51.68",
        "name": "Contreau",
        "description": "Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis.\n\nDuis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus.",
    },
    {
        "id": 48,
        "price": "125.31",
        "name": "Veal - Provimi Inside",
        "description": "Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius.",
    },
    {
        "id": 49,
        "price": "143.53",
        "name": "Lobster - Base",
        "description": "Sed ante. Vivamus tortor. Duis mattis egestas metus.",
    },
    {
        "id": 50,
        "price": "148.58",
        "name": "Vermouth - Sweet, Cinzano",
        "description": "Sed ante. Vivamus tortor. Duis mattis egestas metus.\n\nAenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.",
    },
]

PRODUCTS = {product["id"]: product for product in PRODUCTS}
