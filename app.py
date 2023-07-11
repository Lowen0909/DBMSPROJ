from flask import Flask,render_template,request,session,redirect,url_for
import api,db
import json
app = Flask(__name__)
app.secret_key = 'my secret key'
#首頁
@app.route('/')
def mainpage():
    if session.get('loggedin')==None:
       session['loggedin']=False
    return render_template('parking_web.html')

#停車場查詢頁面
@app.route('/parkinglot')
def parklotsearch():
    return render_template('carpark.html')

#路段查詢頁面
@app.route('/road')
def roadsearch():
    return render_template('search_road.html')

#路段查詢api
@app.route('/roadapi',methods=['POST'])
def roadapi():    
    city = request.form['city']
    keyword=request.form['keyword']
    
    citytw=""
    citycode=""
    if city=="Taoyuan":
        citytw="桃園市"
        citycode="TAO"
    elif city== "Tainan":
        citytw="台南市"
        citycode="TNN"
    elif city== 'NewTaipei':
        citytw="新北市"
        citycode="NWT"
    elif city== "HualienCounty":
        citytw="花蓮縣"
        citycode="HUA"

    url ='https://tdx.transportdata.tw/api/basic/v1/Parking/OnStreet/ParkingSegmentAvailability/City/'+city

    if keyword!="":
        url+="?$filter=contains(ParkingSegmentName/Zh_tw,'"+keyword+"')"

    data_response=api.tdxapi(url)  

    isfind=1
    result =[]
    if len(data_response["CurbParkingSegmentAvailabilities"])==0:
        isfind=0
        data={'city':citytw,'isfind':isfind}
        return render_template('roadresult.html',data=data)
    else:
        isfind=1
        spacetypetable={'0':'所有停車位類型','1':'自小客車位','2':'機車位','3':'重型機車位','4':'腳踏車位','5':'大型車位','6':'小型巴士位',
                        '7':'孕婦及親子專用車位','8':'婦女車位','9':'身心障礙汽車車位','10':'身心障礙機車車位','11':'電動汽車車位','12':'電動機車車位',
                        '13':'復康巴士','14':'月租機車位','15':'月租汽車位','16':'季租機車位','17':'季租汽車位','18':'半年租機車位','19':'半年租汽車位',
                        '20':'年租機車位','21':'年租汽車位','22':'租賃機車位','23':'租賃汽車位','24':'卸貨車位','25':'計程車位','26':'夜間安心停車位',
                        '27':'臨時停車','28':'專用停車','29':'預約停車','254':'其他','255':'未知'}
        statustable={'0':'休息中','1':'營業中','2':'暫停營業'}
        for value in data_response["CurbParkingSegmentAvailabilities"]:
            a = {}
            a["ID"]=value["ParkingSegmentID"]
            a["名稱"]=value["ParkingSegmentName"]["Zh_tw"]
            a["剩餘車位"]=str(value["AvailableSpaces"])+'/'+str(value['TotalSpaces'])
            a["營業狀態"]=statustable[str(value['ServiceStatus'])]
            a["citycode"]=citycode
            a["車位類型"]=""
            if len(value['Availabilities'])!=0:
                for spacetype in value['Availabilities']: 
                    a["車位類型"]=a["車位類型"]+spacetypetable[str(spacetype['SpaceType'])]+"x"+str(spacetype['NumberOfSpaces'])+" "
            else:
                a["車位類型"]="無資料"
            result.append(a)
        id=tuple(map(lambda x:x["ID"],result))
        if session['loggedin']==True:
            fav=db.searchinfav_seg(id,citycode,session["account"])
            fav1=dict(map(lambda x:(x["space_name"],"True"),fav))
            print(fav1)
            data={'city':citytw,'isfind':isfind,'result':result}
            return render_template('roadresult.html',data=data,fav=fav1)
        else:
            fav1={}
            data={'city':citytw,'isfind':isfind,'result':result}
            return render_template('roadresult.html',data=data,fav=fav1)

    


