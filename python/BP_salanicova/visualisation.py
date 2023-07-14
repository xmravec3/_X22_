import cv2
import numpy as np
import sys
import file_work as fw
import edit_data as ed
import compute as cp

# JOINTS DESCRIPTION 0-lFoot 1-lKnee 2-lHip 3-rHip 4-rKnee 5-rFoot 6-root 7-thorax 8-neck 9-head 10-lHand 11-lElbow
# 12-lShoulder 13-rShoulder 14-rElbow 15-rHand
BONES = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [2, 6], [3, 6], [6, 7], [7, 8], [8, 9], [7, 12], [7, 13], [10, 11],
         [11, 12], [13, 14], [14, 15]]


class Canvas:
    """Grid of image """

    def __init__(self, shape, videa_only=None, stop=None, graph_only=None, envp=None):
        self.w0, self.w1, self.w2, self.w3 = 0, 35, 65, 100
        self.h0, self.h1, self.h2, self.h3 = 0, 5, 85, 100

        self.shape = shape
        # height and width of whole drawing area in percent
        self.h, self.w = np.array(shape) // 100
        self.envp = envp
        self.stop = stop
        # self.videos = fw.load_video(videos, (self.video_left.shape[1], self.video_left.shape[0]))
        self.full = self.blank()
        # self.video_left, self.video_right = None, None
        # self.metrics, self.graph = None, None

        self.graph_only, self.videa_only = graph_only, videa_only

    @property
    def video_left(self):
        return self.full[self.h1 * self.h:self.h2 * self.h, self.w0 * self.w:self.w1 * self.w]

    @property
    def video_right(self):
        return self.full[self.h1 * self.h:self.h2 * self.h, self.w2 * self.w:self.w3 * self.w]

    @property
    def graph(self):
        return self.full[self.h1 * self.h:self.h2 * self.h, self.w1 * self.w:self.w2 * self.w]

    @property
    def metrics(self):
        return self.full[self.h2 * self.h:self.h3 * self.h, self.w0 * self.w:self.w3 * self.w]

    @property
    def legend_up(self):
        return self.full[self.h0 * self.h:self.h1 * self.h, self.w1 * self.w:self.w2 * self.w]

    @video_left.setter
    def video_left(self, val):
        self.full[self.h1 * self.h:self.h2 * self.h, self.w0 * self.w:self.w1 * self.w] = val

    @video_right.setter
    def video_right(self, val):
        self.full[self.h1 * self.h:self.h2 * self.h, self.w2 * self.w:self.w3 * self.w] = val

    @graph.setter
    def graph(self, val):
        self.full[self.h1 * self.h:self.h2 * self.h, self.w1 * self.w:self.w2 * self.w] = val

    @metrics.setter
    def metrics(self, val):
        self.full[self.h2 * self.h:self.h3 * self.h, self.w0 * self.w:self.w3 * self.w] = val

    @legend_up.setter
    def legend_up(self, val):
        self.full[self.h0 * self.h:self.h1 * self.h, self.w1 * self.w:self.w2 * self.w] = val

    def blank(self):
        """creates blank white canvas"""
        full = np.zeros(shape=(*self.shape, 3), dtype=np.uint8) + 255
        return full


def draw_climber(image, frame, color=(0, 131, 255), blur=False, thick=1, v=False):
    """
    draw a (bluring) skeleton of climber to a given image
    different colours and thickens of their body possible
    return drew image

    :parameter
    image - drawing area
    frame - information about a climber at given frame
    color - colour of joints
    blur - blur footprint
    thick - thickness of bone when bluring
    v - larger size of joint
    """

    w = 5 if v else 1
    for bone in BONES:
        pt1, pt2 = bone
        colour = (184, 183, 242)  # edit color blur or climber's
        # colour = (0, 0, 0)  # e/dit color blur or climber's

        x1, y1 = frame[pt1]
        x2, y2 = frame[pt2]
        x1 = np.round(x1).astype(int)
        x2 = np.round(x2).astype(int)
        y1 = np.round(y1).astype(int)
        y2 = np.round(y2).astype(int)

        if not blur:
            cv2.circle(image, (x1, y1), w, colour)
            cv2.circle(image, (x2, y2), w, colour)
            cv2.line(image, (x1, y1), (x2, y2), color, thickness=thick)
        else:
            overlay = image.copy()
            alpha = 0.1  # Transparency factor.
            # Following line overlays transparent rectangle over the image
            cv2.line(overlay, (x1, y1), (x2, y2), color=colour, thickness=thick)
            image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
            image = image_new

    return image


