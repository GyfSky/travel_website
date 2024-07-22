from flask import Flask,request,jsonify

#初始化,实例化这个类
app=Flask(__name__)
#methods=['POST','GET']增加post的访问形式
#@app.route调用形式 
@app.route("/index",methods=['POST','GET'])
def index():
    #GET获取参数
    age1=request.args.get("age")
    name1=request.args.get("name")
    #POST传递参数(key,value形式)
    xx=request.form.get('xx')
    #POST传递参数(json形式)不用import jsonify
    yy=request.json

    #返回的只能是字符串或者是json形式
    # return 'success'
    
    #返回json
    #1 import json

    # import json    
    # return json.dumps({'stuts':True,'data':'dsfsdffd'})
    
    #2 用jsonitf
    return jsonify({'stuts':True,'data':'dsfsdffd'})

#运行
#host='127.0.1.1',port=4399 改地址和端口
if __name__=='__main__':
    app.run(host='127.0.1.1',port=4399)