#停車場查詢api
@app.route('/parkinglotapi',methods=['POST'])
def parkinglotapi():
    
    city = request.form['city']
    keyword=request.form['keyword']
    
    citytw=""
    citycode=""
    if city=="Taoyuan":
        citytw="桃園市"
        citycode="TAO"
    elif city== "Tainan":
        citytw="台南市"
        citycode="TNN"
    elif city== 'Keelung':
        citytw="基隆市"
        citycode="KEE"
    elif city=="YilanCounty":
        citytw="宜蘭縣"
        citycode="ILA"
    elif city== "HualienCounty":
        citytw="花蓮縣"
        citycode="HUA"

    url = 'https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/'+city

    if keyword!="":
        url+="?$filter=contains(CarParkName/Zh_tw,'"+keyword+"')"

    data_response=api.tdxapi(url)

    isfind=1
    result =[]
    if len(data_response["ParkingAvailabilities"])==0:
        isfind=0
        data={'city':citytw,'isfind':isfind}
        return render_template('parkinglotresult.html',data=data)
    else:
        isfind=1
        spacetypetable={'0':'所有停車位類型','1':'自小客車位','2':'機車位','3':'重型機車位','4':'腳踏車位','5':'大型車位','6':'小型巴士位',
                        '7':'孕婦及親子專用車位','8':'婦女車位','9':'身心障礙汽車車位','10':'身心障礙機車車位','11':'電動汽車車位','12':'電動機車車位',
                        '13':'復康巴士','14':'月租機車位','15':'月租汽車位','16':'季租機車位','17':'季租汽車位','18':'半年租機車位','19':'半年租汽車位',
                        '20':'年租機車位','21':'年租汽車位','22':'租賃機車位','23':'租賃汽車位','24':'卸貨車位','25':'計程車位','26':'夜間安心停車位',
                        '27':'臨時停車','28':'專用停車','29':'預約停車','254':'其他','255':'未知'}
        statustable={'0':'休息中','1':'營業中','2':'暫停營業'}
        for value in data_response["ParkingAvailabilities"]:
            a = {}
            a["ID"]=value["CarParkID"]
            a["名稱"]=value["CarParkName"]["Zh_tw"]
            a["剩餘車位"]=str(value["AvailableSpaces"])+'/'+str(value['TotalSpaces'])
            a["營業狀態"]=statustable[str(value['ServiceStatus'])]
            a["citycode"]=citycode
            a["車位類型"]=""
            if len(value['Availabilities'])!=0:
                for spacetype in value['Availabilities']: 
                    a["車位類型"]=a["車位類型"]+spacetypetable[str(spacetype['SpaceType'])]+"x"+str(spacetype['NumberOfSpaces'])+" "
            else:
                a["車位類型"]="無"
            result.append(a)
        id=tuple(map(lambda x:x["ID"],result))
        if len(id)==1:
            id="("+str(id[0])+")"
        if session['loggedin']==True:
            fav=db.searchinfav(id,citycode,session["account"])
            if len(fav)==0:
                fav1={}
            else:
                fav1=dict(map(lambda x:(x["parklot_id"],"True"),fav))
            print(fav1)
            data={'city':citytw,'isfind':isfind,'result':result}
            return render_template('parkinglotresult.html',data=data,fav=fav1)
        else:
            fav1={}
            data={'city':citytw,'isfind':isfind,'result':result}
            return render_template('parkinglotresult.html',data=data,fav=fav1)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        ID=str(request.form['ID'])
        account=str(request.form['account'])
        password=str(request.form['password'])
        check=db.newmember(ID,account,password)
        if check:
            msg="註冊成功"
        else:
            msg="註冊失敗"
        return render_template('register.html',msg=msg)
    else:
        return render_template('register.html',msg="")
#####################登入、登出功能#######################
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'account' in request.form and 'password' in request.form:
        account = str(request.form['account'])
        password = str(request.form['password'])
        result =db.memberlogin(account,password)

        if result['msg']=='success':
            session['loggedin'] = True
            session['id'] = result['id']
            session['account'] = result['account']
            return render_template('parking_web.html')
        else:
            msg = 'Incorrect account or password!'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html', msg=msg)
    
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('account', None)
   return redirect('/')

