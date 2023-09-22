import mysql.connector
import dtw
import json
import sys

from math import acos, pow, sqrt


def get_joints_coordinates(data_string):
    """
    Get the joint coordinates from given file.

    :param file_name: file to read from
    :return: list of joint coordinates
    """
    joints = []

    for line in data_string.split('\n'):
        if line == '':
            continue
        line = line.split('#')[1]
        #if line == "\n":
        #    continue
        if line.strip() == "NULL":
            joints.append(None)
        else:
            joints.append(line.split(';'))

    return joints

def process_angles(joints):
    """
    Compute angles from joint coordinates.
    """
    angles = []
    for i in range(len(joints)):
        angles.append(compute_angles(joints[i]))
    return angles

def compute_angles(joints):
    """
    Take the coordinates and compute angles.

    :param joints: joint coordinates
    :return: angles from the coordinates
    """
    if joints == None:
        return None

    vector = []

    joint_coord = []

    for joint in joints:
        coords = joint.split(',')
        joint_coord.append((float(coords[0]), float(coords[1])))

    l_elbow = compute_one_angle(joint_coord[11], joint_coord[10], joint_coord[12])
    vector.append(l_elbow)

    r_elbow = compute_one_angle(joint_coord[14], joint_coord[15], joint_coord[13])
    vector.append(r_elbow)

    l_shoulder = compute_one_angle(joint_coord[12], joint_coord[7], joint_coord[11])
    vector.append(l_shoulder)

    r_shoulder = compute_one_angle(joint_coord[13], joint_coord[14], joint_coord[7])
    vector.append(r_shoulder)

    l_leg = compute_one_angle(joint_coord[2], joint_coord[6], joint_coord[1])
    vector.append(l_leg)

    r_leg = compute_one_angle(joint_coord[3], joint_coord[4], joint_coord[6])
    vector.append(r_leg)

    l_knee = compute_one_angle(joint_coord[1], joint_coord[2], joint_coord[0])
    vector.append(l_knee)

    r_knee = compute_one_angle(joint_coord[4], joint_coord[5], joint_coord[3])
    vector.append(r_knee)

    l_armp = compute_one_angle(joint_coord[7], joint_coord[6], joint_coord[12])
    vector.append(l_armp)

    r_armp = compute_one_angle(joint_coord[7], joint_coord[13], joint_coord[6])
    vector.append(r_armp)

    l_hip = compute_one_angle(joint_coord[6], joint_coord[2], joint_coord[7])
    vector.append(l_hip)

    r_hip = compute_one_angle(joint_coord[6], joint_coord[3], joint_coord[7])
    vector.append(r_hip)

    torso = compute_one_angle(joint_coord[7], joint_coord[6], joint_coord[8])
    vector.append(torso)

    return vector

def compute_one_angle(a, b, c):
    """
    Given points of a triangle a, b, c, compute angle alpha.
    """
    side_a = point_distance(b, c)
    side_b = point_distance(a, c)
    side_c = point_distance(a, b)

    nominator = pow(side_a,2) - pow(side_b,2) - pow(side_c,2)
    denominator = -2 * side_b * side_c

    if denominator == 0:
        return 0
    if nominator / denominator > 1:
        return acos(1)
    if nominator / denominator < -1:
        return acos(-1)

    return acos(nominator / denominator)

def point_distance(a, b):
    """
    Compute Euclidean distance for a and b.
    """
    dist_x = float(b[0]) - float(a[0])
    dist_y = float(b[1]) - float(a[1])
    return sqrt((pow(dist_x,2)) + (pow(dist_y,2)))





# *********************************
knn_id = sys.argv[1]
#knn_id = 2

try:
    connection = mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="root",
        database="eso"
    )

    sql_select_one_Query = "SELECT ID, skeletons FROM video where ID=%s"
    cursor = connection.cursor()
    cursor.execute(sql_select_one_Query, (knn_id,))
    # get video for KNN
    video = cursor.fetchall()[0]

    

    sql_select_other_Query = "select v.ID, v.title, v.video_name, v.climber_id, c.`name` as climber_name, v.`date`, v.attempt, v.`time`, v.skeletons from video AS v inner join climber AS c on v.climber_id = c.ID order by v.ID asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_other_Query)
    # get videos for KNN
    videos = cursor.fetchall()

    #print(len(videos))

    # run KNN search for video in videos

    joints1 = get_joints_coordinates(video[1])
    #print(joints1)

    distance = []

    for file2 in videos:

        joints2 = get_joints_coordinates(file2[8])

        query = process_angles(joints1)
        reference = process_angles(joints2)


        alignment = dtw.dtw(query, reference, distance_only=True)

        distance.append((file2, alignment.normalizedDistance))

    # sort
    distance.sort(key=lambda x : x[1])

    result = []
    # print to get in NODEJS
    for item in distance:
        result.append({'ID': item[0][0], 'dist': item[1], 'title': item[0][1], 'climber_id': item[0][3], 'climber_name': item[0][4], 'attempt': item[0][6], 'time': item[0][7], 'date': str(item[0][5]), 'video_path': item[0][2]})

    json_result = json.dumps(result)
    print(json_result)



#except mysql.connector.Error as e:
    #print("Error reading data from MySQL table", e) throw an error, no print!
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        #print("MySQL connection is closed")
