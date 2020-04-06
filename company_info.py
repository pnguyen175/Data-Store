from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class CompanyInfo(Base):
    """ Company Information """

    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(250), nullable=False)
    order_date = Column(String(250), nullable=False)
    order_date_complete = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, company_name, order_date, order_date_complete):
        """ Initializes a company information """
        self.company_name = company_name
        self.order_date = order_date
        self.order_date_complete = order_date_complete
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a company information """
        dict = {}
        dict['id'] = self.id
        dict['company_name'] = self.company_name
        dict['order_date'] = self.order_date
        dict['order_date_complete'] = self.order_date_complete
        dict['date_created'] = self.date_created
        
        return dict