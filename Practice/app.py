from flask import flask, render_template,request,jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')



@app.route('/test', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})


@app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'}) 



@app.route('/mypage')
def mypage():  
   return 'This is My Page!'

@app.route('/mypage2')
def mypage2():  
   return 'This is a development server. Do not use it in a production deployment.'


if __name__ == '__main__':  
   app.run('localhost',port=5000,debug=True) 