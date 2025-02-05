# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:04:46 2021

@author: kiera
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from extract_data import *
from sklearn.metrics import confusion_matrix

def displacement_till_stop(incident):#returns distance from incident to ignition off
    data=incident[2]
    
    
    time=keyword_time_checker(incident)
    print(time)
    #print(time)
    
    #print(data.head)
    ids = data.index[data['timeoffset'] == time].tolist()[0]
    gridx=0
    gridy=0
    #gridz=0
    gridx=data.loc[data.index[ids], 'gridx']
    gridy=data.loc[data.index[ids], 'gridy']
    #gridz=incident.loc[incident.index[ids], 'gridz']
    #coordinates of stop
    #displacement_till_stop(incident)
    mag = gridx**2+gridy**2#+gridz**2
    mag=mag**(1/2)
    return mag

def keyword_time_checker(incident,keyword="Ignition-Off"):

    data = incident[2]
    ignition_time_off = 0

    event_series = data['event']
    time_offset = data['timeoffset']
    length_events = len(event_series)

    for event in range(length_events):
        if event_series[event] == keyword and time_offset[event] > 0:
            ignition_time_off = time_offset[event]
            break 

    return ignition_time_off


#returns frequency of keyword
def check_keyword(incident, keyword="Ignition-Off"):
    # Returns the number of ignition-off events for an incident
    r = 0
    data = incident[2]
    data = data["event"].values

    for i in range(len(data)):
        if data[i] == keyword:
            r += 1

    return r #returns 0 if no keyword found


def get_max_vel_chng(incidentnum,data0):
    current=0
    data0 =data0["speed"].values
    #print(data0[-1])
    #print(data0)
    #print(type(data0))
    
    for i in range(8):
        #print(i)
        if(i<7):
            #print(i)
            print(abs(data0[i]-data0[i+1]))
            if abs(data0[i]-data0[i+1])>current:
               # print(abs(data0[i]-data0[i+1]))
                current = abs(data0[i]-data0[i+1])
    return current 

def get_vel_change(incident):
    data = incident[0]
    data = data['speed'].values
    d_v = data[6]-data[9]
    return d_v



#feature to see if ignition is turned off after the alert, and if so how long it took for that to happen 
#returns 0 if ignition is not turned off, returns an interger value of time offset if ignition is turned off
#if there are multiple ignition offs after the alert we take the 1st value
#keywordtimechecker(incident)    
#replace change kwarg for time offset of other keywords
def keyword_time_checker(incident,keyword="Ignition-Off"):

    data = incident[2]
    ignition_time_off = 0

    event_series = data['event']
    time_offset = data['timeoffset']
    length_events = len(event_series)

    for event in range(length_events):
        if event_series[event] == keyword and time_offset[event] > 0:
            ignition_time_off = time_offset[event]
            break 

    return ignition_time_off


def displacement_till_stop(incident):#returns distance from incident to ignition off
    data=incident[2]
    
    
    time=keyword_time_checker(incident)
    print(time)
    #print(time)
    
    #print(data.head)
    ids = data.index[data['timeoffset'] == time].tolist()[0]
    gridx=0
    gridy=0
    #gridz=0
    gridx=data.loc[data.index[ids], 'gridx']
    gridy=data.loc[data.index[ids], 'gridy']
    #gridz=incident.loc[incident.index[ids], 'gridz']
    #coordinates of stop
    #displacement_till_stop(incident)
    mag = gridx**2+gridy**2#+gridz**2
    mag=mag**(1/2)
    return mag


def get_max_acc(tilts):
    accs = []
    x = tilts[:,0]
    y = tilts[:,1]

    for i in range(len(x)):
        # Get the acceleration in the horizontal plane
        acc = np.linalg.norm([x[i], y[i]])
        accs.append(acc)

    return np.max(accs)

def distance_travelled(incident):  # calculates the distance travelled after the alert using zoomed out data
    # grab zoomed out data
    data = incident[2]

    # find x and y position of where the car ends up 
    xpos = data['gridx'].iloc[-1]
    ypos = data['gridy'].iloc[-1]
    xpos = xpos.item()
    ypos = ypos.item()

    # create vector of that position and find magnitude of it (distance)
    pos = np.array([xpos,ypos])
    distance = np.linalg.norm(pos)

    return distance


def extract_features(data):
    # Give data (cat/uncat) then recieve features array

    ignition_event_list = []
    stop_event_list = []
    d_v_list = []
    max_acc_list = []
    ignition_times_list = []
    distance_list = []

    tilts = get_tilt_timeseries(data)
    tilts_no_z = calibrate_remove_z(tilts)

    for incident in range(len(data)):
        ig = check_keyword(data[incident], keyword='Ignition-Off')
        st = check_keyword(data[incident], keyword='Stop')
        d_v = get_vel_change(data[incident])
        max_acc = get_max_acc(tilts_no_z[incident])
        ignition_time = ignition_off_checker(data[incident])
        distance = distance_travelled(data[incident])

        ignition_event_list.append(ig)
        stop_event_list.append(st)
        d_v_list.append(d_v)
        max_acc_list.append(max_acc)
        ignition_times_list.append(ignition_time)
        distance_list.append(distance)


    features = np.transpose(np.array([ignition_event_list, stop_event_list, d_v_list, max_acc_list, ignition_times_list, distance_list]))

    return features


cat_data = load_list('pickle_data', 'cat_data')

features = extract_features(cat_data)