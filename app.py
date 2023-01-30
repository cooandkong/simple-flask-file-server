from flask import Flask
from flask import render_template
from flask import request
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


# 파일 정보
def info(filename):
	ctime = os.path.getctime(filename)
	mtime = os.path.getmtime(filename)
	atime = os.path.getatime(filename)
	size = os.path.getsize(filename)
	return ctime, mtime, atime, size


@app.route('/', methods=['GET', 'POST'])
def upload_page():
	form = FileForm()
	if form.validate_on_submit():
		f = form.files.data
		f.save('./uploads/' + secure_filename(f.filename))

		file_info = {}
		ctime, mtime, atime, size = info('./uploads/' + f.filename)
		file_info["create"] = stamp2real(ctime)
		file_info["modify"] = stamp2real(ctime)
		file_info["access"] = stamp2real(ctime)
		if size <= 1000000:
			file_info["size"] = "%.2f KB" % (size / 1024)
		else:
			file_info["size"] = "%.2f MB" % (size / (1024.0 * 1024.0))

		return render_template('check.html', file_info=file_info)
	return render_template('upload.html', form=form)


if __name__ == '__main__':
	app.run()