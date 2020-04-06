import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from company_order import CompanyOrder
from company_info import CompanyInfo
import datetime
from pykafka import KafkaClient
import pykafka
import yaml as yaml
import json
from threading import Thread
from flask_cors import CORS, cross_origin
import logging.config

DB_ENGINE = create_engine('sqlite:///readings.sqlite')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def companyInfo(reading):
    session = DB_SESSION()

    ci = CompanyInfo(reading['company_name'],
                       reading['order_date'],
                       reading['order_date_complete'])

    session.add(ci)
    session.commit()
    session.close()
    return NoContent, 200

def companyOrder(reading):
    session = DB_SESSION()

    co = CompanyOrder(reading['company_name'],
                       reading['material'],
                       reading['quantity'],
                       reading['price'],
                       reading['status'])

    session.add(co)
    session.commit()
    session.close()
    return 200

def get_company_information(startDate, endDate):
    results_list = []

    session = DB_SESSION()

    results = session.query(CompanyInfo).all()
    
    for result in results:
        datetime1 = datetime.datetime.strptime(startDate, '%Y-%m-%d:%H:%M:%S')
        datetime2 = datetime.datetime.strptime(endDate, '%Y-%m-%d:%H:%M:%S')
        print(result.to_dict())
        if datetime1 <= result.to_dict()['date_created'] <= datetime2:
            results_list.append(result.to_dict())
            print(result.to_dict())

    session.close()

    return results_list, 200

def get_company_order(startDate, endDate):
    results_list = []

    session = DB_SESSION()

    results = session.query(CompanyOrder).all()

    for result in results:
        datetime1 = datetime.datetime.strptime(startDate, '%Y-%m-%d:%H:%M:%S')
        datetime2 = datetime.datetime.strptime(endDate, '%Y-%m-%d:%H:%M:%S')
        print(result.to_dict())
        if datetime1 <= result.to_dict()['date_created'] <= datetime2:
            results_list.append(result.to_dict())
            print(result.to_dict())

    session.close()

    return results_list, 200

def process_messages():
    with open ('kafka_config.yaml', 'r') as f:
        kafka = yaml.safe_load(f.read())

    client = KafkaClient(hosts='{0}:{1}'.format(kafka['kafka']['kafka-server'], kafka['kafka']['kafka-port']))
    topic = client.topics['{0}'.format(kafka['kafka']['topic'])]
    consumer = topic.get_simple_consumer()

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'Info':
            reading = msg['payload']
            companyInfo(reading)
        elif msg['type'] == 'Order':
            reading = msg['payload']
            companyOrder(reading)

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)