@app.route('/resetpass', methods = ['GET', 'POST'])
def resetpass():
    if request.method == 'POST':
        account = str(request.form['account'])
        resetpass = str(request.form['password'])
        print('更新密碼為:'+resetpass+'\n')
        flag = db.resetpass(account,resetpass)
        if (flag == 1):
            return render_template('resetpass.html', msg='密碼已成功更改為'+resetpass+"\n")
        else:
            return render_template('resetpass.html', msg='密碼更改失敗\n')
    else:
        return render_template('resetpass.html',msg="")

@app.route('/favoritepage',methods=['POST','GET'])
def favoritepage():
    if session['loggedin']==False:
        return redirect(url_for('login'))
    return render_template('favorite.html')

@app.route('/favorite',methods=['POST','GET'])
def favorite():
    if session['loggedin']==False:
        return "False"
        # return "False"
    elif request.method=='GET':
        return render_template('favorite.html')
    elif request.method=='POST':
        result=db.favorite(str(session["account"]),str(request.form["id"]),str(request.form["citycode"]),request.form["method"])
        return result
    else:
        return

@app.route('/favorite_seg',methods=['POST','GET'])
def favorite_seg():
    if session['loggedin']==False:
        return "False"
    elif request.method=='GET':
        #favorite=db.favorite()
        return render_template('favorite.html')
    elif request.method=='POST':
        result=db.favorite_seg(str(session["account"]),str(request.form["id"]),str(request.form["citycode"]),request.form["method"])
        return result
    else:
        return

@app.route('/comment_parklot',methods=['POST'])
def comment_parklot():
    item_id = str(request.form.get("id"))
    print(item_id)
    citycode = str(request.form.get("citycode"))
    user_id = str(session["id"])
    comment_text = str(request.form.get("comment"))
    db.comment(user_id, item_id, citycode, comment_text)
    return "success"

@app.route('/comment_seg',methods=['POST'])
def comment_seg():
    item_id = str(request.form.get("id"))
    print(item_id)
    citycode = str(request.form.get("citycode"))
    user_id = str(session["id"])
    comment_text = str(request.form.get("comment"))
    db.comment_seg(user_id, item_id, citycode, comment_text)
    return "success"

@app.route('/comment_parklot_show',methods=['POST','GET'])
def comment_parklot_show():
    if session['loggedin']==False:
        return "False"
    elif request.method == 'GET':
        return render_template('parkinglotresult.html')
    elif request.method == 'POST':
        result = db.searchincomment(str(request.form["id"]), str(request.form["citycode"]))
        return result
    else:
        return
@app.route('/comment_seg_show',methods=['POST','GET'])
def comment_seg_show():
    if session['loggedin']==False:
        return "False"
    elif request.method == 'GET':
        return render_template('roadresult.html')
    elif request.method == 'POST':
        result = db.searchincomment_seg(str(request.form["id"]), str(request.form["citycode"]))
        return result
    else:
        return
    


