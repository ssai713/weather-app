import click
from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import os
try:
    from .ingest import (
        generate_statistics,
        ingest_wx_data,
    )
except Exception:
    from ingest import (
        generate_statistics,
        ingest_wx_data,
    )



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example2.sqlite"


# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)



db = SQLAlchemy(app)


class Statistic(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(15))
    date = db.Column(db.String(8))
    final_maximum_temperature = db.Column(db.Integer)
    final_minimum_temperature = db.Column(db.Integer)
    final_precipitation = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            "station": self.station,
            "date": self.date,
            "final_maximum_temperature": self.final_maximum_temperature,
            "final_minimum_temperature": self.final_minimum_temperature,
            "final_precipitation": self.final_precipitation,
        }


class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(15))
    date = db.Column(db.String(8))
    maximum_temperature = db.Column(db.Integer)
    minimum_temperature = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            "station": self.station,
            "date": self.date,
            "maximum_temperature": self.maximum_temperature,
            "minimum_temperature": self.minimum_temperature,
            "precipitation": self.precipitation,
        }


@click.command(name="create")
def create():
    with app.app_context():
        db.drop_all()
        db.create_all()
        ingest_wx_data(f"../wx_data")
        generate_statistics()


@app.route("/api/weather/", methods=["GET"])
def weather_home():
    page = request.args.get("page", type=int)
    date = request.args.get("date")
    station = request.args.get("station")
    result = WeatherRecord.query
    if date:
        result = result.filter(WeatherRecord.date == date)
    if station:
        result = result.filter(WeatherRecord.station == station)
    result = result.paginate(page=page, per_page=100).items
    return jsonify([r.serialize for r in result])




@app.route("/api/weather/stats/", methods=["GET"])
def stats():
    page = request.args.get("page", type=int)
    date = request.args.get("date")
    station = request.args.get("station")
    query = Statistic.query
    if date:
        query = query.filter(Statistic.date == date)
    if station:
        query = query.filter(Statistic.station == station)
    result = query.paginate(page=page, per_page=100).items
    return jsonify([r.serialize for r in result])

if __name__ == "__main__":
    app.run(debug=True)

app.cli.add_command(create)
