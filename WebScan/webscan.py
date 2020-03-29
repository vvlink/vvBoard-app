# -*- coding: utf-8 -*-
import os,shutil,time
import itertools as it, glob
from flask import Flask, render_template, send_from_directory,request
import importlib,sys
importlib.reload(sys)
from PIL import Image

app = Flask(__name__)
#扫描文件的保存目录
home_path='/static/scan/'
scan_path=os.getcwd() + home_path

def multiple_file_types(*patterns):
    return it.chain.from_iterable(glob.iglob(scan_path + pattern) for pattern in patterns)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def doscan():
    ext="jpg"
    if (request.method == 'GET'):
        if request.values.get('ext'):
            ext=request.values.get('ext')
    # 编写扫描的命令
    i=scan_cnt()
    f1="scan%s.pnm"%i
    f2="scan" + str(i) + "."+ ext
    # return f2
    cmd = ("scanimage --mode Color --resolution 300 >")
    os.system(cmd + scan_path + f1)
    # print("图片扫描成功，正在转换。")
    cmd= "convert " + scan_path + f1 + " " + scan_path + f2
    os.system(cmd)
    cmd= "rm " + scan_path + f1
    os.system(cmd)
    html = "<div style='text-align:center;font-size:12px'>扫描完成！文件名为：“"+ f2 +"”，点击图片下载。<br><br>"
    html = html+ "<a href="+ home_path + f2 +" target=_blank><img width='60%' src='"+ home_path + f2 +"' /></a></div>"
    return html

@app.route('/cls')
def docls():
    # 清除文件夹
    shutil.rmtree(scan_path) # 能删除该文件夹和文件夹下所有文件
    os.mkdir(scan_path)
    html="<p style='text-align:center'>文件清理成功！</p>"
    return html
@app.route('/list')
def filelist():
    maps = {}
    scanlist=multiple_file_types("*.jpg","*.png","*.pdf")
    for fname in scanlist:
        if os.path.isfile(fname):
            #key = fname.decode('utf-8')
            key = fname.replace(os.getcwd(),"")
            attribute = {}
            attribute["size"]=round(os.path.getsize(fname)/1024,2)
            ftime=time.localtime(os.path.getctime(fname)) #文件创建时间
            attribute["time"]=time.strftime("%Y-%m-%d %H:%M:%S", ftime) 
            maps[key]= attribute
    # return maps
    # maps=sorted(maps,key = maps,reverse = False)
    return render_template('list.html', files=maps)

def scan_cnt():
    #一个简单的计数器
    with open('cnt.txt','a+') as f:
        f.seek(0)
        temp=f.read()
        if len(temp)>0:
            i=int(temp) + 1
        else:
            i=1
        f.seek(0)
        f.truncate() 
        f.write(str(i))
    return i

if __name__ == '__main__':
    #app.run(debug=True, port=80)
    app.run(debug=True, host='0.0.0.0', port=80)
