from flask import Flask, render_template, request, redirect, url_for

# Flask 애플리케이션 초기화
app = Flask(__name__)

# DB 기본코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

# 테이블 생성
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)    # 이름
    part = db.Column(db.String(100), nullable=False)        # 역할
    mbti = db.Column(db.String(100), nullable=False)        # MBTI
    comment = db.Column(db.String(100), nullable=False)     # 각오
    advantage = db.Column(db.String(100), nullable=False)   # 장점
    tmi = db.Column(db.String(1000), nullable=False)         # TMI
    blog = db.Column(db.String(1000), nullable=False)         # 블로그주소
    image_url = db.Column(db.String(10000), nullable=False)  # 사진

    # def __repr__(self):
    #     return f'{self.username} {self.title} 추천 by {self.username}'

with app.app_context():
    db.create_all()

# 메인페이지
@app.route("/")
def home():
    # 전부 다 가져오기
    team_list = Team.query.all()
    return render_template('index.html', data = team_list)

# 데이터 받아오기(모달)
@app.route('/create', methods=['POST'])
def team_create():
    # form으로 데이터 입력 받기
    username_receive = request.args.get("username")
    part_receive = request.args.get("part")
    mbti_receive = request.args.get("mbti")
    comment_receive = request.args.get("comment")
    advantage_receive = request.args.get("advantage")
    tmi_receive = request.args.get("tmi")
    blog_receive = request.args.get("blog")
    image_receive = request.args.get("image_url")

    team = Team(username=username_receive, part=part_receive, mbti=mbti_receive, comment=comment_receive, 
    advantage=advantage_receive, tmi=tmi_receive, blog=blog_receive, image_url=image_receive)
    db.session.add(team)
    db.session.commit()

    return redirect(url_for('render_team_filter', username=username_receive))


if __name__ == '__main__':
    app.run(debug=True)
