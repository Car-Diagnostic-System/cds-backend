from .database import db

class Product(db.Model):
    __tablename__ = 'product'
    serial_no = db.Column(db.String(255), primary_key=True)
    supplier_no = db.Column(db.String(255), nullable=False)
    oem_no = db.Column(db.String(255), nullable=False)
    benchmark_no = db.Column(db.String(255), nullable=True)
    car_brand = db.Column(db.String(255), nullable=True)
    car_model = db.Column(db.String(255), nullable=True)
    model_name_th = db.Column(db.String(255), nullable=True)
    nickname = db.Column(db.String(255), nullable=True)
    item_name = db.Column(db.String(255), nullable=False)
    fitment_detail = db.Column(db.String(255), nullable=True)
    brand = db.Column(db.String(255), nullable=False)
    item_group = db.Column(db.String(255), nullable=True)
    stock_uom = db.Column(db.String(255), nullable=False)

    def __init__(self, serial_no, supplier_no, oem_no, benchmark_no, car_brand, car_model, model_name_th, nickname, item_name, fitment_detail, brand, item_group, stock_uom):
        self.serial_no = serial_no
        self.supplier_no = supplier_no
        self.oem_no = oem_no
        self.benchmark_no = benchmark_no
        self.car_brand = car_brand
        self.car_model = car_model
        self.model_name_th = model_name_th
        self.nickname = nickname
        self.item_name = item_name
        self.fitment_detail = fitment_detail
        self.brand = brand
        self.item_group = item_group
        self.stock_uom = stock_uom

    @property
    def serialize(self):
        return {
            'serial_no': self.serial_no,
            'supplier_no': self.supplier_no,
            'oem_no': self.oem_no,
            'benchmark_no': self.benchmark_no,
            'car_brand': self.car_brand,
            'car_model': self.car_model,
            'model_name_th': self.model_name_th,
            'nickname': self.nickname,
            'item_name': self.item_name,
            'fitment_detail': self.fitment_detail,
            'brand': self.brand,
            'item_group': self.item_group,
            'stock_uom': self.stock_uom,
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]