import os
import uuid
from datetime import datetime
from datetime import timedelta



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
    # try:
    #     # 只校验签名，允许过期，忽略类型
    #     decoded = decode_token(token, allow_expired=True)
    #     print("✅ 刚生成的 token 成功解码：", decoded)
    # except jwt_exc.JWTDecodeError as e:
    #     # 如果这里失败，说明生成的 token 就有问题
    #     print("❌ 生成后立即 decode 失败：", e)
    
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

# @app.before_request
# def log_headers():
#     print("== headers ==")
#     print(dict(request.headers))


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

if __name__ == '__main__':
	with app.app_context():
		db.create_all()  # 确保所有表已创建
	app.run(host='0.0.0.0', port=3001, debug=True)