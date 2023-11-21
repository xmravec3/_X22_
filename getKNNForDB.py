import mysql.connector
import dtw
import json
import sys

def get_angles(data_string):
    """
    Get angles from string to float.

    :param data_string: variable contains string array
    :return: list of angles
    """
    angles = []
    for line in data_string.split('\n'):
        if line == '':
            continue
        array_string =line.split(' ')
        angles.append(list(map(float, array_string)))

    return angles

knn_id = sys.argv[1]

try:
    connection = mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="root",
        database="eso"
    )

    # get video for KNN with specific ID (knn_id)
    sql_select_one_Query = "SELECT ID, angles FROM video where ID=%s"
    cursor = connection.cursor()
    cursor.execute(sql_select_one_Query, (knn_id,))
    selected_video = cursor.fetchall()[0]

    # get all videos
    #sql_select_other_Query = "select v.ID, v.title, v.video_name, v.climber_id, c.`name` as climber_name, v.`date`, v.attempt, v.`time`, v.angles from video AS v inner join climber AS c on v.climber_id = c.ID order by v.ID asc"
    
    # get videos without specific ID (knn_id)
    sql_select_other_Query = "select v.ID, v.title, v.video_name, v.climber_id, c.`name` as climber_name, v.`date`, v.attempt, v.`time`, v.angles from video AS v inner join climber AS c on v.climber_id = c.ID where v.ID != %s order by v.ID asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_other_Query, (knn_id,))
    videos = cursor.fetchall()

    query = get_angles(selected_video[1])
    distance = []

    for video in videos:
        reference = get_angles(video[8])
        alignment = dtw.dtw(query, reference, distance_only=True)
        distance.append((video, alignment.normalizedDistance))

    distance.sort(key=lambda x : x[1])

    result = []
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
