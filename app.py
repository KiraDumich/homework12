from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import raw_data
import json


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# создаём базу данных
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) # ключ базы данных
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))

    # метод, преобразующий поля в словарь

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
        }

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)  # ключ базы данных
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    start_date = db.Column(db.String(100))
    end_date =  db.Column(db.String(100))

    address = db.Column(db.String(100))
    price = db.Column(db.Integer)


    customer_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))

    # метод, преобразующий поля в словарь

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }

class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{Order.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
      result = []
      for u in User.query.all():
          result.append(u.to_dict())

      return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

    if request.method == "POST":
        user_data = json.loads(request.data)

        db.session.add(
            User(
                id=user_data.get("id"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                age=user_data.get("age"),
                email=user_data.get("email"),
                role=user_data.get("role"),
                phone_number=user_data.get("phone"),
            )
        )
        db.session.commit()

        return "", 201


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):
    if request.method == "GET":
      return json.dumps(User.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    if request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)

        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "", 201

    if request.method == "DELETE":
        u = User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "", 204


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
      result = []
      for u in Order.query.all():
          result.append(u.to_dict())

      return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

    if request.method == "POST":
        order_data = json.loads(request.data)

        db.session.add(
            Order(
                id=order_data.get("id"),
                name=order_data.get("name"),
                description=order_data.get("description"),
                start_date=order_data.get("start_date"),
                end_date=order_data.get("end_date"),
                address=order_data.get("address"),
                price=order_data.get("price"),
                customer_id=order_data.get("customer_id"),
                executor_id=order_data.get("executor_id"),
            )
        )
        db.session.commit()

        return "", 201


@app.route("/orders/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid: int):
     if request.method == "GET":
        return json.dumps(Order.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}

     if request.method == "PUT":
         order_data = json.loads(request.data)
         u = Order.query.get(uid)

         u.name = order_data["name"]
         u.description = order_data["description"]
         u.start_date = order_data["start_date"]
         u.end_date = order_data["end_date"]
         u.address = order_data["address"]
         u.price = order_data["price"]
         u.customer_id = order_data["customer_id"]
         u.executor_id = order_data["executor_id"]

         db.session.add(u)
         db.session.commit()

         return "", 201


     if request.method == "DELETE":
        u = Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "", 204


@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
      result = []
      for u in Offer.query.all():
          result.append(u.to_dict())

      return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

    if request.method == "POST":
        offer_data = json.loads(request.data)

        db.session.add(
            Offer(
                id=offer_data.get("id"),
                order_id=offer_data.get("order_id"),
                executor_id=offer_data.get("description"),
            )
        )
        db.session.commit()


@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid: int):
    if request.method == "GET":
      return json.dumps(Offer.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)

        u.order_id = offer_data["order_id"]
        u.executor_idv= offer_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "", 201

    if request.method == "DELETE":
       u = Offer.query.get(uid)

       db.session.delete(u)
       db.session.commit()

       return "", 204


# кладём данные из файла с помощью моделей
def init_database():
    db.drop_all()
    db.create_all()

    for user_data in raw_data.users:
       db.session.add(
          User(
            id=user_data.get("id"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            age=user_data.get("age"),
            email=user_data.get("email"),
            role=user_data.get("role"),
            phone_number=user_data.get("phone"),
          )
       )
       db.session.commit()

    for order_data in raw_data.orders:
       db.session.add(
          Order(
            id=order_data.get("id"),
            name=order_data.get("name"),
            description=order_data.get("description"),
            start_date=order_data.get("start_date"),
            end_date=order_data.get("end_date"),
            address=order_data.get("address"),
            price=order_data.get("price"),
            customer_id=order_data.get("customer_id"),
            executor_id=order_data.get("executor_id"),
          )
       )
       db.session.commit()

    for offer_data in raw_data.offers:
       db.session.add(
          Offer(
            id=offer_data.get("id"),
            order_id=offer_data.get("order_id"),
            executor_id=offer_data.get("description"),
          )
       )
       db.session.commit()


if __name__ == '__main__':
    init_database()
    app.run(debug=True)