# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 12:07:59 2020

@author: SSSar
"""

from flask import Flask, render_template, request, session, url_for, redirect
import csv
from docplex.mp.model import Model
from openpyxl import load_workbook
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/hos')
def hos():
    return render_template('hos.html')

@app.route('/dect')
def dect():
    return render_template('dect.html')

@app.route('/donator')
def donator():
    return render_template('donator.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/hosAuth', methods=['GET', 'POST'])
def hospital():
    date = request.form['date']
    hsp_name = request.form['name']
    request_num = request.form['number']
    
    l = []
    with open('hospital.csv','rt') as f:
        cr = csv.DictReader(f)
        for row in cr:
            l.append(row)
    with open('hospital.csv','wt',newline = '') as csvfile:
        fieldnames = ['date','hospital name','request number']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(l)
        writer.writerow({'date':date,'hospital name':hsp_name,'request number':request_num})
        csvfile.close()
    return render_template('hos.html')

@app.route('/deliveryAuth', methods=['GET', 'POST'])     
def deliveryAuth():
    hospitallist = []
    with open('hospital.csv','r') as f:
        station = csv.DictReader(f)
        for row in station:
            hospitallist.append((row['date'],row['hospital name'],row['request number']))
    f.close()
    
    workbook = load_workbook('distance.xlsx')    #找到需要xlsx文件的位置
    booksheet = workbook.active                 #获取当前活跃的sheet,默认是第一个sheet

    #获取sheet页的行数据
    rows = booksheet.rows
    #获取sheet页的列数据
    columns = booksheet.columns

    distance = []
    i = 0
    # 迭代所有的行
    for row in rows:
        line = [col.value for col in row if col.value != None]
        if line != []:
            distance.append(line)
    dis = []
    dist = []
    for i in range(1, len(distance)):
        for j in distance[i][1:]:
            if j != 0.0:
                j = float(j[:-2])
            dis.append(j)
        dist.append(dis)
        dis = []
    
    weight = []

    for i in dist[1:]:
        demand = 0
        for j in hospitallist:
            if j[0] == '2020/7/2':
                if j[1] == i:
                    demand = j[2]
        weight.append(demand)

    n = len(distance) - 2 #医院
    Q = 3000

    # M = [i for i in range(1,m+1)]
    N = [i for i in range(1,n+1)]
    V = [0] + N
    A = [(i,j) for i in V for j in V if i != j]

    q = {i:weight[i-1] for i in N}
    c = {(i,j): dist[i][j] for i,j in A}
    mdl = Model('CVRP')
    x = mdl.binary_var_dict(A, name='x')
    u = mdl.continuous_var_dict(N, ub = Q, name='u')
    mdl.minimize(mdl.sum(c[i,j]*x[i,j] for i,j in A))
    mdl.add_constraints(mdl.sum(x[i,j] for j in V if j!= i) == 1 for i in N)
    mdl.add_constraints(mdl.sum(x[i,j] for i in V if i!= j) == 1 for j in N)
    mdl.add_indicator_constraints(mdl.indicator_constraint(x[i,j],u[i] + q[j] == u[j]) for i,j in A if i!=0 and j!=0)
    solution = mdl.solve(log_output = True)
    actove_arcs = [a for a in A if x[a].solution_value > 0.9] 

    all_order = []
    one = []
    actove = actove_arcs[:]
    for i,j in actove:
    # print(actove)
    # print((i,j))
        if i != 0:
            break
        if i == 0:
            one.append(distance[0][i])
            one.append(distance[0][j])
        while j != 0:
            for m,n in actove:
            # print((m,n))
                if m == j:
                    one.append(distance[0][n])
                    j = n
            
        all_order.append(one)
        one = []
    
    l = []
    with open('route.csv','rt') as f:
        cr = csv.DictReader(f)
        for row in cr:
            l.append(row)
    with open('route.csv','wt',newline = '') as csvfile:
        fieldnames = ['Route1','Route2','Route3','Route4']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(l)
        writer.writerow({'Route1':all_order[0],'Route2':all_order[1],'Route3':all_order[2],'Route4':all_order[3]})
        csvfile.close()

    return render_template('delivery.html',result=json.dumps(all_order))

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
