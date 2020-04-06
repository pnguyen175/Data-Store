from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class CompanyOrder(Base):
    """ Company Order """

    __tablename__ = "company_order"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(250), nullable=False)
    material = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, company_name, material, quantity, price, status):
        """ Initialzes a company order """
        self.company_name = company_name
        self.material = material
        self.quantity = quantity
        self.price = price
        self.status = status
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a company order """
        dict = {}
        dict['id'] = self.id
        dict['company_name'] = self.company_name
        dict['material'] = self.material
        dict['quantity'] = self.quantity
        dict['price'] = self.price
        dict['status'] = self.status
        dict['date_created'] = self.date_created
        
        return dict