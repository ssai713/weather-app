import datetime
import logging
import os
from pathlib import Path

logging.basicConfig(filename="../answers/record.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)



def read_wx_data(data_folder):
    from .app import WeatherRecord
    logger.info("Reading weather data...")
    weather = []
    data_folder_path = Path(data_folder)
    for file_path in data_folder_path.glob("*.txt"):
        logger.info("Reading file: %s", file_path)
        print("Reading file: %s", file_path)
        try:
            with file_path.open("r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    temp = line.split("\t")
                    w = WeatherRecord(
                        station=file_path.stem,
                        date=int(temp[0]),
                        maximum_temperature=int(temp[1]),
                        minimum_temperature=int(temp[2]),
                        precipitation=int(temp[3]),
                    )
                    weather.append(w)
        except Exception as e:
            logger.error("Error reading file %s: %s", file_path, e)
            continue
    logger.info("Weather data read complete: found %d records", len(weather))
    return weather


def ingest_wx_data(data_folder):
    from .app import db
    initial_time = datetime.datetime.now()

    weather = read_wx_data(data_folder)
    s = db.session
    logger.info("Inserting weather data into database...")
    print("data_ingesting")
    try:
        s.bulk_save_objects(weather)
        s.commit()
        logger.info("Weather data loaded.")
        completion_time = datetime.datetime.now()
        logger.info(
            f"Weather data inserted in {(completion_time - initial_time).total_seconds()} seconds. Total rows: {len(weather)}"
        )
    except Exception as e:
        s.rollback()
        logger.error("Error inserting weather data into database: %s", e)
    finally:
        s.close()


def generate_statistics():
    from .app import db
    query = """
            INSERT INTO statistic(station, date, final_maximum_temperature, final_minimum_temperature, final_precipitation)
            SELECT station, date, avg(maximum_temperature), avg(minimum_temperature), sum(precipitation)
            FROM (
                SELECT *
                FROM weather_record
                WHERE maximum_temperature != -9999
                AND minimum_temperature != -9999
                AND precipitation != -9999
            )
            GROUP BY station, substring(date, 1, 4)
            """
    s = db.session
    logger.info("Generating weather statistics...")
    try:
        s.execute(query)
        s.commit()
        logger.info("Statistics data loaded.")
    except Exception as e:
        s.rollback()
        logger.error("Error generating weather statistics: %s", e)
    finally:
        s.close()
