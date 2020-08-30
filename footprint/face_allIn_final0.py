import time, os, dlib, glob
from skimage import io
import cv2
import imutils
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
from matplotlib import pyplot as plt
import h5py
from playsound import playsound
from threading import Thread

#def play_music():
    # playsound('./sound/voice1_ch.wav')
    # playsound('./sound/voice1_en.wav')
    # playsound('./sound/voice1_j.wav')



def test():

    # 取得dlib預設的臉部偵測器
    detector = dlib.get_frontal_face_detector()
    # 根據shape_predictor方法載入68個特徵點模型，此方法為人臉表情識別的偵測器
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    # 臉部校正
    fa = FaceAligner(predictor, desiredFaceWidth=256)
    # 載入人臉辨識檢測器
    facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
    # 比對人臉描述子列表
    descriptors = []
    # 比對人臉名稱列表
    candidate = []
    # 圖片路徑
    path=[]

    # 開鏡頭前先播放聲音
    playsound('./sound/voice1_ch.mp3')
    playsound('./sound/voice1_en.mp3')
    playsound('./sound/voice1_j.mp3')
    # Play Music on Separate Thread (in background)
    # music_thread = Thread(target=play_music)
    # music_thread.start()


    # 開啟影片檔案
    cap = cv2.VideoCapture(0)
    # 比對人臉圖片資料夾名稱
    faces_folder_path = "./rec"
    WHO = None
    Erro = 0
    # 有讀過的照片存成新的檔可直接使用，有新的圖片再加

    # 路徑中的file個數
    NUM_OF_FILES = 0  # 檔案數
    for fn in os.listdir(faces_folder_path):
        NUM_OF_FILES += 1
    #print(NUM_OF_FILES)


    person = [0 for i in range(NUM_OF_FILES)]
    #print(person)

    # 原本的個數
    f = open("numOfFiles.txt")
    num_o = f.read()
    num_o = int(num_o)
    h5file = './desc.h5'
    #print(sorted(glob.glob(os.path.join(faces_folder_path, "*.jpg")),key=os.path.getmtime))
    # 所有檔名
    for f in sorted(glob.glob(os.path.join(faces_folder_path, "*.jpg")),key=os.path.getmtime):
        base = os.path.basename(f)
        # print(base)
        # 依序取得圖片檔案人名，存到candidate一維陣列中
        candidate.append(os.path.splitext(base)[0])
        # print(candidate)
        path.append(f)
    #print(path)

    # 如果新的檔案數與舊的檔案數不同
    if num_o != NUM_OF_FILES:
        # 把新的個數寫到txt檔裡
        num = open('numOfFiles.txt', 'w')
        num.write(str(NUM_OF_FILES))
        num.close()

        # 新增檔名 new NUM_OF_FILES  ori num_o
        c = open("cand.txt", "a",encoding="utf-8")
        for i in range(num_o-1, NUM_OF_FILES-1, 1):  # -2 -1是mac檔多一個檔案
            c.write('\n')
            c.write(candidate[i])

        c.close()

        # 新增one shot計算匡
        # 讀取資料夾裡的圖片及檔案名(人名)，並將每張圖的128維特徵向量存到description一維陣列中
        h5f = h5py.File(h5file, 'a')
        for i in range(num_o-1, NUM_OF_FILES-1, 1):
            img = io.imread(path[i])
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # 1.人臉偵測
            face_rects = detector(img, 0)
            # print(face_rects)
            for index, face in enumerate(face_rects):
                # 2.人臉校正
                faceAligned = fa.align(img, gray, face)
                # 3.再人臉偵測(去除校正後多餘的部分)
                face_rects2 = detector(faceAligned, 1)
                for index2, face2 in enumerate(face_rects2):
                    ax1 = face2.left()
                    ay1 = face2.top()
                    ax2 = face2.right()
                    ay2 = face2.bottom()
                    # 4.68特徵點偵測
                    shape = predictor(faceAligned, face2)
                    # 5.取得描述子，128維特徵向量
                    face_descriptor = facerec.compute_face_descriptor(faceAligned, shape)
                    # 轉換numpy array格式
                    v = np.array(face_descriptor)
                    descriptors.append(v)
                    #print(face_rects)
            # original的在face_allIn_final0.py
            h5f.create_dataset('new{}'.format(i), data=v)
        h5f.close()
        # 存新的到原本的txt檔
        np.savetxt('desc_txt.txt', descriptors)

    # 檢查用
    # 讀檔
    kk = h5py.File(h5file, 'r')
    #print(type(h5f))
    #print(h5f)
    # 通過切片得到numpy陣列
    #print(list(kk.keys()))
    #print(h5f['new8'][:])
    #下面這條要在裡面執行，現在在外面

    #for i in range(0, NUM_OF_FILES-1, 1):
      #print(kk['new{}'.format(i)][:])


    # 以迴圈從影片檔案讀取影格，並顯示出來
    while cap.isOpened():
        k = open("cand.txt",encoding="utf-8")
        cand = k.readlines()
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        # 從視訊鏡頭擷取畫面
        ret, frame = cap.read()
        # 縮小圖片
        frame = imutils.resize(frame, width=800) # 顯示影像框框
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # 1.人臉偵測
        face_rects = detector(frame, 1)
        # 取出所有偵測的結果(所有人臉座標點)
        for index, rect in enumerate(face_rects):
            x1 = rect.left()
            y1 = rect.top()
            x2 = rect.right()
            y2 = rect.bottom()
            # 以方框標示偵測的人臉
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)
            # 2.人臉校正
            faceAligned = fa.align(frame, gray, rect)
            # 3.再人臉偵測(去除校正後多餘的部分)
            face_rects2 = detector(faceAligned, 1)
            # 取出所有偵測的結果(所有人臉座標點)
            for index2, rect2 in enumerate(face_rects2):
                ax1 = rect2.left()
                ay1 = rect2.top()
                ax2 = rect2.right()
                ay2 = rect2.bottom()
                # 4.68特徵點偵測
                shape = predictor(faceAligned, rect2)
                # 5.取得描述子，128維特徵向量
                face_descriptor = facerec.compute_face_descriptor(faceAligned, shape)
                # 轉換numpy array格式
                d_test = np.array(face_descriptor)
                # 計算歐式距離  (與圖片庫裡，各個人臉間的距離)(5張照片就有5個距離)
                # 開h5檔案
                h5f = h5py.File(h5file, 'r')
                    # 清空 存放人臉距離的陣列
                dist = []
                for i in range(0, NUM_OF_FILES -1, 1): #-1就好
                    # 計算距離
                    dist_ = np.linalg.norm(h5f['new{}'.format(i)][:]- d_test)
                    # 加入陣列
                    dist.append(dist_)
                # 辨識人名
                if dist != []:
                    # 將比對人名和比對出來的歐式距離組成一個dict
                    c_d = dict(zip(cand, dist))
                    # 根據歐式距離由小到大排序 [("名字",距離)]二微陣列
                    cd_sorted = sorted(c_d.items(), key=lambda d: d[1])
                    #print(cd_sorted)
                    # 歐式距離(0~1)越小越像，設定0.5作為最低辨識標準
                    if cd_sorted[0][1] < 0.4:
                        rec_name = cd_sorted[0][0]
                    else:
                        rec_name = "No Data"
                        Erro = Erro + 1
                        if Erro == 6:
                            WHO = "No Data"
                            cap.release()
                            cv2.destroyAllWindows()
                            return WHO
                            break

                # 標示辨識的人名(中文)
                imgPil = Image.fromarray(frame)
                font = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 20)
                draw = ImageDraw.Draw(imgPil)
                draw.fontmode = '1'  # 關閉反鋸齒
                draw.text((x1, y1 - 20), rec_name, font=font, fill=(255, 255, 255))
                frame = np.array(imgPil)
                for index, name in enumerate(cand):
                    if rec_name == name:
                        person[index] = person[index] + 1
                        # print(person)
                        if person[index] == 4:
                            WHO = cand[index]
                            # 標示辨識的人名(中文)
                            if WHO is not None:
                                time.sleep(5)
                                cap.release()
                                cv2.destroyAllWindows()
                                print(WHO)
                                return WHO
                            break
                    elif sum(person) > 8:
                        WHO = "No Data"
                        cap.release()
                        cv2.destroyAllWindows()
                        return WHO
                        break

            # 標示辨識的人名(只能標示英文)
            # cv2.putText(frame, rec_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # CV2是用BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 顯示結果
        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

#test()
