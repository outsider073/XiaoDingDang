import flask_sqlalchemy

from . import db

assert isinstance(db, flask_sqlalchemy.SQLAlchemy)


class Corporation(db.Model):
    # 公司客户基本信息
    __tablename__ = 'corporation'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=True)  # 企业名称
    account = db.Column(db.String(25), unique=True)  # 企业帐号
    customer_number = db.Column(db.Integer, unique=True)  # 公司客户号
    license_number = db.Column(db.String(20), unique=True)  # 企业营业执照号
    credit_number = db.Column(db.String(20), unique=True)  # 企业社会信用代码证
    seal = db.Column(db.String(80), unique=True)  # 企业公章存放地址
    description = db.Column(db.Text)  # 企业描述
    address = db.Column(db.String(80))  # 企业地址
    phone = db.Column(db.String(20))  # 企业电话
    # credit_id = db.Column(db.Integer, db.ForeignKey('credit.id'))
    legal_relative = db.relationship('Person', backref='corporation', uselist=True, lazy='dynamic')  # 企业法人
    pictures = db.relationship('Picture', backref='corporation', lazy='dynamic')  # 企业证件扫描件
    credit = db.relationship('Credit', backref='corporation', uselist=True, lazy='dynamic')  # 企业授信

    def __init__(self, name, account, customer_number, license_number, credit_number, seal, address, phone,
                 description):
        # self.id = id
        self.name = name
        self.account = account
        self.customer_number = customer_number
        self.license_number = license_number
        self.credit_number = credit_number
        self.seal = seal
        self.description = description
        self.address = address
        self.phone = phone

    def __repr__(self):
        return "企业:" + self.name


class Picture(db.Model):
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80))  # 档案名称
    path = db.Column(db.String(80), unique=True)  # 档案路径
    date = db.Column(db.DateTime)  # 档案上传时间
    updated = db.Column(db.Boolean)  # 档案是否为最新
    description = db.Column(db.String(80))  # 档案描述
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __init__(self, name, path, date, updated):
        # self.id = id
        self.name = name
        self.path = path
        self.date = date
        self.updated = updated

    def __repr__(self):
        return "图像：" + self.name


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(20))  # 自然人姓名
    id_number = db.Column(db.String(20))  # 自然人身份证号
    mate_id = db.Column(db.Integer, db.ForeignKey('person.id'))  # 自然人配偶
    pictures = db.relationship('Picture', backref='')  # 自然人档案扫描件
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))

    def __init__(self, name, id_number, mate_id=None):
        self.name = name
        self.id_number = id_number
        self.mate_id = mate_id

    def __repr__(self):
        return "姓名:" + self.name


class Credit(db.Model):
    __tablename__ = 'credit'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    credit_limit = db.Column(db.Integer)  # 授信额度
    credit_limit_available = db.Column(db.Integer)  # 可用授信额度
    start_time = db.Column(db.Date)  # 授信启用日期
    end_time = db.Column(db.Date)  # 授信终止日期
    credit_reply = db.Column(db.Text)  # 批复
    customer_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))

    # customer = db.relationship('Corporation', backref='credit', lazy='dynamic', uselist=True)
    land_mortage = db.relationship('LandMortage', backref='credit', lazy='dynamic')  # 土地抵押
    estimate_mortage = db.relationship('EstimateMortage', backref='credit', lazy='dynamic')  # 房产抵押
    person_guarantee = db.relationship('PersonGuarantee', backref='credit', lazy='dynamic')  # 自然人担保
    corportion_guarantee = db.relationship('CorporationGuarantee', backref='credit', lazy='dynamic')  # 企业担保

    def __init__(self, credit_limit, credit_limit_available, start_time, end_time, credit_reply):
        self.credit_limit = credit_limit
        self.credit_limit_available = credit_limit_available
        self.start_time = start_time
        self.end_time = end_time
        self.credit_reply = credit_reply

    def __repr__(self):
        c = Corporation.query.get(self.id)
        return c.name + ":" + str(self.credit_limit)


class LandMortage(db.Model):
    __tablename__ = 'landmortage'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    corporation = db.relationship('Corporation', backref='landmortage')  # 抵押企业
    credit_id = db.Column(db.Integer, db.ForeignKey('credit.id'))
    warrants = db.relationship('LandWarrant', backref='landmortage', lazy='dynamic')  # 他项权证
    start_time = db.Column(db.Date)  # 抵押开始时间
    end_time = db.Column(db.Date)  # 抵押终止时间


class LandWarrant(db.Model):
    __tablename__='landwarrant'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    landmortage_id = db.Column(db.Integer, db.ForeignKey('landmortage.id'))
    lands = db.relationship('Land', backref='landwarrant', lazy='dynamic') #土地证
    owner = db.Column(db.String(80)) #他项权证抵押人
    area = db.Column(db.Float) #抵押面积
    certificate_number = db.Column(db.String(80), unique=True) #他证号
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))
    picture = db.relationship('Picture', backref='landwarrant', uselist=False)

    def __init__(self, certificate_number):
        self.certificate_number = certificate_number


class Land(db.Model):
    __tablename__ = 'land'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    landwarrant_id = db.Column(db.Integer, db.ForeignKey('landwarrant.id'))
    land_certificate_number = db.Column(db.String(80), unique=True)  # 土地证

    area = db.Column(db.Float)  # 使用权面积
    area_available = db.Column(db.Float)  # 独用面积
    owner = db.Column(db.String(80))  # 使用权人
    address = db.Column(db.String(80))  # 坐落
    land_code = db.Column(db.String(20))  # 地号
    start_date = db.Column(db.Date)  # 注册时间
    end_date = db.Column(db.Date)  # 终止时间
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))
    picture = db.relationship('Picture', backref='land', uselist=False)

    def __init__(self, land_certificate_number):
        self.land_certificate_number = land_certificate_number


class EstimateMortage(db.Model):
    __tablename__='estimatemortage'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    corporation = db.relationship('Corporation', backref='estimatemortage')  # 抵押企业
    credit_id = db.Column(db.Integer, db.ForeignKey('credit.id'))
    warrants = db.relationship('EstimateWarrant', backref='estimatemortage', lazy='dynamic')
    start_time = db.Column(db.Date) # 抵押起始时间
    end_time = db.Column(db.Date) # 抵押终止时间

    def __init__(self, corporation):
        self.corporation = corporation

class EstimateWarrant(db.Model):
    __tablename__='estimatewarrant'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    estimatemortage_id = db.Column(db.Integer, db.ForeignKey('estimatemortage.id'))
    estimates = db.relationship('Estimate', backref='estimatewarrant', lazy='dynamic')  # 房产证
    owner = db.Column(db.String(80))  # 他项权证抵押人
    area = db.Column(db.Float)  # 抵押面积
    certificate_number = db.Column(db.String(80), unique=True)  # 他证号
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))
    picture = db.relationship('Picture', backref='estimatewarrant', uselist=False)

    def __init__(self, certificate_number):
        self.certificate_number = certificate_number

class Estimate(db.Model):
    __tablename__ = 'estimate'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    estimatewarrant_id = db.Column(db.Integer, db.ForeignKey('estimatewarrant.id'))
    owner = db.Column(db.String(80))
    area = db.Column(db.Float)
    certificate_number = db.Column(db.String(80), unique=True)
    area_available = db.Column(db.Float)
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))
    picture = db.relationship('Picture', backref='estimate', uselist=False)

## 流程

class Task(db.Model):
    pass