@app.route('/searchparklotapi',methods=['POST'])
def searchparkinglotapi():
    
    citycode = request.form['citycode']
    # name=request.form['parkname']
    id=request.form['id']

    if citycode=="TAO":
        city="Taoyuan"
    elif citycode== "TNN":
        city="Tainan"
    elif citycode== "KEE":
        city='Keelung'
    elif citycode=="ILA":
        city="YilanCounty"
    elif citycode== "HUA":
        city="HualienCounty"

    url = 'https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/'+city
    url+="?$filter=CarParkID eq '"+id+"'"
    # and CarParkName/Zh_tw eq '"+name+"'"

    data_response=api.tdxapi(url)
    isfind=1
    result =[]
    if len(data_response["ParkingAvailabilities"])==0:
        isfind=0
        data={'msg':"not found"}
        return data
    else:
        isfind=1
        spacetypetable={'0':'所有停車位類型','1':'自小客車位','2':'機車位','3':'重型機車位','4':'腳踏車位','5':'大型車位','6':'小型巴士位',
                        '7':'孕婦及親子專用車位','8':'婦女車位','9':'身心障礙汽車車位','10':'身心障礙機車車位','11':'電動汽車車位','12':'電動機車車位',
                        '13':'復康巴士','14':'月租機車位','15':'月租汽車位','16':'季租機車位','17':'季租汽車位','18':'半年租機車位','19':'半年租汽車位',
                        '20':'年租機車位','21':'年租汽車位','22':'租賃機車位','23':'租賃汽車位','24':'卸貨車位','25':'計程車位','26':'夜間安心停車位',
                        '27':'臨時停車','28':'專用停車','29':'預約停車','254':'其他','255':'未知'}
        statustable={'0':'休息中','1':'營業中','2':'暫停營業'}
        for value in data_response["ParkingAvailabilities"]:
            a = {}
            a["ID"]=value["CarParkID"]
            a["名稱"]=value["CarParkName"]["Zh_tw"]
            a["剩餘車位"]=str(value["AvailableSpaces"])+'/'+str(value['TotalSpaces'])
            a["營業狀態"]=statustable[str(value['ServiceStatus'])]
            a["citycode"]=citycode
            a["車位類型"]=""
            if len(value['Availabilities'])!=0:
                for spacetype in value['Availabilities']: 
                    a["車位類型"]=a["車位類型"]+spacetypetable[str(spacetype['SpaceType'])]+"x"+str(spacetype['NumberOfSpaces'])+" "
            else:
                a["車位類型"]="無"
            result.append(a)
        
        data={'msg':'success','isfind':isfind,'result':result}
        return data

@app.route('/searchparksegapi',methods=['POST'])
def searchparksegapi():
    
    citycode = request.form['citycode']
    # name=request.form['parkname']
    id=request.form['id']

    if citycode=="NWT":
        city="NewTaipei"
    elif citycode== "TAO":
        city="Taoyuan"
    elif citycode== "TNN":
        city='Tainan'
    elif citycode== "HUA":
        city="HualienCounty"

    url = 'https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/'+city
    url+="?$filter=ParkingSegmentID eq '"+id+"'"
    # and CarParkName/Zh_tw eq '"+name+"'"

    data_response=api.tdxapi(url)
    isfind=1
    result =[]
    if len(data_response["CurbParkingSegmentAvailabilities"])==0:
        isfind=0
        data={'msg':"not found"}
        return data
    else:
        isfind=1
        spacetypetable={'0':'所有停車位類型','1':'自小客車位','2':'機車位','3':'重型機車位','4':'腳踏車位','5':'大型車位','6':'小型巴士位',
                        '7':'孕婦及親子專用車位','8':'婦女車位','9':'身心障礙汽車車位','10':'身心障礙機車車位','11':'電動汽車車位','12':'電動機車車位',
                        '13':'復康巴士','14':'月租機車位','15':'月租汽車位','16':'季租機車位','17':'季租汽車位','18':'半年租機車位','19':'半年租汽車位',
                        '20':'年租機車位','21':'年租汽車位','22':'租賃機車位','23':'租賃汽車位','24':'卸貨車位','25':'計程車位','26':'夜間安心停車位',
                        '27':'臨時停車','28':'專用停車','29':'預約停車','254':'其他','255':'未知'}
        statustable={'0':'休息中','1':'營業中','2':'暫停營業'}
        for value in data_response["CurbParkingSegmentAvailabilities"]:
            a = {}
            a["ID"]=value["ParkingSegmentID"]
            a["名稱"]=value["ParkingSegmentName"]["Zh_tw"]
            a["剩餘車位"]=str(value["AvailableSpaces"])+'/'+str(value['TotalSpaces'])
            a["營業狀態"]=statustable[str(value['ServiceStatus'])]
            a["citycode"]=citycode
            a["車位類型"]=""
            if len(value['Availabilities'])!=0:
                for spacetype in value['Availabilities']: 
                    a["車位類型"]=a["車位類型"]+spacetypetable[str(spacetype['SpaceType'])]+"x"+str(spacetype['NumberOfSpaces'])+" "
            else:
                a["車位類型"]="無"
            result.append(a)
        
        data={'msg':'success','isfind':isfind,'result':result}
        return data





if __name__=="__main__":
    app.debug = True
    app.run()