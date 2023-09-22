import BP_salanicova.file_work as fw
import BP_salanicova.edit_data as ed
import BP_salanicova.compute as cp
import json
import numpy as np
import sys

import mysql.connector


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# 8_2019-08-17_1 -> ID 75
# 25_2019-08-17_1 -> ID 74
if __name__ == "__main__":
    l_ID = sys.argv[1]
    r_ID = sys.argv[2]
    #l_ID = 75
    #r_ID = 74

    try:
        connection = mysql.connector.connect(
            host="mysql_db",
            user="root",
            password="root",
            database="eso"
        )

        sql_select_one_Query = "SELECT ID, skeletons, trans_matrixes FROM video where ID=%s"
        cursor = connection.cursor()
        cursor.execute(sql_select_one_Query, (l_ID,))
        # get video for KNN
        l_raw_data = cursor.fetchall()[0]

        sql_select_one_Query = "SELECT ID, skeletons, trans_matrixes FROM video where ID=%s"
        cursor = connection.cursor()
        cursor.execute(sql_select_one_Query, (r_ID,))
        # get video for KNN
        r_raw_data = cursor.fetchall()[0]

    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()

    #shape = (600, 1200)
    shape = (480, 360) # used as it was in BP from Salanicova

    # loads relative data and unroll the camera movement
    rel_climbers = fw.load_data_PM(l_raw_data[1], r_raw_data[1]) # - it is loading skeletons into an array
    #print(rel_climbers)
    ##matches = ['8_2019-08-17_1', '25_2019-08-17_1']
    ##un_file0, un_file1 = f"unpacked_data/{matches[0]}.data", f"unpacked_data/{matches[1]}.data" # BP SALANICOVA
    # loads relative data and unroll the camera movement
    ##rel_climbers = fw.load_data(un_file0, un_file1) # - it is loading skeletons into an array

        # Relevant data for gpraph!!!!!!
    clms = fw.load_matrices_PM([l_raw_data[2], r_raw_data[2]], rel_climbers.copy())   # - it is loading matrixes and multiply them into virtual refference wall
    
    clms_insert = ed.insert_frame(clms) # it is double the length
    climbers = ed.fit_to_graph(clms_insert, shape)   # needed information for graph

    # CODE RELEVANT FOR DELAY DATA
    climbers_d = climbers
    clusters, _, _ = cp.delay_points(climbers_d)
    #print(clusters)

    joint_description = {0: 'lFoot', 1: 'lKnee', 2: 'lHip', 3: 'rHip', 4: 'rKnee', 5: 'rFoot', 6: 'root', 7: 'thorax',
                         8: 'neck', 9: 'head', 10: 'lHand', 11: 'lElbow', 12: 'lShoulder', 13: 'rShoulder',
                         14: 'rElbow', 15: 'rHand'}
    
    delay_points = []

    for i in range(len(clusters)):
            for joints in clusters[i]:
                for point in joints:
                    coor, count, joint, (first_f, last_f) = point
                    if count > 15:
                        delay_points.append({'position': i, 'body_part': joint_description[joint], 'X': np.round(coor[0], 2),
                                           'Y': np.round(coor[1], 2), 'time': count / 50})
                        #d = f"{i},{joint_description[joint]},{(first_f, last_f)},{np.round(coor[0], 2)},{np.round(coor[1], 2)},{count / 50}\n"
    #print(delay_points)

    
    
    # PRINT RESULT - RETURN IT FOR NODEJS
    
    #json_result = json.dumps(climbers, cls=NpEncoder)
    #json_result = json.dumps([{'result': climbers}], cls=NpEncoder) WORKING BEFORE DELAY_DATA

    # data needed for Y-axis chart draw
    index = 0 if len(climbers[0]) < len(climbers[1]) else 1
    h1, h2 = int(np.min(climbers[index][:, :, 1])), int(np.max(climbers[index][:, :, 1]))

    # get data for speed and advantage
    speed = cp.compute_speed(climbers=climbers.copy(), window=25, rate=50)
    speed_diff = list(map(lambda x, y: y - x, speed[0], speed[1]))
    indc_diff = cp.get_advantage_clm(climbers)
    local_adv = cp.local_advantage(climbers)

    json_result = json.dumps([{'result': climbers, 'delay_data': delay_points, 'speed_diff': speed_diff, 'indc_diff': indc_diff, 'local_adv': local_adv, 'min_y': h1, 'max_y': h2}], cls=NpEncoder) 
    #json_result = [{'result': climbers, 'delay_data': delay_points}]

    print(json_result)
    
    #print(l_raw_data)
    #exit
            
## OWN CODE FOR PROCESSING

    # 8_2019-08-17_1 -> ID: 75
    # 25_2019-08-17_1 -> ID: 74
    #matches = [75, 74]
    #shape = (800, 1000)


    #  finds files
    #un_file0, un_file1 = f"unpacked_data/{matches[0]}.data", f"unpacked_data/{matches[1]}.data" # BP SALANICOVA
    #print(un_file0)

    # loads relative data and unroll the camera movement
    #rel_climbers = fw.load_data(un_file0, un_file1) # - it is loading skeletons into an array

    # Relevant data for graph!!!!!!
    #clms = fw.load_matrices(matches, rel_climbers.copy())   # - it is loading matrixes and multiply them into virtual refference wall
    #clms_insert = ed.insert_frame(clms) # it is double the length
    #climbers = ed.fit_to_graph(clms_insert, shape)   # needed information for graph
    #print(climbers)

    #json_result = json.dumps(climbers, cls=NpEncoder)
    #print(json_result)

    #print("HELLO")

    # GET DELAY POINTS
    #climbers_d = climbers
    #delayData = cp.delay_points(climbers_d)
    #print(delayData)










