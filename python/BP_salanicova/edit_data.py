import numpy as np


def scaling(climbers, shape):
    """
    maintain ratio of climbers skeletons in videos

    :return: edited_clms
    """
    width, height = shape[1], shape[0]
    # all videos are in this format
    oW, oH = 1080, 960
    rx, ry = width / oW, height / oH

    for i in range(2):
        climbers[i][:, :, 0] *= rx
        climbers[i][:, :, 1] *= ry

    return climbers


def normalise(climbers):
    """
    It normalise climbers between 1 and 0 for each climber, add the potential negative minimum,
    especially in case the np.abs(minimum) > max
    :param climbers:
    :return: normalised climbers
    """

    # uncommmented this part and commented the other one
    # if both climbers need to end at the same point, however, the camera movement is unrolled badly

    # for c in range(2):
    #     # climbers[c] += abs(np.min(climbers[c][:, :, 1]))
    #     max_, min_ = np.max(climbers[c][:, :, 1]), np.min(climbers[c][:, :, 1])
    #
    #     climbers[c][:, :, 0] = (climbers[c][:, :, 0] - min_) / (max_ - min_)
    #     climbers[c][:, :, 1] = (climbers[c][:, :, 1] - min_) / (max_ - min_)
    # return climbers

    max_0, min_0 = np.max(climbers[0][:, :, 1]), np.min(climbers[0][:, :, 1])
    max_1, min_1 = np.max(climbers[1][:, :, 1]), np.min(climbers[1][:, :, 1])
    max_, min_ = max(max_0, max_1), min(min_0, min_1)

    for c in range(2):
        climbers[c][:, :, 0] = (climbers[c][:, :, 0] - min_) / (max_ - min_)
        climbers[c][:, :, 1] = (climbers[c][:, :, 1] - min_) / (max_ - min_)

    return climbers


# TODO crop the edges for legends
def fit_to_graph(climbers, shape):
    """Edit data to fit to image accordingly.
    :parameter
    climbers
    shape - shape of image

    :returns
    edit_climbers
    """

    width, height = shape[1], shape[0]

    climbers = normalise(climbers)

    for c in range(2):
        climbers[c][:, :, 0] *= width * 0.9
        climbers[c][:, :, 1] *= height * 0.9

        climbers[c][:, :, 0] += (width * 0.1) // 2
        climbers[c][:, :, 0] += 50  # okraje pre legendu
        climbers[c][:, :, 0] -= 25
        climbers[c][:, :, 1] += (height * 0.1) // 2

    # shift to x coordinates
    avrg_x = (np.max(climbers[0][:, :, 0]) - np.min(climbers[0][:, :, 0])) / 2
    start_x = climbers[0][0, 6, 0] - avrg_x - width / 3.5
    #a = climbers[0][0, 6, 0] #PM debug
    # climbers[0][nth, pose, x or y coordinate]
    climbers[0][:, :, 0] -= start_x
    #b = climbers[0][:, :, 0] #PM debug

    avrg_x1 = (np.max(climbers[1][:, :, 0]) - np.min(climbers[1][:, :, 0])) / 2
    start_x1 = climbers[1][0, 6, 0] - avrg_x1 - 3 * width / 4
    #cc = climbers[1][:, :, 0] #PM debug
    #d = np.min(climbers[1][:, :, 0]) #PM debug
    climbers[1][:, :, 0] -= start_x1

    return climbers


def insert_frame(climbers):
    """Very easy way of supersampling DATA. Between each frame of data is computed "half-frame"

    :returns
    in_clms - len(array2) = 2*len(array), doubled in size
    """

    in_clms = [np.zeros(((2 * len(climbers[c])) - 1, 16, 2)) for c in range(2)]
    for c in range(2):
        in_clms[c][list(range(0, len(in_clms[c]), 2))] = climbers[c]
        for i in range(1, len(in_clms[c]) - 1, 2):
            in_clms[c][i] = (in_clms[c][i - 1] + in_clms[c][i + 1]) / 2
    return in_clms


def synchronised_video_climber(climbers, desired_len=None):
    """ Synchronised videos aligned by same height with the climbers on a reference wall

        :returns
        in_clms - synchronised climbers with videos, aligned by height
    """

    addor = desired_len / max(len(climbers[0]), len(climbers[1]))
    in_clms = [np.zeros((int(len(climbers[c]) * addor), 16, 2)) for c in
               range(2)]  # (len(climbers[c])//evevr_frmae[c]+len(climbers[c])) - 1

    addor -= 1e-5
    for c in range(2):

        acc = 0
        last_ind = -1
        for i in range(len(climbers[c])):
            acc += addor
            curr_ind = int(acc)

            if curr_ind >= len(in_clms[c]):
                continue
            in_clms[c][curr_ind] = climbers[c][i]

            if curr_ind != last_ind + 1:
                assert curr_ind == last_ind + 2
                in_clms[c][curr_ind - 1] = (climbers[c][i - 1] + climbers[c][min(i, len(climbers[c]))]) / 2
            last_ind = curr_ind
    return in_clms


def aligning_by_height_indices(climbers, tolerance=1):
    """It freezes the faster one: matching video frames by height
     The faster climber waits for the slower one amount of frames necessary to catch up.
     According to same height not time

    :returns
    index_clms - array of indices for aligned frames
    """
    index_clms = [[], []]
    i, j = 5, 5

    while i <= len(climbers[0]) or j <= len(climbers[1]):
        _, root_y1 = climbers[0][min(len(climbers[0]) - 1, i), 6]
        _, root_y2 = climbers[1][min(len(climbers[1]) - 1, j), 6]

        index_clms[0].append(min(i, len(climbers[0]) - 1))
        index_clms[1].append(min(j, len(climbers[1]) - 1))
        if root_y1 > root_y2 and abs(root_y1 - root_y2) > tolerance and i < len(climbers[0]):
            i += 1
        elif root_y1 < root_y2 and abs(root_y2 - root_y1) > tolerance and j < len(climbers[1]):
            j += 1
        else:
            i += 1
            j += 1

    return index_clms
