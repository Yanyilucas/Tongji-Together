import os
import uuid
from datetime import datetime
from datetime import timedelta
import math
from flask import Flask, send_from_directory
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import decode_token, exceptions as jwt_exc

db = SQLAlchemy()
app = Flask(__name__, static_url_path='')
# 在应用启动时自动迁移
app.secret_key = '2251316#TJTX'
app.config['JWT_SECRET_KEY'] = '2251316#TJTX'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TJTX.db"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['PROPAGATE_EXCEPTIONS'] = True
# 配置上传文件夹
UPLOAD_FOLDER = os.path.join(app.root_path, 'static')
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传大小为16MB
# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# 允许跨域
CORS(app, supports_credentials=True)
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager()
jwt.init_app(app)
bcrypt = Bcrypt()

"""
用户模型
"""
class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Password = db.Column(db.String(127), nullable=False)
    Name = db.Column(db.String(127), nullable=False)
    Tel = db.Column(db.String(15), nullable=False, unique=True)
    isDriver = db.Column(db.Boolean, default=False) # 是否为司机 / 是否为乘客
    
    def serialize(self):
        return {
            'UserID': self.UserID,
            'Name': self.Name,
            'Tel': self.Tel,
            'isDriver': self.isDriver
        }
        
    def set_password(self, password):
        """设置用户密码"""
        self.Password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """检查用户密码"""
        return bcrypt.check_password_hash(self.Password, password)

    def __repr__(self):
        return f"<User(UserID={self.UserID}, Name={self.Name}, Tel={self.Tel}, isDriver={self.isDriver})>"

class DriverPosting(db.Model):
    __tablename__ = 'DriverPostings'
    PostingID = db.Column(db.Integer     , primary_key=True, autoincrement=True)
    DrviverID = db.Column(db.Integer     , db.ForeignKey('Users.UserID'), nullable=False)
    From = db.Column(db.String(255)      , nullable=False)  # 出发地
    To = db.Column(db.String(255)        , nullable=False)  # 目的地
    
    FromLat = db.Column(db.Float, nullable=False)  # 出发地纬度
    FromLng = db.Column(db.Float, nullable=False)  # 出发地经度
    ToLat = db.Column(db.Float, nullable=False)    # 目的地纬度
    ToLng = db.Column(db.Float, nullable=False)    # 目的地经度
    CreatedAt = db.Column(db.DateTime, server_default=db.func.now())  # 创建时间
    
    PlateNumber = db.Column(db.String(20), nullable=False)  # 车牌号
    DepartureTime = db.Column(db.DateTime, nullable=False)  # 出发时间
    SeatsAvailable = db.Column(db.Integer, nullable=False)  # 可用座位数
    Fare = db.Column(db.Float, nullable=False)  # 费用
    Note = db.Column(db.String(255), nullable=True)  # 附加说明
    driver = db.relationship('User', backref='driver_postings')

    
    def serialize(self):
        return {
            'PostingID': self.PostingID,
            'DrviverID': self.DrviverID,
            'From': self.From,
            'To': self.To,
            'FromLat': self.FromLat,
            'FromLng': self.FromLng,
            'ToLat': self.ToLat,
            'ToLng': self.ToLng,
            'CreatedAt': self.CreatedAt.isoformat(),
            'PlateNumber': self.PlateNumber,
            'DepartureTime': self.DepartureTime.isoformat(),
            'SeatsAvailable': self.SeatsAvailable,
            'Fare': self.Fare,
            'Note': self.Note
        }
