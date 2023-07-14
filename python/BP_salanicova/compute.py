import numpy as np
from sklearn.cluster import DBSCAN


def y_root_route(climbers):
    """traversed route of climbers' root y coordinate

    :returns
    trajectory_a - array of frame, idclimber, trajectory of previous frames in m
    """

    # standardise wall of 15m
    trajectory_a = [np.zeros(len(climbers[0])), np.zeros(len(climbers[1]))]
    for j in range(2):
        pxpm = (np.max(climbers[j][:, :, 1]) - np.min(climbers[j][:, :, 1])) / 15
        for i in range(1, len(climbers[j])):
            b = (climbers[j][i - 1, 6, 1] - climbers[j][i, 6, 1])
            if b < 0:  # we dont want to count fall to the route as we compute then speed
                trj = 0
            else:
                trj = b
            trajectory_a[j][i] = trajectory_a[j][i - 1] + trj
        trajectory_a[j][:] /= pxpm

    return trajectory_a


def compute_speed(climbers, window=15, rate=50):
    """Speed of window frames track, for each frame.

    :parameter
    climbers
    window = size of sliding window
    rate = number of frames per second

    :returns
    speed - array of speeds to the current frame in seconds during window frames
    """

    trj = y_root_route(climbers)
    speed = [np.zeros(len(climbers[0])), np.zeros(len(climbers[1]))]
    half_window = window // 2
    for j in range(2):
        for i in range(half_window, len(climbers[j]) - half_window):
            track = trj[j][i + half_window] - trj[j][i - half_window]
            speed[j][i] = track / (window / rate)

    return speed


def sum_joint_cluster(clustering, sum_cl):
    """
    Summary of the delay during entire run for each end effector

    :return: sum_cluster - summary in seconds
    """
    sum_cluster = [np.zeros(4), np.zeros(4)]
    for d, cl in enumerate(clustering):
        for j in cl:
            for clust in j:
                (x, y), count, joint, _ = clust
                if count > 15:
                    sum_cluster[d][int(joint // 5)] += count
        sum_cluster[d] /= 50

    return sum_cluster


def delay_points(climbers):
    """Cluster of delay of end effectors. using DBSCAN


    :returns
    clustering - array of coordinates of point, size, id_joint for both climbers
    sum_clust - array of size of points ???
    """
    clustering = []
    clusters_frames = []
    # f_cl = climbers.copy()
    dbscan = DBSCAN(eps=0.8, min_samples=5, n_jobs=-1, metric="euclidean")
    sum_clust = []
    for c in range(2):
        meta_pole = []
        count = 0
        for j in [0, 5, 10, 15]:  # end effectors
            meta_meta_pole = []
            data = climbers[c][10:, j]  # all frames for given climber and given joint
            labels = dbscan.fit_predict(data)
            for clust in np.unique(labels):
                if clust == -1:
                    continue
                mask = labels == clust
                b = mask[::-1]
                last_frame_cluster = len(b) - np.argmax(b) - 1
                first_frame_cluster = np.argmax(mask)
                points_clust = climbers[c][10:, j][mask]
                avr = np.mean(points_clust, axis=0)
                meta_meta_pole.append((avr, len(points_clust), j, (first_frame_cluster, last_frame_cluster)))
                count += len(points_clust)
                if len(points_clust) > 15:
                    sum_clust.append(len(points_clust))

            meta_pole.append(meta_meta_pole)
        clustering.append(meta_pole)
    joint_sum = sum_joint_cluster(clustering, sum_clust)

    return clustering, sum_clust, joint_sum


def local_advantage(climbers):
    """
    Function counts number of frames (time) spend on the part of the wall. It computes difference in frames between
    climbers

    :return: array of signum function -1 -> less amount of frames of 0th climber
                                       1 -> -||- of 1st cl
                                       0 -> same amount of frames for the part of the wall
    """

    pxm0 = ((np.max(climbers[0][:, :, 1]) - np.min(climbers[0][:, :, 1])) / 15)
    pxm1 = ((np.max(climbers[1][:, :, 1]) - np.min(climbers[1][:, :, 1])) / 15)
    pxms = [pxm0, pxm1]
    local_frames = np.zeros(shape=(2, 15))

    for i in range(15, 0, -1):
        for j in range(2):
            bottom = i * pxms[j]
            top = (i - 1) * pxms[j]

            i1 = np.argmin(np.abs(climbers[j][:, 6, 1] - bottom))
            i2 = np.argmin(np.abs(climbers[j][:, 6, 1] - top))

            local_frames[j, 15 - i] = i2 - i1

    local_adv = list(map(lambda x, y: x - y, local_frames[0], local_frames[1]))

    return np.sign(local_adv)


def get_advantage_clm(climbers):
    """
    It computes difference in time advantage between climbers. Negative value means advantage of the 0th climber,
    positive of the 1st climber
    :param climbers:
    :return: array of time advantage differences.
    """
    clm1, clm2 = climbers[0], climbers[1]
    advantages = np.zeros(len(clm1))
    for i in range(min(len(clm1), len(clm2))):
        frame_i_height = clm1[i, 6, 1]

        # get mask with frames on which clm2 is higher then clm1 on ith frame
        mask = clm2[:, 6, 1] <= frame_i_height
        first_ind = np.argmax(mask) if not mask.all() else 0

        advantages[i] = i - first_ind

        # edge case undefined in the thesis
        if not mask.any():
            advantages[i] = 0

    return advantages


def trajectory(climbers, traj):
    """
    :param climbers:
    :return:
    """
    # standardise wall of 15m
    trajectory_a = [0, 0]
    for j in range(2):
        pxpmY = (np.max(climbers[j][:, :, 1]) - np.min(climbers[j][:, :, 1])) / 15  # maybe same per_px forbothclimbers
        pxpmX = (np.max(climbers[j][:, :, 0]) - np.min(climbers[j][:, :, 0])) / 3  # maybe same per_px forbothclimbers
        for i in range(1, len(climbers[j])):
            a = 100 * (abs(climbers[j][i, 6, 0] - climbers[j][i - 1, 6, 0])) / pxpmX
            b = 100 * (climbers[j][i - 1, 6, 1] - climbers[j][i, 6, 1]) / pxpmY
            trj = np.math.sqrt(a ** 2 + b ** 2)
            trajectory_a[j] += trj
        trajectory_a[j] /= 100

    if traj:
        print(f"Left climber time : {len(climbers[0]) / 50}s trajectory: {np.round(trajectory_a[0], 2)}m")
        print(f"Right climber time : {len(climbers[1]) / 50}s trajectory: {np.round(trajectory_a[1], 2)}m")

    return [len(climbers[0]) / 50, len(climbers[1]) / 50], trajectory_a