def draw_trajectory(image, climbers, time_mark):
    """
    Draw trajectory of root to the time_mark frame
    :param climbers:
    :param time_mark:
    :param image:
    :return: image
   """
    grey = (210, 210, 210)
    for j in range(len(climbers)):
        for i in range(5, time_mark[j]):
            rootx0, rooty0 = climbers[j][i, 6]
            rootx1, rooty1 = climbers[j][i - 1, 6]
            cv2.line(image, (int(rootx0), int(rooty0)), (int(rootx1), int(rooty1)), color=grey, thickness=1)

    return image



def pts_poly(array_y, x_cord, W, H, coef):
    """Creates array of polygon points for cv2 drawing
    :parameter
    array_y = y coordinates of polygon
    x-cord  = x coordinates of polygon
    W, H - width, height of image
    coef - coeficient of enlarging polygon

    :returns
    pts - points of polygon
    """
    # print(x_cord)
    pts = []
    i = 0
    for h in array_y:
        pts.append([W // 2 + x_cord[i] * coef, h])
        i += 1
    pts.append([W // 2, np.min(array_y)])
    pts.append([W // 2, np.max(array_y)])
    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1, 1, 2))

    return pts


def print_inner_graph(image, coor_y, coor_x, coef=1, color=(0, 0, 0), alpha=0.6):
    H, W, _ = image.shape
    pts_faster = pts_poly(coor_y[:], coor_x, W, H, coef)
    overlay = image.copy()
    cv2.polylines(image, [pts_faster], False, color)
    cv2.fillPoly(image, pts=[pts_faster], color=color)
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    return image_new


def print_local_advantage(image, loc_adv, height, widths, meter):
    """
    On y-axes it colorfully higlighted the local advantages... how long it takes climber to climb the one meter.
    :param widths:
    :param image:
    :param loc_adv:
    :param height:
    :param meter:
    :return:
    """
    w1, w2 = widths
    black = (0, 0, 0)
    red = (51, 51, 255)
    green = (102, 255, 102)
    if loc_adv == -1:
        color0, color1 = green, red
    elif loc_adv == 1:
        color0, color1 = red, green
    else:
        color0, color1 = black, black

    alpha = 0.5
    overlay = image.copy()
    cv2.rectangle(image, (w1 - 1, height), (w1 + 1, meter), color=color0, thickness=-1)
    cv2.rectangle(image, (w2 - 1, height), (w2 + 1, meter), color=color1, thickness=-1)
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    return image_new


def print_axis(image, widths, heights, colorad, colorsp):
    h1, h2 = heights
    w1, w2 = widths
    black = (0, 0, 0)
    cv2.line(image, (w1, h1), (w2, h1), color=colorad, thickness=1)
    cv2.line(image, (w1, h2), (w2, h2), color=colorsp, thickness=1)
    cv2.line(image, (w1, 0), (w1, image.shape[0]), color=black, thickness=1)
    cv2.line(image, (w2, 0), (w2, image.shape[0]), color=black, thickness=1)


def print_height_legend(climbers, image, heights, widths, index):
    h1, h2 = heights
    w1, w2 = widths
    local_adv = cp.local_advantage(climbers)
    black = (0, 0, 0)
    meter = (h2 - h1) / 15
    for i in range(15 + 1):
        cf, thick, fs = 3, 1, 0.38
        h = int(np.max(climbers[0][:, :, 1]) - meter * i)
        if 0 <= i < 15:
            image = print_local_advantage(image, local_adv[i], h, (w1, w2),
                                          int(np.max(climbers[index][:, :, 1]) - meter * (i + 1)))
        if i % 5 == 0:
            cf = 5
            cv2.putText(image, f"{i}", (w1 - 20, h + 2), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=fs, thickness=1,
                        color=black)
            cv2.putText(image, f"{i}", (w2 + 8, h + 2), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=fs, thickness=1,
                        color=black)

        cv2.line(image, (w1 - cf, h), (w1 + cf, h), color=black, thickness=thick)
        cv2.line(image, (w2 - cf, h), (w2 + cf, h), color=black, thickness=thick)

    return image

# TODO colours of legend
def print_graph(image, climbers, rate=25, colorsp=(153, 138, 72), colorad=(96, 122, 244), colors=None):
    """displays information about difference in between speeds/advantage of climbers at given height
    :parameter
    image - area of drawing
    climbers - normalised climbers data according to given image

    :returns
    image
    """
    H, W, _ = image.shape
    index = 0 if len(climbers[0]) < len(climbers[1]) else 1
    w1, w2 = 50, W - 25
    h1, h2 = int(np.min(climbers[index][:, :, 1])), int(np.max(climbers[index][:, :, 1]))
    array_y = climbers[index][:, 6, 1]

    speed = cp.compute_speed(climbers=climbers.copy(), window=25, rate=rate)
    speed_diff = list(map(lambda x, y: y - x, speed[0], speed[1]))
    indc_diff = cp.get_advantage_clm(climbers)

    # height legend
    print_axis(image, (w1, w2), (h1, h2), colorad, colorsp)
    image = print_height_legend(climbers, image, (h1, h2), (w1, w2), index)

    # print chart
    image_new = print_inner_graph(image, array_y, indc_diff, 1, colorad, alpha=0.55)
    image_new = print_inner_graph(image_new, array_y, speed_diff, 10, colorsp, alpha=0.6)

    # width legend time
    for s in range(5):
        cv2.line(image_new, (int(W // 2 + s * 10), h2 + 5), (int(W // 2 + s * 10), h2 - 5), color=colorsp, thickness=1)
        cv2.line(image_new, (int(W // 2 + (-s) * 10), h2 + 5), (int(W // 2 + (-s) * 10), h2 - 5), color=colorsp,
                 thickness=1)
        if s % 2 == 0:
            cv2.putText(image_new, f"{s}", (W // 2 + s * 10, h2 + 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.35, thickness=1,
                        color=colorsp)
            cv2.putText(image_new, f"{s}", (W // 2 - s * 10, h2 + 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.35,
                        thickness=1,
                        color=colorsp)

    # width legend advantage
    for a in range(0, 7, 3):
        cv2.line(image_new, (int(W // 2 + a * 10), h1 + 5), (int(W // 2 + a * 10), h1 - 5), color=colorad, thickness=1)
        cv2.line(image_new, (int(W // 2 + (-a) * 10), h1 + 5), (int(W // 2 + (-a) * 10), h1 - 5), color=colorad,
                 thickness=1)
        cv2.putText(image_new, f"{round(a / 6, 2)}", (W // 2 + a * 10, h1 - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.35,
                    thickness=1,
                    color=colorad)
        cv2.putText(image_new, f"{round(a / 6, 2)}", (W // 2 - a * 10, h1 - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.35,
                    thickness=1,
                    color=colorad)

    cv2.putText(image_new, f"s", (w2 - 15, h1 - 5), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, thickness=1,
                color=colorad)
    cv2.putText(image_new, f"m/s", (w2 - 30, h2 + 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.35, thickness=1,
                color=colorsp)

    print_delay_points(image_new, climbers, colors)

    return image_new


def print_delay_points(image, climbers, colors=None):
    """"It displays points of climber's joint delay.
    End effectors as hand and feet are differentiated in colours. A size of point shows time of delay.
    :parameter
    image - area of drawing
    climbers - normalised climbers data according to given image

    :returns
    image
    """
    cltr, sum_cluster, _ = cp.delay_points(climbers)
    limit = 15  # heuristic

    # JOINTS DESCRIPTION 0-lFoot 1-lKnee 2-lHip 3-rHip 4-rKnee 5-rFoot 6-root 7-thorax 8-neck 9-head 10-lHand 11-lElbow
    # 12-lShoulder 13-rShoulder 14-rElbow 15-rHand

    for d, cl in enumerate(cltr):
        for j in cl:
            for clust in j:
                (x, y), count, joint, _ = clust
                if joint == 0:
                    clor = colors["left foot"]
                elif joint == 5:
                    clor = colors["right foot"]
                elif joint == 10:
                    clor = colors["left hand"]
                else:
                    clor = colors["right hand"]

                if count > limit:
                    cv2.circle(image, (int(x), int(y)), int(count / 4), color=clor, thickness=-1)

    return image


def draw_indicator(image, climbers, times, stop=False, shift_legend=(50, 25)):
    """
    Indicator shows current height (also in meters) of climber on a graph.
    The thicker one presents a climber, according to whom animation is moving.
    :param image: area of drawing
    :param climbers:
    :param times: defines height to be drawn
    :param advantage: array of waiting indices
    :param stop:
    :param shift_legend: width of edges in graph
    :return: image
    """
    tl, tr = times
    H, W, _ = image.shape
    sh0, sh1 = shift_legend
    pxm = H / 15
    x0, y0 = sh0, int(climbers[0][tl, 6, 1])
    x1, y1 = W - sh1, int(climbers[1][tr, 6, 1])
    red, green, grey, black = (0, 0, 255), (0, 150, 0), (152, 152, 152), (0, 0, 0)
    color, color0 = black, black

    r = 6
    if stop:
        pts = np.array([(x0, y0), (x0 - r, y0 + r), (x0 - r, y0 - r), (x0 - r, y0 - r), ], np.int32)
        cv2.polylines(image, [pts], False, color)
        cv2.fillPoly(image, pts=[pts], color=color)
    else:  # colors for height
        if climbers[0][tl, 6, 1] > climbers[1][tr, 6, 1]:
            color, color0 = green, red
        if climbers[0][tl, 6, 1] < climbers[1][tr, 6, 1]:
            color, color0 = red, green

    # indicator for right one
    cv2.line(image, (x1, y1), (x1 + r, y1 + r), color=color, thickness=1)
    cv2.line(image, (x1, y1), (x1 + r, y1 - r), color=color, thickness=1)
    cv2.line(image, (x1 + r, y1 - r), (x1 + r, y1 + r), color=color, thickness=1)
    cv2.line(image, (x1, y1), (int(climbers[1][tr, 6, 0]), y1), color=grey, thickness=1)

    # indicator for left one
    cv2.line(image, (x0, y0), (x0 - r, y0 + r), color=color0, thickness=1)
    cv2.line(image, (x0, y0), (x0 - r, y0 - r), color=color0, thickness=1)
    cv2.line(image, (x0 - r, y0 - r), (x0 - r, y0 + r), color=color0, thickness=1)
    cv2.line(image, (x0, y0), (int(climbers[0][tl, 6, 0]), y0), color=grey, thickness=1)

    # display height difference in meters
    direction = "+" if y0 < y1 else ""
    cv2.putText(image,
                f"{direction}{np.round(np.round(15 - y0 / pxm, 2) - np.round(15 - y1 / pxm, 2), 2)}",
                (x0 - 45, y0 + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 0), 1)

    return image


def print_x_labels(image, label, points, color, font, font_size):
    """
    Prints x axis titles
    :param image:
    :param label:
    :param points:
    :param color:
    :param font:
    :param font_size:
    :return:
    """
    x, y = points
    size_ = cv2.getTextSize(f"{label}", font, font_size, 1)[0][0]
    cv2.putText(image, f"{label}", (int(x - size_ / 2), y), font, font_size, color, 1)


def print_delay_summary(image, points, sum_joints, colors, font, font_size):
    """
    Printunder each climber video a summary of dealy for each end effector
    :param image:
    :param points:
    :param sum_joints:
    :param colors:
    :param font:
    :param font_size:
    :return:
    """
    x, y = points
    x_ = x
    for c in range(2):
        e = 0  # text width shift
        for i, d in enumerate(colors.keys()):
            size_tex_t = cv2.getTextSize(f"{d}:{np.round(sum_joints[c][i], 2)}", font, font_size, 1)[0][0]
            cv2.circle(image, (int(x_ + e - 5), int(y - 5)), 4, color=colors[d], thickness=-1)
            cv2.putText(image, f"{d}:{np.round(sum_joints[c][i], 2)}", (x_ + e, y), font, font_size,
                        (0, 0, 0), thickness=1)
            e += size_tex_t + 10
        x_ = 2 * (image.shape[1] // 3)


def print_size_delay(image, sum_cluster, points, font, font_size):
    """
    Print dealy size legend maximum and minimum delay of both climbs
    :param image:
    :param sum_cluster:
    :param points:
    :param font:
    :param font_size:
    :return: None
    """
    x, y = points
    black = (0, 0, 0)
    rate = 50

    min15, max15 = np.min(sum_cluster), np.max(sum_cluster)

    if max15 > 15:
        cv2.circle(image, (int(x), int(y + 30)), int(min15 // 4), color=(0, 0, 0, 0), thickness=-1)
        cv2.circle(image, (int(x + 60), int(y + 30)), int(max15 // 4), color=(0, 0, 0, 0), thickness=-1)

        cv2.putText(image, f"{round(min15 / rate, 2)} s", (x + 5, y + 35), font, font_size, black, 1)
        cv2.putText(image, f"{round(max15 / rate, 2)} s", (x + 75, y + 35), font, font_size, black, 1)


def print_legend(image_l, image_up, colorsp, colorad, climbers, rate=50, colors=None):
    """Legends assigns time to size of delay point, colour to end effectors,
    explains graph.
    :parameter
    image - area of drawing
    ...

    :returns
    image
    """

    W, H = image_l.shape[1], image_l.shape[0]
    font, font_size = cv2.FONT_HERSHEY_SIMPLEX, 0.4

    # labels x-axis
    print_x_labels(image_l, "speed difference", (int(W / 2), int(H / 10)), colorsp, font, font_size)
    print_x_labels(image_up, "advantage in seconds", (int(image_up.shape[1] / 2), int(image_up.shape[0] - 10)), colorad,
                   font, font_size)

    x, y = W // 10, int(H // 3)

    cltr, sum_cluster, sum_joints = cp.delay_points(climbers)

    # print legend of delay
    cv2.putText(image_l, f"Delay:", (5, y), font, font_size, (0, 0, 0), 1)
    print_delay_summary(image_l, (W // 22, y), sum_joints, colors, font, font_size)

    if len(sum_cluster) > 0:
        print_size_delay(image_l, sum_cluster, (x, y), font, font_size)

    return image_l, image_up


def print_information(metrics, graph, image_up, climbers, rate):
    """compute mutual information
     :returns
     metrics, graph - tuple of images"""

    colorsp = (0, 128, 255)
    colorad = (153, 138, 72)
    colors = {"left foot": (68, 138, 235), "right foot": (36, 220, 249), "left hand": (71, 116, 75),
              "right hand": (67, 186, 142)}

    metrics = print_legend(metrics, image_up, colorsp, colorad, climbers, rate, colors)
    graph = print_graph(graph, climbers, rate, colorsp, colorad, colors)

    return metrics, graph


def get_data(matches, shape=(800, 1000), video_load=True):
    """parse the data and edit it to fit to graph

    :parameter
    matches - two comparing climbs
    shape - height, width of drawing area

    :returns
    name, canvas, video_match, climbers, un_climbers:
    """

    canvas = Canvas(shape)  # create canvas

    video_left = canvas.video_left
    video_right = canvas.video_right
    graph = canvas.graph.copy()

    #  finds files
    # un_file0, un_file1 = f"unpacked_data/{matches[0]}.data", f"unpacked_data/{matches[1]}.data" # BP SALANICOVA
    un_file0 = f"C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/unpacked_data/{matches[0]}.data"
    un_file1 = f"C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/unpacked_data/{matches[1]}.data"
    f_video0, f_video1 = f"videa/{matches[0]}.mp4", f"videa/{matches[1]}.mp4"

    # loads relative data and unroll the camera movement
    rel_climbers = fw.load_data(un_file0, un_file1) # - it is loading skeletons into an array


    # slow down movement and scaling - not for graph
    un_climbers = ed.insert_frame(rel_climbers.copy())
    un_climbers = ed.scaling(un_climbers, video_right.shape)

    # Relevant data for gpraph!!!!!!
    clms = fw.load_matrices(matches, rel_climbers.copy())   # - it is loading matrixes and multiply them into virtual refference wall
    clms_insert = ed.insert_frame(clms) # it is double the length
    climbers = ed.fit_to_graph(clms_insert, graph.shape)

    if video_load:
        try:
            video_match = fw.load_video([f_video0, f_video1], (video_left.shape[1], video_left.shape[0]))
        except IOError as e:
            print(e)
            sys.exit(1)
    else:
        video_match = None

    name = f"{matches[0]};{matches[1]}"

    return name, canvas, video_match, climbers, un_climbers


def play_match(matches, shape, stop, trj):
    """
    generates images for video/app

    :return: images - array of names of generated images
    """

    name, canvas, video_match, climbers, un_climbers = get_data(matches, shape)

    images = []
    graph = canvas.graph.copy()
    metrics, graph = print_information(canvas.metrics, graph, canvas.legend_up, climbers, rate=1 * 2 * 25)

    climbers_d = climbers

    fw.write_graph(name, cp.delay_points(climbers_d), cp.compute_speed(climbers_d),
                   ed.aligning_by_height_indices(climbers_d), climbers_d)
    #fw.write_trajectory("C:/Users/salan/Documents/SKOLA/SBAPR/out_data/koleracia.txt", climbers, trj) SALANICOVA BP
    fw.write_trajectory("C:/Users/I343585/Desktop/transformMatricies/editSalaniva_transform/SBAPR/out_data/koleracia.txt", climbers, trj)

    indc_c = [[i for i in range(len(climbers[j]))] for j in range(2)]
    indc_v = indc_c

    if stop:
        indc_v = ed.aligning_by_height_indices(climbers)
        desired_len = len(indc_v[0])
        fw.write_matching_video(indc_v, name)
        climbers_d = ed.synchronised_video_climber(climbers, desired_len)
        indc_c = [[*range(len(climbers_d[j]))] for j in range(2)]

    i = 0
    while i < max(len(indc_v[0]), len(indc_v[1])):
        # different length  f a climb -> display of last frame during the other finishes performance
        j = indc_c[0][-1] if i >= len(indc_c[0]) else indc_c[0][i]
        k = indc_c[1][-1] if i >= len(indc_c[1]) else indc_c[1][i]
        m = indc_v[0][-1] if i >= len(indc_v[0]) else indc_v[0][i]
        n = indc_v[1][-1] if i >= len(indc_v[1]) else indc_v[1][i]

        canvas.video_left = video_match[m, 0]
        canvas.video_right = video_match[n, 1]

        canvas.graph = graph
        canvas.graph = draw_indicator(canvas.graph, climbers_d, (j, k), stop=stop)
        canvas.graph = draw_climber(canvas.graph, climbers_d[0][j])
        canvas.graph = draw_climber(canvas.graph, climbers_d[1][k])

        canvas.video_left = draw_climber(canvas.video_left, un_climbers[0][m], v=True)
        canvas.video_right = draw_climber(canvas.video_right, un_climbers[1][n], v=True)

        if j > 3:
            canvas.graph = draw_trajectory(canvas.graph, climbers_d, (j, k))

        # cv2.imshow("full", canvas.full)
        # cv2.waitKey(150)
        cv2.imwrite(f"images/{name}{i + 1}.jpg", canvas.full)
        images.append(f"{name}{i + 1}.jpg")
        i += 1

    return images