class RideJoin(db.Model):
    __tablename__ = 'RideJoins'
    JoinID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    PostingID = db.Column(db.Integer, db.ForeignKey('DriverPostings.PostingID'), nullable=False)
    CreatedAt = db.Column(db.DateTime, server_default=db.func.now())  # 创建时间
    user = db.relationship('User', backref='ride_joins')
    posting = db.relationship('DriverPosting', backref='ride_joins')

    def serialize(self):
        return {
            'JoinID': self.JoinID,
            'UserID': self.UserID,
            'PostingID': self.PostingID,
            'CreatedAt': self.CreatedAt.isoformat()
        }
        
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
	# 提取并验证数据
    tel = data.get('Tel', '').strip().lower()
    password = data.get('password', '').strip()
    if not tel:
        return jsonify({'error': 'tel is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    existing_user = User.query.filter_by(Tel=tel).first()
    if not existing_user:
        return jsonify({'error': '未注册的手机号'}), 400
	# 验证密码
    if not existing_user.check_password(password):
        return jsonify({'error': '密码错误'}), 401
	# 生成 JWT token
    token = create_access_token(identity=str(existing_user.UserID))
    
    return jsonify({'message': '登录成功', 'token': token}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # 提取并初步校验
    name          = (data.get('name') or '').strip()
    tel           = (data.get('tel') or '').strip().lower()
    password      = (data.get('password') or '').strip()
    confirm       = (data.get('confirmPassword') or '').strip()
    is_driver     = bool(data.get('isDriver', False))

    if not name:
        return jsonify({'error': '用户名不能为空'}), 400
    if not tel:
        return jsonify({'error': '手机号不能为空'}), 400
    if not password:
        return jsonify({'error': '密码不能为空'}), 400
    if password != confirm:
        return jsonify({'error': '两次输入的密码不一致'}), 400

    # 手机号唯一性检查
    if User.query.filter_by(Tel=tel).first():
        return jsonify({'error': '该手机号已注册'}), 400

    # 创建并保存用户
    user = User(Name=name, Tel=tel, isDriver=is_driver)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # 返回 JWT + 成功信息
    return jsonify({'message': '注册成功'}), 201

@app.route('/userinfo', methods=['GET'])
@jwt_required()
def get_user_info():
    identity = get_jwt_identity()
    print(f"🔑 Token 校验成功，用户 ID: {identity}")
    user_id =int(identity)

    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(user.serialize()), 200

@app.route('/register_driver', methods=['POST'])
@jwt_required()
def apply_driver():
    identity = get_jwt_identity()
    user_id = int(identity)

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    if user.isDriver:
        return jsonify({'error': '您已经是车主'}), 400

    user.isDriver = True
    db.session.commit()
    return jsonify({'message': '申请成功'}), 200

@app.route('/unregister_driver', methods=['POST'])
@jwt_required()
def cancel_driver():
    identity = get_jwt_identity()
    user_id = int(identity)

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    if not user.isDriver:
        return jsonify({'error': '您不是车主'}), 400

    user.isDriver = False
    db.session.commit()
    return jsonify({'message': '注销车主成功'}), 200


@app.route('/post_driver_posting', methods=['POST'])
@jwt_required()
def create_driver_posting():
    identity = get_jwt_identity()
    user_id = int(identity)

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    if not user.isDriver:
        return jsonify({'error': '您不是车主'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # ----------------- 提取并验证数据 -----------------
    required_fields = [
        'From', 'To',
        'FromLat', 'FromLng',
        'ToLat', 'ToLng',
        'DepartureTime',
        'SeatsAvailable',
        'Fare',
        'PlateNumber'
    ]
    missing = [f for f in required_fields if f not in data or data[f] in (None, '')]
    if missing:
        return jsonify({'error': f"缺少必要字段: {', '.join(missing)}"}), 400

    # 字段预处理 & 类型转换
    try:
        posting_kwargs = {
            'DrviverID': user_id,
            'From':        str(data['From']).strip(),
            'To':          str(data['To']).strip(),
            'FromLat':     float(data['FromLat']),
            'FromLng':     float(data['FromLng']),
            'ToLat':       float(data['ToLat']),
            'ToLng':       float(data['ToLng']),
            'PlateNumber': str(data['PlateNumber']).strip(),
            'SeatsAvailable': int(data['SeatsAvailable']),
            'Fare':          float(data['Fare']),
            'Note':          str(data.get('Note') or '').strip()
        }
    except (ValueError, TypeError):
        return jsonify({'error': '坐标、座位数或费用格式不正确'}), 400

    # 解析出发时间 (ISO8601 或 “YYYY-MM-DD HH:MM”)
    departure_raw = str(data['DepartureTime']).strip()
    try:
        if 'T' in departure_raw:
            # ISO 格式
            departure_dt = datetime.fromisoformat(departure_raw)
        else:
            departure_dt = datetime.strptime(departure_raw, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'DepartureTime 时间格式应为 ISO8601 或 YYYY-MM-DD HH:MM'}), 400
    posting_kwargs['DepartureTime'] = departure_dt

    # 创建并保存
    posting = DriverPosting(**posting_kwargs)
    db.session.add(posting)
    db.session.commit()

    return jsonify({'message': '发布成功', 'posting': posting.serialize()}), 201

# --------------------------------  行程列表接口  --------------------------------
def _haversine(lat1, lng1, lat2, lng2):
    """
    Returns great‑circle distance in kilometres between two points on the Earth.
    """
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.asin(math.sqrt(a))


@app.route('/get_driver_postings', methods=['GET'])
@jwt_required()
def list_driver_postings():
    limit = request.args.get('limit', 2, type=int)
    now = db.func.now()
    identity = get_jwt_identity()
    user_id = int(identity)
    postings = DriverPosting.query.filter((DriverPosting.DepartureTime > now) &\
       (DriverPosting.DrviverID!=user_id)).all()

    def _coord(name):
        try:
            return float(request.args.get(name))
        except (TypeError, ValueError):
            return None

    from_name = request.args.get('From', '')
    to_name = request.args.get('To', '')
    flt, flng = _coord('FromLat'), _coord('FromLng')
    tlt, tlng = _coord('ToLat'), _coord('ToLng')

    # 排序逻辑保持不变
    if from_name == '' and to_name != '' and None not in (tlt, tlng):
        postings.sort(key=lambda p: _haversine(tlt, tlng, p.ToLat, p.ToLng))
    elif from_name != '' and to_name == '' and None not in (flt, flng):
        postings.sort(key=lambda p: _haversine(flt, flng, p.FromLat, p.FromLng))
    elif from_name != '' and to_name != '' and None not in (flt, flng, tlt, tlng):
        postings.sort(key=lambda p: (
            _haversine(flt, flng, p.FromLat, p.FromLng) +
            _haversine(tlt, tlng, p.ToLat, p.ToLng)
        ))
    else:
        postings.sort(key=lambda p: p.DepartureTime)

    # 查询所有 PostingID
    posting_ids = [p.PostingID for p in postings]

    # 查询预约人数统计
    counts = db.session.query(
        RideJoin.PostingID,
        db.func.count(RideJoin.JoinID).label('join_count')
    ).filter(RideJoin.PostingID.in_(posting_ids)) \
     .group_by(RideJoin.PostingID).all()

    # 转成字典便于快速查找
    join_count_map = {cid: cnt for cid, cnt in counts}

    # 在每条 posting 上添加预约人数字段
    result = []
    for p in postings[:limit]:
        obj = p.serialize()
        obj['JoinCount'] = join_count_map.get(p.PostingID, 0)  # 默认0
        obj['Tel'] = p.driver.Tel if p.driver else None
        obj['Name'] = p.driver.Name if p.driver else None
        result.append(obj)

    return jsonify(result), 200

@app.route('/my_trip', methods=['GET'])
@jwt_required()
def get_my_trip():
    identity = get_jwt_identity()
    user_id = int(identity)

    now = db.func.now()

    ride = (RideJoin.query
        .join(DriverPosting, RideJoin.PostingID == DriverPosting.PostingID)
        .filter(RideJoin.UserID == user_id)
        .filter(DriverPosting.DepartureTime > now)
        .order_by(DriverPosting.DepartureTime.asc())
        .first())
    if not ride:
        return jsonify([]), 200
    # 构造与 /get_driver_postings 相同的结构
    postings = [ride.posting]
    posting_ids = [p.PostingID for p in postings]

    # 查询预约人数统计
    counts = db.session.query(
        RideJoin.PostingID,
        db.func.count(RideJoin.JoinID).label('join_count')
    ).filter(RideJoin.PostingID.in_(posting_ids)) \
     .group_by(RideJoin.PostingID).all()

    join_count_map = {cid: cnt for cid, cnt in counts}

    result = []
    for p in postings:
        obj = p.serialize()
        obj['JoinCount'] = join_count_map.get(p.PostingID, 0)  # 默认0
        obj['Tel'] = p.driver.Tel if p.driver else None
        obj['Name'] = p.driver.Name if p.driver else None
        result.append(obj)

    return jsonify(result), 200

if __name__ == '__main__':
	with app.app_context():
		db.create_all()  # 确保所有表已创建
	app.run(host='0.0.0.0', port=3001, debug=True)