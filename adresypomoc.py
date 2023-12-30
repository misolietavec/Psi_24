import sqlite3.dbapi2 as sqlite

def conn_open(dbname='adresy.sqlite'):
    conn = sqlite.connect(dbname)
    curs = conn.cursor()
    return curs,conn

def conn_close(curs,conn):
    curs.close()
    conn.close()

def searchAddr(mesto,ulica,cislo,like_ulica=False):
    curs,conn = conn_open()
    if not like_ulica:
        curs.execute("select c.Latitude,c.Longitude from ulice u, obce o, popcisla c \
        where o.MenoObce = ? and u.IdObce=o.IdObce and c.IdUlice=u.IdUlice and u.MenoUlice = ? \
        and c.CisloDomu = ?", (mesto,ulica,str(cislo)))
    else:
        curs.execute("select c.Latitude,c.Longitude from ulice u, obce o, popcisla c \
        where o.MenoObce = ? and u.IdObce=o.IdObce and c.IdUlice=u.IdUlice and u.MenoUlice like ? \
        and c.CisloDomu = ?", (mesto, '%'+ulica+'%', str(cislo)))
    res = curs.fetchall()
    conn_close(curs,conn)
    return res

def searchNums(mesto,ulica,like_ulica=False):
    curs,conn = conn_open()
    if not like_ulica:
        curs.execute("select c.CisloDomu from ulice u, obce o, popcisla c \
        where o.MenoObce = ? and u.IdObce=o.IdObce and c.IdUlice=u.IdUlice and u.MenoUlice = ?", (mesto,ulica))
    else:
        curs.execute("select c.CisloDomu from ulice u, obce o, popcisla c \
        where o.MenoObce = ? and u.IdObce=o.IdObce and c.IdUlice=u.IdUlice and u.MenoUlice like ?", (mesto, '%'+ulica+'%'))
    res = curs.fetchall()
    conn_close(curs,conn)
    return [p[0] for p in res]

def fuzzyUlica(mesto,ulica,fuzzy_mesto=False):
    curs,conn = conn_open()
    if not fuzzy_mesto:
        curs.execute("select u.MenoUlice from ulice u, obce o where o.MenoObce = ? and u.IdObce=o.IdObce \
        and u.MenoUlice like ?", (mesto,'%'+ulica+'%'))
    else:
        curs.execute("select u.MenoUlice from ulice u, obce o where o.MenoObce like ? and u.IdObce=o.IdObce \
        and u.MenoUlice like ?", ('%'+mesto+'%','%'+ulica+'%'))  
    res = curs.fetchall()
    conn_close(curs,conn)
    return [p[0] for p in res]

def lokaciaUlica(mesto,ulica,like_ulica=False):
    curs,conn = conn_open()
    if not like_ulica:
        curs.execute("select c.CisloDomu, c.Latitude, c.Longitude from ulice u, obce o, popcisla c \
        where o.MenoObce = ? and u.IdObce=o.IdObce and c.IdUlice=u.IdUlice and u.MenoUlice = ?", (mesto,ulica))
    else:
        curs.execute("select c.CisloDomu, c.Latitude, c.Longitude from ulice u, obce o, popcisla c \
        where o.MenoObce = ? and u.IdObce=o.IdObce and c.IdUlice=u.IdUlice and u.MenoUlice like ?", (mesto, '%'+ulica+'%'))
    res = curs.fetchall()
    conn_close(curs,conn)
    C,Lat,Lon = zip(*res)
    Polohy = list(zip(Lat,Lon))
    return C, Polohy
