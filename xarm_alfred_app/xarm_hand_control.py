from cv2 import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
import sys
import signal
from collections import deque
import statistics
from statistics import mode #, multimode
import math
from collections import Counter
import time 
import robot_control


# def signal_handler(signal, frame):
# 	sys.exit(0)

### Functions
def recognizeHandGesture(landmarks):
  thumbState = 'UNKNOWN'
  indexFingerState = 'UNKNOWN'
  middleFingerState = 'UNKNOWN'
  ringFingerState = 'UNKNOWN'
  littleFingerState = 'UNKNOWN'

  recognizedHandGesture = ""
  pseudoFixKeyPoint = landmarks.landmark[2].y
  if (landmarks.landmark[3].y < pseudoFixKeyPoint and landmarks.landmark[4].y < landmarks.landmark[3].y and landmarks.landmark[4].y < landmarks.landmark[6].y ):
    thumbState = 'OPENUP'
  elif (pseudoFixKeyPoint < landmarks.landmark[3].y  and landmarks.landmark[3].y  < landmarks.landmark[4].y ):
    thumbState = 'OPENDOWN'
  elif  (landmarks.landmark[2].x < landmarks.landmark[3].x  and landmarks.landmark[3].x  < landmarks.landmark[4].x ):
    thumbState = 'CLOSE'

  pseudoFixKeyPoint = landmarks.landmark[6].y
  if (landmarks.landmark[7].y < pseudoFixKeyPoint and landmarks.landmark[8].y < landmarks.landmark[7].y):
    indexFingerState = 'OPENUP'
  elif (pseudoFixKeyPoint < landmarks.landmark[7].y and landmarks.landmark[7].y < landmarks.landmark[8].y):
    indexFingerState = 'CLOSE'

  pseudoFixKeyPoint = landmarks.landmark[10].y
  if (landmarks.landmark[11].y < pseudoFixKeyPoint and landmarks.landmark[12].y < landmarks.landmark[11].y and landmarks.landmark[2].x < landmarks.landmark[10].x):
    middleFingerState = 'OPENUP'
  elif (pseudoFixKeyPoint < landmarks.landmark[11].y and landmarks.landmark[11].y < landmarks.landmark[12].y):
    middleFingerState = 'CLOSE'

  pseudoFixKeyPoint = landmarks.landmark[14].y
  if (landmarks.landmark[15].y < pseudoFixKeyPoint and landmarks.landmark[16].y < landmarks.landmark[15].y and landmarks.landmark[2].x < landmarks.landmark[14].x):
    ringFingerState = 'OPENUP'
  elif (pseudoFixKeyPoint < landmarks.landmark[15].y and landmarks.landmark[15].y < landmarks.landmark[16].y):
    ringFingerState = 'CLOSE'

  pseudoFixKeyPoint = landmarks.landmark[18].y
  if (landmarks.landmark[19].y < pseudoFixKeyPoint and landmarks.landmark[20].y < landmarks.landmark[19].y and landmarks.landmark[2].x < landmarks.landmark[18].x):
    littleFingerState = 'OPENUP'
  elif (pseudoFixKeyPoint < landmarks.landmark[19].y and landmarks.landmark[19].y < landmarks.landmark[20].y):
    littleFingerState = 'CLOSE'


  ############################################__DOWN__###################################################


  pseudoFixKeyPoint = landmarks.landmark[5].y
  if (landmarks.landmark[6].y > pseudoFixKeyPoint and landmarks.landmark[8].y > landmarks.landmark[7].y and landmarks.landmark[7].y > landmarks.landmark[6].y and landmarks.landmark[3].x < landmarks.landmark[6].x):
    indexFingerState = 'OPENDOWN'

  pseudoFixKeyPoint = landmarks.landmark[9].y
  if (landmarks.landmark[10].y > pseudoFixKeyPoint and landmarks.landmark[12].y > landmarks.landmark[11].y and landmarks.landmark[11].y > landmarks.landmark[10].y and landmarks.landmark[2].x < landmarks.landmark[10].x ):
    middleFingerState = 'OPENDOWN'

  pseudoFixKeyPoint = landmarks.landmark[13].y
  if (landmarks.landmark[14].y > pseudoFixKeyPoint and landmarks.landmark[16].y > landmarks.landmark[15].y and landmarks.landmark[15].y > landmarks.landmark[14].y and landmarks.landmark[2].x < landmarks.landmark[14].x):
    ringFingerState = 'OPENDOWN'

  pseudoFixKeyPoint = landmarks.landmark[17].y
  if (landmarks.landmark[18].y > pseudoFixKeyPoint and landmarks.landmark[20].y > landmarks.landmark[19].y and landmarks.landmark[19].y > landmarks.landmark[18].y and landmarks.landmark[2].x < landmarks.landmark[18].x):
    littleFingerState = 'OPENDOWN'

  ############################################__RIGHT__###################################################

  pseudoFixKeyPoint = landmarks.landmark[5].x
  if (landmarks.landmark[6].x > pseudoFixKeyPoint and landmarks.landmark[8].x > landmarks.landmark[7].x and landmarks.landmark[7].x > landmarks.landmark[6].x and landmarks.landmark[3].y < landmarks.landmark[5].y ):
    indexFingerState = 'OPENRIGHT'

  pseudoFixKeyPoint = landmarks.landmark[9].x
  if (landmarks.landmark[10].x > pseudoFixKeyPoint and landmarks.landmark[12].x > landmarks.landmark[11].y and landmarks.landmark[11].x > landmarks.landmark[10].x and landmarks.landmark[2].y < landmarks.landmark[10].y):
    middleFingerState = 'OPENRIGHT'

  pseudoFixKeyPoint = landmarks.landmark[13].x
  if (landmarks.landmark[14].x > pseudoFixKeyPoint and landmarks.landmark[16].x > landmarks.landmark[15].x and landmarks.landmark[15].x > landmarks.landmark[14].x and landmarks.landmark[2].y < landmarks.landmark[14].y):
    ringFingerState = 'OPENRIGHT'

  pseudoFixKeyPoint = landmarks.landmark[17].x
  if (landmarks.landmark[18].x > pseudoFixKeyPoint and landmarks.landmark[20].x > landmarks.landmark[19].x and landmarks.landmark[19].x > landmarks.landmark[18].x and landmarks.landmark[2].y < landmarks.landmark[18].y):
    littleFingerState = 'OPENRIGHT'

  ############################################__LEFT__###################################################

  # pseudoFixKeyPoint = landmarks.landmark[2].x
  # if (landmarks.landmark[3].x < pseudoFixKeyPoint and landmarks.landmark[4].x < landmarks.landmark[3].x ):
  #   thumbState = 'OPENLEFT'


  pseudoFixKeyPoint = landmarks.landmark[5].x
  if (landmarks.landmark[6].x < pseudoFixKeyPoint and landmarks.landmark[8].x < landmarks.landmark[7].x and landmarks.landmark[7].x < landmarks.landmark[6].x and landmarks.landmark[2].y < landmarks.landmark[6].y and landmarks.landmark[2].x > landmarks.landmark[6].x):
    indexFingerState = 'OPENLEFT'

  pseudoFixKeyPoint = landmarks.landmark[9].x
  if (landmarks.landmark[10].x < pseudoFixKeyPoint and landmarks.landmark[12].x < landmarks.landmark[11].y and landmarks.landmark[11].x <landmarks.landmark[10].x and landmarks.landmark[2].y < landmarks.landmark[10].y and landmarks.landmark[2].x > landmarks.landmark[6].x):
    middleFingerState = 'OPENLEFT'

  pseudoFixKeyPoint = landmarks.landmark[13].x
  if (landmarks.landmark[14].x < pseudoFixKeyPoint and landmarks.landmark[16].x < landmarks.landmark[15].x and landmarks.landmark[15].x < landmarks.landmark[14].x and landmarks.landmark[2].y < landmarks.landmark[14].y and landmarks.landmark[2].x > landmarks.landmark[6].x):
    ringFingerState = 'OPENLEFT'

  pseudoFixKeyPoint = landmarks.landmark[17].x
  if (landmarks.landmark[18].x < pseudoFixKeyPoint and landmarks.landmark[20].x < landmarks.landmark[19].x and landmarks.landmark[19].x < landmarks.landmark[18].x and landmarks.landmark[2].y < landmarks.landmark[18].y and landmarks.landmark[2].x > landmarks.landmark[6].x):
    littleFingerState = 'OPENLEFT'

  ########################################__ACTION__############################################################

  if (thumbState == 'OPENUP' and landmarks.landmark[8].y<landmarks.landmark[12].y and landmarks.landmark[12].y<landmarks.landmark[16].y):
    recognizedHandGesture = "THUMBUP"

  if (thumbState == 'OPENDOWN' and landmarks.landmark[8].y>landmarks.landmark[12].y and landmarks.landmark[12].y>landmarks.landmark[16].y ):
    recognizedHandGesture = "THUMBDOWN"

  if ( indexFingerState == 'OPENUP' and middleFingerState == 'OPENUP' and ringFingerState == 'OPENUP' and littleFingerState == 'OPENUP'):
    recognizedHandGesture = "UP"

  if ( indexFingerState == 'OPENDOWN' and middleFingerState == 'OPENDOWN' and ringFingerState == 'OPENDOWN' and littleFingerState == 'OPENDOWN'):
    recognizedHandGesture = "DOWN"

  if ( indexFingerState == 'OPENRIGHT' and middleFingerState == 'OPENRIGHT' and ringFingerState == 'OPENRIGHT' and littleFingerState == 'OPENRIGHT'):
    recognizedHandGesture = "RIGHT"

  if ( indexFingerState == 'OPENLEFT' and middleFingerState == 'OPENLEFT' and ringFingerState == 'OPENLEFT' and littleFingerState == 'OPENLEFT'):
    recognizedHandGesture = "LEFT"

  if (middleFingerState == 'OPENUP' and indexFingerState == 'OPENUP' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE' ):
    recognizedHandGesture ="PEACE"

  if (middleFingerState == 'CLOSE' and indexFingerState == 'OPENUP' and ringFingerState == 'CLOSE' and littleFingerState == 'OPENUP' ):
    recognizedHandGesture ="SPIDERMAN"

  if (middleFingerState == 'CLOSE' and indexFingerState == 'OPENUP' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE' ):
    recognizedHandGesture ="INDEX"

  if (middleFingerState == 'OPENUP' and indexFingerState == 'CLOSE' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE' ):
    recognizedHandGesture ="FUCK"

  if (middleFingerState == 'OPENUP' and indexFingerState == 'OPENUP' and ringFingerState == 'OPENUP' and littleFingerState == 'CLOSE' ):
    recognizedHandGesture ="THREE"

  if ( indexFingerState == 'CLOSE' and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE'):
    recognizedHandGesture = "FIST"

  if (landmarks.landmark[8].y>landmarks.landmark[7].y and landmarks.landmark[8].y<landmarks.landmark[5].y and landmarks.landmark[12].y>landmarks.landmark[11].y and landmarks.landmark[12].y<landmarks.landmark[9].y and landmarks.landmark[16].y>landmarks.landmark[15].y and landmarks.landmark[16].y<landmarks.landmark[13].y):
    recognizedHandGesture = "GRAB"
  

  # print("Thumb : "+str(thumbState))
  # print ("Index : "+str(indexFingerState))
  # print ("Middle : "+str(middleFingerState))
  # print ("Ring : "+str(ringFingerState))
  # print ("Little : "+str(littleFingerState))

  # print(recognizedHandGesture)
  return recognizedHandGesture



#trigger = []

def isTrigger(landmarks, trigger):
    trigger[0] = landmarks.landmark[0].x
    trigger[1] = landmarks.landmark[0].y
    return trigger

def isNewPosition(landmarks, trigger):

    initialPosition_x = trigger[0]
    initialPosition_y = trigger[1]

    actualPosition_x = landmarks.landmark[0].x
    actualPosition_y = landmarks.landmark[0].y

    delta_x = initialPosition_x - actualPosition_x
    delta_y = initialPosition_y - actualPosition_y

    delta = [delta_x, delta_y, 0]

    #newposition = cf.position() + np.array([delta_x, delta_y, 0])




def isSliding(landmarks,memo):

    actualPosition_x = landmarks.landmark[0].x
    actualPosition_y = landmarks.landmark[0].y
    actualPosition_x2 = landmarks.landmark[5].x
    actualPosition_y2 = landmarks.landmark[5].y
    

    

    if memo == None:
        memo=[landmarks.landmark[0].x,landmarks.landmark[0].y,landmarks.landmark[5].x,landmarks.landmark[5].y]

    lastPosition_x,lastPosition_y,lastPosition_x2,lastPosition_y2 = memo[0],memo[1],memo[2],memo[3]

    slide = ""
    memory=[]

    last_distance= math.sqrt((lastPosition_x2-lastPosition_x)**2+(lastPosition_y2-lastPosition_y)**2)
    actual_distance= math.sqrt((actualPosition_x2-actualPosition_x2)**2+(actualPosition_y2-actualPosition_y)**2)

    # print("distances :",last_distance-actual_distance)

    # if last_distance-actual_distance > 0.003:
    #     slide = "ZOOM OUT"
    # if last_distance - actual_distance < -0.001:
    #     slide = "ZOOM IN"
    if actualPosition_x - lastPosition_x > 0.01:
        slide = "RIGHT SLIDE"
    if actualPosition_y - lastPosition_y > 0.01:
        slide = "DOWN SLIDE"
    if actualPosition_x - lastPosition_x < -0.01:
        slide = "LEFT SLIDE"
    if actualPosition_y - lastPosition_y < -0.01:
        slide = "UP SLIDE"

    memory= [actualPosition_x, actualPosition_y,actualPosition_x2,actualPosition_y2]
    
    if actualPosition_x - lastPosition_x > 0.01 and actualPosition_y - lastPosition_y > 0.01:
        if actualPosition_x - lastPosition_x > actualPosition_y - lastPosition_y:
            slide="RIGHT SLIDE"
            memory= [actualPosition_x, lastPosition_y,actualPosition_x2,actualPosition_y2]
        else:
            slide="DOWN SLIDE"
            memory= [lastPosition_x, actualPosition_y,actualPosition_x2,actualPosition_y2]

    if actualPosition_x - lastPosition_x > 0.01 and actualPosition_y - lastPosition_y < -0.01:
        if actualPosition_x - lastPosition_x > -(actualPosition_y - lastPosition_y):
            slide="RIGHT SLIDE"
            memory= [actualPosition_x, lastPosition_y,actualPosition_x2,actualPosition_y2]
        else:
            slide="UP SLIDE"
            memory= [lastPosition_x, actualPosition_y,actualPosition_x2,actualPosition_y2]

    if actualPosition_x - lastPosition_x < -0.01 and actualPosition_y - lastPosition_y > 0.01:
        if actualPosition_x - lastPosition_x < -(actualPosition_y - lastPosition_y):
            slide="LEFT SLIDE"
            memory= [actualPosition_x, lastPosition_y,actualPosition_x2,actualPosition_y2]
        else:
            slide="DOWN SLIDE"
            memory= [lastPosition_x, actualPosition_y,actualPosition_x2,actualPosition_y2]

    if actualPosition_x - lastPosition_x < -0.01 and actualPosition_y - lastPosition_y < -0.01:
        if actualPosition_x - lastPosition_x < (actualPosition_y - lastPosition_y):
            slide="LEFT SLIDE"
            memory= [actualPosition_x, lastPosition_y,actualPosition_x2,actualPosition_y2]
        else:
            slide="UP SLIDE"
            memory= [lastPosition_x, actualPosition_y,actualPosition_x2,actualPosition_y2]

    if slide == "":
        memory=[lastPosition_x,lastPosition_y,lastPosition_x2,lastPosition_y2]

   

    return [slide,memory]


def addToQueueAndAverage(d, image):
    global theta
    d.append(image)
    counter = Counter(d)
    best = counter.most_common(3)

    if len(best)>2:
      if best[0][0]=="":                    #We remove the frames where we are not moving
        best.remove(best[0])
      elif best[1][0]=="":
        best.remove(best[1])

      if best[0][0]=="UP SLIDE" or best[0][0]=="DOWN SLIDE":
        best[0],best[1]=best[1],best[0]
      
      if best[0][0]=="LEFT SLIDE":
        if best[1][0]=="UP SLIDE":
          theta=math.pi/4+math.pi/2
        elif best[1][0]=="DOWN SLIDE":
          theta=math.pi/4+math.pi
      
      if best[0][0]=="RIGHT SLIDE":
        if best[1][0]=="UP SLIDE":
          theta=math.pi/4
        elif best[1][0]=="DOWN SLIDE":
          theta=-math.pi/4
          # theta=math.pi/4+math.pi*(2/3)

    elif len(best)==2:
      if best[0][0]=="":                     #We remove the frames where we are not moving
        best.remove(best[0])
      elif best[1][0]=="":
        best.remove(best[1])
      
      if best[0][0]=="RIGHT SLIDE":
        theta=0
      elif best[0][0]=="UP SLIDE":
        theta=math.pi/2
      elif best[0][0]=="LEFT SLIDE":
        theta=math.pi
      elif best[0][0]=="DOWN SLIDE":
        theta=math.pi*(3/2)

    else:
      if best[0][0]=="RIGHT SLIDE":
        theta=0
      elif best[0][0]=="UP SLIDE":
        theta=math.pi/2
      elif best[0][0]=="LEFT SLIDE":
        theta=math.pi
      elif best[0][0]=="DOWN SLIDE":
        theta=math.pi*(3/2)

    if len(d) == precision:
      try:
        rep = mode(d)
        if (rep != ""):
          numberOfRep = d.count(rep)
          speed=numberOfRep/precision          #Speed value beetween 0-1
          return([rep,speed,theta])
        else:
          if  d.count(rep) <= precision*0.80  :
            a = list(filter(lambda a: a != "", d))
            rep2 = mode(a)
            numberOfRep2 = a.count(rep2)
            return([rep2,numberOfRep2/precision,theta])
          else:
            return(['',0,theta])
      except:
        return(['',0,theta])
    else:
      return(['',0,theta])

def execute():
    print("execute")
    start=time.time()
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5,max_num_hands=1)
    cap = cv2.VideoCapture(0)
    memo = None
    i=0

    while cap.isOpened():
      
      success, image = cap.read()
      if not success:
        break

      # Flip the image horizontally for a later selfie-view display, and convert
      # the BGR image to RGB.
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      results = hands.process(image)

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      font = cv2.FONT_HERSHEY_COMPLEX

      if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        #Get Signal: average signal. works.
        image_signal = recognizeHandGesture(results.multi_hand_landmarks[0])
        video_signal = addToQueueAndAverage(d_signal, image_signal)
        #print("video_signal: ", video_signal)
        text = str(id)+str(video_signal[0])

        #Get Slide: should be based on pose with goTo().
        image_slide,memo = isSliding(results.multi_hand_landmarks[0],memo)
        video_slide = addToQueueAndAverage(d_slide, image_slide)

        speed = str(id) + "V" +str(video_slide[1])
        # theta = str(id) + "A" +str(video_slide[2])

        i+=1
        msg = f"#402 {video_slide[1]:.3f} {video_slide[2]} {video_signal[0]}"
        if i == 15:
            robot_control.rasa_command_queue.put(msg)
            i=0
            print(f"MESSAGE : {msg}")


        angle=video_slide[2]/(2*math.pi)*360
        # print("THETA: ",theta)

        cv2.putText(image, text[1:], (0,30), font, 1, (0, 0, 255), 2, cv2.LINE_4)
        cv2.putText(image, "FPS : "+str(1/(time.time()-start)), (0,60), font, 1, (0, 0, 255), 2, cv2.LINE_4)
        start=time.time()
        cv2.putText(image, "Speed :"+speed[2:], (0,90), font, 1, (0, 0, 255), 2, cv2.LINE_4)
        cv2.putText(image, "Theta :"+str(angle), (0,120), font, 1, (0, 0, 255), 2, cv2.LINE_4)
        start=time.time()

      cv2.imshow('MediaPipe Hands', image)
      if cv2.waitKey(5) & 0xFF == 27:
        break

    hands.close()
    cap.release()


# signal.signal(signal.SIGINT, signal_handler)


arm = robot_control.Arm(daemon=True, )
arm.start()
if __name__ == '__main__':
    try:
        #Testing our function
        global d_signal, d_slide, trigger, precision, id, theta
        id = 1
        precision = 15              #we can have several precision for the speed
        theta=0
        d_signal = deque([], precision)
        d_slide = deque([], precision)
        trigger = []
        execute()
    except:
      pass
