import pymysql
def access_mysql():
    conn = pymysql.connect(host='qdm10645012.my3w.com',port=3306,db='qdm10645012_db', user='qdm10645012',password='asxxsw21')
    cur = conn.cursor()
    cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES")
    for r in cur:
        #print(r)
        if(r[2]=='wp_users'):
            print(r)
            cur.execute("select * from wp_users")
            for r in cur:
                print(r)
    cur.close()
    conn.close()
if __name__== '__main__':
    access_mysql()