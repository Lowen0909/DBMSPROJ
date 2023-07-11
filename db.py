import pymysql


db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "a123456",###########################################改成你的mysql密碼
        "db": "parking",
        "charset": "utf8",
        "cursorclass":pymysql.cursors.DictCursor,
        }
def newmember(id,account,password):
    conn = pymysql.connect(**db_settings)
    cursor=conn.cursor()
    sql=f"SELECT * FROM user WHERE account ='{account}'"
    cursor.execute(sql)
    if len(cursor.fetchall()):
        conn.close()
        return False
    else:
        sql= f"INSERT INTO user VALUES('{id}','{account}','{password}')"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
def memberlogin(account,password):
    conn = pymysql.connect(**db_settings)
    cursor=conn.cursor()
    sql=f"SELECT * FROM user WHERE account ='{account}' and password='{password}'"
    cursor.execute(sql)
    result=cursor.fetchone()
    print(result)
    if result:
        conn.close()
        return {'msg':'success','id':result['id'],'account':result['account']}
    else:
        conn.close()
        return {'msg':'fail'}
    
def resetpass(account,password):
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    sql = f"UPDATE user SET password ='{password}' WHERE account = '{account}';"
    try:
        print("正在修改密碼...")
        resetflag = cursor.execute(sql)
        conn.commit()
        #close_conn(conn, cursor)
        cursor.close()
        conn.close()
        if (resetflag == 1):
            print("修改成功")
            return 1
        else:
            print("修改失敗！")
            return 0
    except:
        print("系统錯誤...修改密碼失敗！")
        return

def favorite(account,id,citycode,operation):
    conn = pymysql.connect(**db_settings)
    cursor=conn.cursor()
    if operation=="delete":
        sql=f"SELECT * FROM favorite_parklot WHERE account ='{account}' and parklot_id='{id}' and citycode='{citycode}'"
        cursor.execute(sql)
        result=cursor.fetchone()
        print(result)
        if result:
            sql=f"DELETE FROM favorite_parklot WHERE account ='{account}' and parklot_id='{id}' and citycode='{citycode}'"
            result=cursor.execute(sql)
            conn.commit()
            conn.close()
            return {'msg':'success'}
        else:
            conn.close()
            return {'msg':'fail'}
        
    elif operation=="insert":
        sql=f"INSERT INTO favorite_parklot VALUES ('{account}','{id}','{citycode}')"
        result=cursor.execute(sql)
        print(result)
        conn.commit()
        conn.close()
        return {'msg':'success'}
    elif operation=="select":
        sql=f"SELECT p.parklot_id,p.parklot_name,p.descrip,p.address,p.fare,p.city,p.citycode FROM parking.favorite_parklot f , parking.parklot p WHERE f.parklot_id=p.parklot_id and f.account = '{account}'"
        cursor.execute(sql)
        result=cursor.fetchall()
        conn.close()
        if result:
         return result
        else:
         return []

def comment(id, park_seg_id, citycode, comment):
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    sql = f"SELECT * FROM parklot_comment p WHERE p.parklot_id ='{park_seg_id}' and p.user_id = '{id}'"
    cursor.execute(sql)
    if len(cursor.fetchall()):
        sql = f"UPDATE parklot_comment SET comment ='{comment}' WHERE parklot_id ='{park_seg_id}' and user_id = '{id}'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
    else:
        sql = f"INSERT INTO parklot_comment VALUES('{park_seg_id}','{citycode}','{comment}','{id}') "
        cursor.execute(sql)
        conn.commit()
        conn.close()
    return "success"

def comment_seg(id, park_seg_id, citycode, comment):
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    sql = f"SELECT * FROM parkseg_comment p WHERE p.park_seg_id ='{park_seg_id}' and p.user_id = '{id}'"
    cursor.execute(sql)
    if len(cursor.fetchall()):
        sql = f"UPDATE parkseg_comment SET comment ='{comment}' WHERE park_seg_id ='{park_seg_id}' and user_id = '{id}'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
    else:
        sql = f"INSERT INTO parkseg_comment VALUES('{park_seg_id}','{citycode}','{comment}','{id}') "
        cursor.execute(sql)
        conn.commit()
        conn.close()
    return "success"

def favorite_seg(account,id,citycode,operation):
    conn = pymysql.connect(**db_settings)
    cursor=conn.cursor()
    if operation=="delete":
        sql=f"SELECT * FROM favorite_parksegment WHERE account ='{account}' and space_name='{id}' and citycode='{citycode}'"
        cursor.execute(sql)
        result=cursor.fetchone()
        if result:
            sql=f"DELETE FROM favorite_parksegment WHERE account ='{account}' and space_name='{id}' and citycode='{citycode}'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return {'msg':'success'}
        else:
            conn.close()
            return {'msg':'fail'}
        
    elif operation=="insert":
        sql=f"INSERT INTO favorite_parksegment VALUES ('{account}','{id}','{citycode}')"
        result=cursor.execute(sql)
        print(result)
        conn.commit()
        conn.close()
        return {'msg':'success'}
    elif operation=="select":
        sql=f"SELECT p.segmentID,p.segmentname,p.description,p.fare,p.city,p.citycode FROM parking.favorite_parksegment f , parking.parksegment p WHERE f.space_name=p.segmentID and f.account = '{account}'"
        cursor.execute(sql)
        result=cursor.fetchall()
        conn.close()
        if result:
         return result
        else:
         return []
    
def searchinfav(list,citycode,account):
    conn = pymysql.connect(**db_settings)
    cursor=conn.cursor()
    print(list)
    sql=f"SELECT parklot_id FROM favorite_parklot WHERE parklot_id in {list} and  citycode='{citycode}'and account='{account}'"
    cursor.execute(sql)
    result=cursor.fetchall()
    conn.close()
    if result:
     return result
    else:
     return []

def searchinfav_seg(list,citycode,account):
    conn = pymysql.connect(**db_settings)
    cursor=conn.cursor()
    sql=f"SELECT space_name FROM favorite_parksegment WHERE space_name in {list} and  citycode='{citycode}'and account='{account}'"
    cursor.execute(sql)
    result=cursor.fetchall()
    conn.close()
    if result:
     return result
    else:
     return []
def searchincomment(id,citycode):
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    sql = f"SELECT user_id, comment FROM parklot_comment WHERE parklot_id ='{id}'and citycode='{citycode}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    if result:
        return result
    else:
        return []
def searchincomment_seg(id,citycode):
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    sql = f"SELECT user_id, comment FROM parkseg_comment WHERE park_seg_id ='{id}'and citycode='{citycode}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    if result:
        return result
    else:
        return []