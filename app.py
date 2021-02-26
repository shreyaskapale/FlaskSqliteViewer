from flask import Flask, render_template, request
import requests
import sqlite3
from bs4 import BeautifulSoup


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('teditor.html')


@app.route('/suggestions')
def suggestions():
    text = request.args.get('jsdata')


    tdata = []
    cnames_list = []
    if text:
    	
    	con = sqlite3.connect("food.db")
    	cursorObj = con.cursor()
    	if(text == "showtable"):
    		cursorObj.execute('SELECT name from sqlite_master where type= "table"')
    		tables = cursorObj.fetchall()

    		for i in tables:
    			tdata.append(*i)
    		return render_template('tablist.html', suggestions=tdata)
    	elif "showstruct" in text:
    		x = text.split(":")
    		tname = x[1]
    		cursorObj.execute("PRAGMA table_info('" + tname +"')")
    		r = cursorObj.fetchall()
    		for i in r:
    			tdata.append(i)
    		return render_template('suggestions.html', suggestions=tdata)
    	elif "showcontent" in text:
    		x = text.split(":")
    		tname = x[1]

    		cursorObj.execute("PRAGMA table_info('" + tname +"')")
    		r = cursorObj.fetchall()
    		for i in r:
    			cnames_list.append(i[1])


    		cursorObj.execute("select * from " + tname)
    		tcontent = cursorObj.fetchall()
    		for i in tcontent:
    			tdata.append(i)
    		return render_template('tcontent.html', suggestions=tdata, cnames = cnames_list)
    	elif "delete" in text:
    		x = text.split(":")
    		tname = x[1]
    		cid = x[2]
    		ctd = x[3]
    		cell = x[4]
    		if(not RepresentsInt(cell)):
    			cell = "'"+cell+"'"
    		cursorObj.execute("DELETE FROM "+ tname + " WHERE " + cid + ctd + cell);

    		cursorObj.execute("PRAGMA table_info('" + tname +"')")
    		r = cursorObj.fetchall()
    		for i in r:
    			cnames_list.append(i[1])


    		cursorObj.execute("select * from " + tname)
    		tcontent = cursorObj.fetchall()
    		for i in tcontent:
    			tdata.append(i)
    		return render_template('tcontent.html', suggestions=tdata, cnames = cnames_list)
    	elif "update" in text:
    		x = text.split(":")
    		tname = x[1]
    		cid = x[2]
    		ctd = x[3]
    		cell = x[4]
    		scid = x[5]
    		val = x[6]
    		if(not RepresentsInt(cell)):
    			cell = "'"+cell+"'"
    		if(not RepresentsInt(val)):
    			val = "'"+val+"'"

    		fctd = cid + ctd + cell
    		sql = "UPDATE {0} SET {1} = {2} WHERE {3}".format(tname,scid,val,fctd)
    		cursorObj.execute(sql);
    		cursorObj.execute("PRAGMA table_info('" + tname +"')")
    		r = cursorObj.fetchall()
    		for i in r:
    			cnames_list.append(i[1])


    		cursorObj.execute("select * from " + tname)
    		tcontent = cursorObj.fetchall()
    		for i in tcontent:
    			tdata.append(i)
    		return render_template('tcontent.html', suggestions=tdata, cnames = cnames_list)


if __name__ == '__main__':
    app.run(debug=True)
