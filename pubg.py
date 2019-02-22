"""
This programm uses the data by https://www.kaggle.com/skihikingkevin/pubg-match-deaths (thanks for posting it)
the csv files contains: killed_by	killer_name    killer_placement    killer_position_x    killer_position_y    map    match_id    time    victim_name    victim_placement    victim_position_x    victim_position_y
written by Maximilian Zangl 12.02.18
"""
import numpy as np
import csv
import cv2

MAP_PATH = "erangel.jpg"
MAP_NAME ="ERANGEL"
DATA_PATH = "deaths\kill_match_stats_final_0.csv"
TEST_PATH= "tester.csv"
ANNOTATION="2"
    
#fucntions
def extract_data(csv_data_path,t1,t2):
    list_with_extracted_data = []
    with open(csv_data_path,"rb") as csv_file:
        reader = csv.reader(csv_file)
        labels = reader.next()        
        kpi = labels.index("killer_placement")
        map_name = labels.index("map")
        time = labels.index("time")
        for row in reader:
            #data gets filtered here:
            if(row[kpi]!="1.0" and row[map_name]=="ERANGEL"and t1<=int(row[time]) and int(row[time])<=t2):
                list_with_extracted_data.append(row)
        csv_file.close()
    return list_with_extracted_data

def extract_death_coordinates(killed_by):    
    death_coordinates = np.zeros([len(killed_by),2])
    i=0
    for row in killed_by:
        x = row[3] 
        y = row[4]
        try:
            death_coordinates[i]= [float(x),float(y)]
        except ValueError:
            death_coordinates[i]= [0,0]
        i=i+1
    return death_coordinates

def transform_coordinates_map_to_pixels(deaths_coordiantes):
    f = 4096.0/812800.0 #map is 800000x800000  pixel grid of 8x8  image is 4096x4096
    arr = np.multiply(deaths_coordiantes,f)
    deaths_pixels = arr.astype(np.int32)
    return  deaths_pixels

def draw_deaths_on_map(image_path,deaths_pixels,annotation):
    map_grey = cv2.imread(image_path,0)
    map = cv2.imread(image_path,1)
    map = cv2.cvtColor(map_grey,cv2.COLOR_GRAY2RGB)
    for row in deaths_pixels:
        if (row[0]<4097 and row[1]<4097):
            #cg = map_grey[row[1],row[0]]
            red = 255
            map[row[1],row[0]] = [0,0,red]
    cv2.imwrite("marked"+str(annotation)+".png",map)
    return
def bin_timeframe (max_min,bins):#e.g.40min and bins=2:  0-20min 20-40min as array[bins,2]
    step = max_min*60.0/bins
    time_arr = np.zeros([bins,2],np.int32)
    for i in range(bins):
        time_arr[i,0] = i*step
        time_arr[i,1] = (i+1)*step
    return time_arr

def draw_with_time (max_mins,bins):
    time_array = bin_timeframe(max_mins,bins)
    for i in range(len(time_array)):
        #print(i,time_array[i,0],time_array[i,1])
        kbw=extract_data(DATA_PATH,time_array[i,0],time_array[i,1])
        dc=extract_death_coordinates(kbw)
        dp=transform_coordinates_map_to_pixels(dc)
        annotation = " " + str(time_array[i,0]) +"_"+ str(time_array[i,1])
        draw_deaths_on_map(MAP_PATH,dp,annotation)
    return

#main
draw_with_time(35,8)





















