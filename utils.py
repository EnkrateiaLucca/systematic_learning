import cv2 as cv
import numpy as np
import sys
from ast import literal_eval


def convert_to_frames(min,secs,fps,h=None):
    if h is not None:
        h = h * 3600 * fps
    min_frames = min * 60 * fps
    sec_frames = secs * fps
    return min_frames+sec_frames


def get_indexes(begin,end,fps,h=None):
    index_start = int(np.floor(convert_to_frames(begin[0], begin[1], fps)))
    index_end = int(np.ceil(convert_to_frames(end[0],end[1],fps)))
    clip_duration = index_end - index_start
    return index_start, clip_duration


def get_list_of_index_clips(index_start, clip_duration):
    lista_list_index_clips = list(range(index_start, index_start+clip_duration))
    return lista_list_index_clips


def get_num_clips(list_index_pairs):
    return len(list_index_pairs)


#Check and try for different extensions
def create_video_writer(output_path, fps, h, w):
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, fps,
                         (int(w),int(h)))

    return out


def clip_video(video_path, output_file_path, list_clips):
    cap = cv.VideoCapture(video_path)
    fps = cap.get(cv.CAP_PROP_FPS)
    h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    w = cap.get(cv.CAP_PROP_FRAME_WIDTH)

    out = create_video_writer(output_file_path, fps,h,w)
    for clip in list_clips:
        begin = clip[0]
        end = clip[1]
        print("Begin: {}".format(begin))
        print("End: {}".format(end))
        print(get_indexes(begin,end,fps))
        index_start, clip_duration = get_indexes(begin,end,fps)
        #list_clips_frames.append(get_list_of_index_clips(index_start, clip_duration))
        index_vid = 0
        cap.set(1, index_start)
        while cap.isOpened():
            while index_vid<clip_duration:
                ret, frame = cap.read()
                #cv.imshow("frame", frame)
                out.write(frame)
                index_vid+=1

                if cv.waitKey(1) & 0xFF == ord("q"):
                    break
            break

    cap.release()
    cv.destroyAllWindows()



if __name__=="__main__":
    # Loads the video
    video_path = sys.argv[1]
    # Loads the output file name from terminal
    output_file_path = sys.argv[2]
    # Loads the list of clips with start and end as a list of lists
    list_clips = literal_eval(sys.argv[3])
    
    clip_video(video_path,output_file_path,list_clips)

    
