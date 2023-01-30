from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm  # 폼 관리, CSRF보호, 유효성 검사, 리캡차 기능
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename  # 사용자 업로드 파일명 검증

import os
import time
import datetime

app = Flask(__name__)
"""
CSRF 공격을 방지하기 위한 토큰으로 flask-wtf 사용을 위해 필요함 
form을 통해 전송된 데이터가 실제 웹에서 작성된 데이터인지 위조된 스크립트인지 판단
실제로는 보안을 위해 유추하기 어려운 물자열을 사용
"""
app.config['SECRET_KEY'] = "secret"
# 파일 업로드 용량 제한
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16mb


class FileForm(FlaskForm):
	files = FileField(validators=[FileRequired("Please select file for upload")])


# 날짜 데이터 포멧 변환
def stamp2real(stamp):
	return datetime.datetime.fromtimestamp(stamp)


def getctime(file_path):
	return os.path.getctime(file_path)

def getmtime(file_path):
	return os.path.getmtime(file_path)

def getsize(file_path):
	return os.path.getsize(file_path)


@app.route('/', methods=['GET', 'POST'])
def upload_page():
	form = FileForm()
	if form.validate_on_submit():
		f = form.files.data
		f.save('./uploads/' + f.filename)
		return render_template('check.html', pwd=os.getcwd() + "\\uploads")

	filelist = os.listdir('./uploads')
	infos = [{
		"name": name,
		"extension": os.path.splitext(name)[1].lower(),
		"create": stamp2real(getctime('./uploads/' + name)),
		"modify": stamp2real(getmtime('./uploads/' + name)),
		"size": "%.2f KB" % (getsize('./uploads/' + name) / 1024) if getsize('./uploads/' + name) / 1024 <= 1000000
		else "%.2f MB" % (getsize('./uploads/' + name) / 1024 <= 1000000 / (1024.0 * 1024.0))
	} for name in filelist]
	return render_template('home.html', form=form, pwd=os.getcwd() + "\\uploads", infos=infos)


if __name__ == '__main__':
	app.run(debug=True)