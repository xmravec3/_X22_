import sys
import BP_salanicova.compute as cp # modified to imported
import numpy as np
import cv2
import os
import io # PM


def load_video(filenames, target_dim=None):
    """Loading videos to target dimension

    filenames :parameter array of two video paths
    target_dim - size of one videoframe

    :returns
    np.array of videoframes
    """
    fpss = []
    video_climbers = []
    try:
        for video_file in filenames:
            video_climber = []
            video_file = "C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/" + video_file  # added PM
            cap = cv2.VideoCapture(video_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            fpss.append(fps)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if target_dim is not None:
                    frame = cv2.resize(frame, target_dim, interpolation=cv2.INTER_AREA)
                video_climber.append(frame)
                video_climber.append(frame)
            video_climbers.append(video_climber)
        if len(filenames) > 1:
            len0 = len(video_climbers[0])
            len1 = len(video_climbers[1])
            if len0 > len1:
                for _ in range(len0 - len1):
                    video_climbers[1].append(video_climbers[1][len1 - 1])
            else:
                for _ in range(len1 - len0):
                    video_climbers[0].append(video_climbers[0][len0 - 1])
    except IOError as e:
        print(e)
        sys.exit(1)
    try:
        assert fpss[0] == fpss[1]
    except AssertionError as e:
        print("Different framerate")
        sys.exit(1)
    return np.array(video_climbers).swapaxes(0, 1)


def load_data(file0, file1):
    """"Two files are loaded and merge to one match
     :parameter
     file0 - 0id climber
     file1 - 1id climber

     :returns
     climbers - np.array of climbers data: id_climber, number of frame, id_joint, xcoord, ycoord
     """

    try:
        with open(file0) as f0, open(file1) as f1:
            lines0 = f0.readlines()
            lines1 = f1.readlines()
    except IOError as e:
        print(e)
        sys.exit(1)

    lines = [lines0, lines1]
    n_frames0 = int(max(lines0, key=lambda x: int(x.split(",")[0])).split(",")[0])
    n_frames1 = int(max(lines1, key=lambda x: int(x.split(",")[0])).split(",")[0])
    climber0 = np.zeros(shape=(n_frames0, 16, 2), dtype=float)
    climber1 = np.zeros(shape=(n_frames1, 16, 2), dtype=float)
    climbers = [climber0, climber1]
    for c in range(2):
        for frame in lines[c]:
            splitted = frame.split('#')
            fr, id_ = splitted[0].split(',')[:2]
            if len(splitted[1]) > 1:
                joints = [cord.split(',') for cord in splitted[1].split(';')]
                climbers[c][int(fr) - 1] = joints
    return climbers

## UPDATED Peter Mravec - get data from DB not from file folders
def load_data_PM(lines0, lines1):
    """"Two files are loaded and merge to one match
     :parameter
     lines0 - 0id climber skeleton data
     lines1 - 1id climber skeleton data

     :returns
     climbers - np.array of climbers data: id_climber, number of frame, id_joint, xcoord, ycoord
     """

    lines0 = lines0.replace('#', ',0#') #PM
    lines1 = lines1.replace('#', ',0#') #PM
    lines0 = lines0.split('\n')[:-2]
    lines1 = lines1.split('\n')[:-2]
    lines = [lines0, lines1]

    n_frames0 = int(max(lines0, key=lambda x: int(x.split(",")[0])).split(",")[0])
    n_frames1 = int(max(lines1, key=lambda x: int(x.split(",")[0])).split(",")[0])
    climber0 = np.zeros(shape=(n_frames0, 16, 2), dtype=float)
    climber1 = np.zeros(shape=(n_frames1, 16, 2), dtype=float)
    climbers = [climber0, climber1]
    for c in range(2):
        for frame in lines[c]:
            splitted = frame.split('#')
            fr, id_ = splitted[0].split(',')[:2]
            if len(splitted[1]) > 1:
                joints = [cord.split(',') for cord in splitted[1].split(';')]
                climbers[c][int(fr) - 1] = joints
    return climbers


def write_graph(name, delay_points, speed, advantage, climbers):
    """Writing in file the output digital data

    :returns
    """
    joint_description = {0: 'lFoot', 1: 'lKnee', 2: 'lHip', 3: 'rHip', 4: 'rKnee', 5: 'rFoot', 6: 'root', 7: 'thorax',
                         8: 'neck', 9: 'head', 10: 'lHand', 11: 'lElbow', 12: 'lShoulder', 13: 'rShoulder',
                         14: 'rElbow', 15: 'rHand'}
    id0, id1 = name.split(';')
    ids = [id0, id1]

    speed = list(map(lambda a, b: b - a, speed[0], speed[1]))

    clusters, _ , _= delay_points
    #with open(f"out_data/{name}_delay_data.txt", "w") as out_file:
    with open(f"C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/out_data/{name}_delay_data.txt", "w") as out_file:
    #C:\GIT\diplom\SalanicovaBP\SBAPR\out_data\BP_8_2019-08-17_1;25_2019-08-17_1_delay_data.txt
        for i in range(len(clusters)):
            for joints in clusters[i]:
                for point in joints:
                    coor, count, joint, (first_f, last_f) = point
                    if count > 15:
                        d = f"{ids[i].split('_')[0]},{joint_description[joint]},{(first_f, last_f)},{np.round(coor[0], 2)},{np.round(coor[1], 2)},{count / 50}\n"
                        out_file.write(d)
                    # print(d)
    out_file.close()

    h1 = int(min(np.min(climbers[0][:, :, 1]), np.min(climbers[1][:, :, 1])))
    h2 = int(max(np.max(climbers[0][:, :, 1]), np.max(climbers[1][:, :, 1])))
    # height legend
    meter = (h2 - h1) / 15

    try:
        with open(f"out_data/{name}_graph_data.txt", "w") as outfile:
            for i in range(0, min(len(climbers[0]), len(climbers[1])) - 5):
                # 50 -> frame rate
                string = f"{np.round((climbers[0][i + 5, 6, 1]), 2)},{(advantage[1][i] - advantage[0][i]) / 50}," \
                         f"{np.round(speed[i], 2)} "
                outfile.write(f"{string}\n")
        outfile.close()
    except IOError:
        print("Transformation matrix for matches was not find.")


def create_video(images, name, rate):
    """
    From given images creates a video

    :param images:
    :param name:
    :param rate:

    """
    #image_folder = 'images'
    image_folder = 'C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/images'   # PM changes
    video_name = f'C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/outputs/{name}.avi'  # 'f'{images[0][:5]}.avi'

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # video = cv2.VideoWriter('video.avi', fourcc, 1, (width, height))

    video = cv2.VideoWriter(video_name, fourcc, rate, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    for i in range(rate):
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def write_images(images, name):
    """Writes images as np.array as .jpg"""
    names_imgs = []
    for i in range(len(images)):
        image = images[i]
        #cv2.imwrite(f"images/{name}{i + 1}.jpg", image)
        cv2.imwrite(f"C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/images/{name}{i + 1}.jpg", image)  #PM changes
        names_imgs.append(f"{name}{i + 1}.jpg")
    return names_imgs


def load_matrices(matches, climbers):
    """
    Load matrices and computes the unrolling.
    :param matches:
    :param climbers:
    :return:
    """

    try:
        #trans_matrices = [np.loadtxt(f'cut_out/{matches[0]}.mp4.txt.gz').reshape((-1, 3, 3)),
        #                  np.loadtxt(f'cut_out/{matches[1]}.mp4.txt.gz').reshape((-1, 3, 3))]
        trans_matrices = [np.loadtxt(f'C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/cut_out/{matches[0]}.mp4.txt.gz').reshape((-1, 3, 3)),
                          np.loadtxt(f'C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/cut_out/{matches[1]}.mp4.txt.gz').reshape((-1, 3, 3))]
    except IOError as e:
        print(e)
        sys.exit(1)

    delta_y = [trans_matrices[0][:, 1, 2], trans_matrices[1][:, 1, 2]]
    for j in range(len(delta_y)):
        for i in range(len(delta_y[j]) - 1):
            for joint in range(16):
                climbers[j][i, joint] = (trans_matrices[j][i, :2, :2] @ climbers[j][i, joint])+trans_matrices[j][i, :2, 2]
    return climbers

## UPDATED Peter Mravec - get data from DB not from file folders
def load_matrices_PM(trans_matrixes_read, climbers):
    """
    Load matrices and computes the unrolling.
    :param trans_matrixes_read:
    :param climbers:
    :return:
    """

    l_trans_matrix_file = io.StringIO(trans_matrixes_read[0]) # possible issue with last item \n
    r_trans_matrix_file = io.StringIO(trans_matrixes_read[1])
    trans_matrices = [ np.loadtxt(l_trans_matrix_file).reshape((-1, 3, 3)), 
                      np.loadtxt(r_trans_matrix_file).reshape((-1, 3, 3)) ]


    delta_y = [trans_matrices[0][:, 1, 2], trans_matrices[1][:, 1, 2]]
    for j in range(len(delta_y)):
        for i in range(len(delta_y[j]) - 1):
            for joint in range(16):
                climbers[j][i, joint] = (trans_matrices[j][i, :2, :2] @ climbers[j][i, joint])+trans_matrices[j][i, :2, 2]
    return climbers


def write_trajectory(file, climbers, trj):
    """
    Writes into file korelacia.txt
    25_2019-08-17_1 - time 6.136 319 50 49 - 6.38 6.51
    8_2019-08-17_1  - time 6.441 305 50 49 - 6.1 6.22
      Length of trajectories and climbers'time are written
      :return:
      """
    times, trjs = cp.trajectory(climbers, trj)
    trjs = np.round(trjs, 2)
    try:
        with open(file, "a") as out_f:
            string = f"{times[0]},{times[1]},{trjs[0]},{trjs[1]}\n"
            out_f.write(string)
        out_f.close()
    except IOError as e:
        print(e)


def write_matching_video(indc_v, name):
    """
    Indices aligning video frames by height are written

    :return:
    """
    with open(f"out_data/{name}_matching.txt", "w") as f:
        for i in range(len(indc_v[0])):
            string = f"{indc_v[0][i]},{indc_v[1][i]}\n"
            f.write(string)
    f.close()