"""my_controller controller."""

from controller import Robot
class node:
  def __init__(self,id,adj,dir,searched):
    self.adj=adj
    self.id=id
    self.dir=dir
    self.searched=searched
  def insertEdge(self,u ):
    u.adj.append(self.id)
    self.adj.append(u.id)

graph=[]
for i in range(16):
  graph.append(node(i,[],0,False))
robot = Robot()
timestep = int(robot.getBasicTimeStep())

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
psNames=['ps0','ps7','ps3','ps4']
ps=[]
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
for i in range(4):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(timestep)

def get_ps_value():
    data=[]
    for i in range(4):
        data.append(ps[i].getValue())
    return data
def delay(ms):
    initTime = robot.getTime()      # Store starting time (in seconds)
    while robot.step(timestep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms: # If time elapsed (converted into ms) is greater than value passed in
            break

MAX_SPEED = 6.28
def stop_motor():
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def move_forward_motor(duration):
    leftMotor.setVelocity(0.5*MAX_SPEED)
    rightMotor.setVelocity(0.5*MAX_SPEED)
    delay(duration)

def move_backward_motor():
    leftMotor.setVelocity(-0.5*MAX_SPEED)
    rightMotor.setVelocity(-0.5*MAX_SPEED)
    delay(1500)

def rotate_right_motor():
    leftMotor.setVelocity(0.5*MAX_SPEED)
    rightMotor.setVelocity(-0.5*MAX_SPEED)
    delay(750)

def rotate_left_motor():
    leftMotor.setVelocity(-0.5*MAX_SPEED)
    rightMotor.setVelocity(0.5*MAX_SPEED)
    delay(750)



def detect(array):
    threshold=80
    for i in range(len(array)):
        if array[i]>threshold:
            return 'wall'
    return 'path'

def search(n:node,stack,duration):
    res=[]
    move_forward_motor(duration)
    res.append(detect(get_ps_value()))
    print(get_ps_value(),res[0])
    move_backward_motor()
    move_backward_motor()
    res.append(detect(get_ps_value()))
    print(get_ps_value(),res[1])
    move_forward_motor(duration)
    rotate_left_motor()
    move_forward_motor(duration)
    res.append(detect(get_ps_value()))
    print(get_ps_value(),res[2])
    move_backward_motor()
    move_backward_motor()
    res.append(detect(get_ps_value()))
    print(get_ps_value(),res[3])
    move_forward_motor(duration)
    rotate_right_motor()
    rotate_right_motor()
    stop_motor()
    #
    tmp=res.copy()
    if n.dir==0:
      res[0]=tmp[2]
      res[1]=tmp[1]
      res[2]=tmp[3]
      res[3]=tmp[0]
    elif n.dir==90:
      res[0]=tmp[0]
      res[1]=tmp[2]
      res[2]=tmp[1]
      res[3]=tmp[3]
    elif n.dir==180:
      res[0]=tmp[3]
      res[1]=tmp[0]
      res[2]=tmp[2]
      res[3]=tmp[1]
    else:#270
      res[0]=tmp[1]
      res[1]=tmp[3]
      res[2]=tmp[0]
      res[3]=tmp[2]


    #ccwise

    i=n.id
    if res[0] =='path':
      if i >= 4 and graph[i-4].searched == False :
        n.insertEdge(graph[i-4])
        stack.append(n)
        stack.append(graph[i-4])
    if res[1] =='path':
      if i%4 >0 and  graph[i-1].searched == False :
        n.insertEdge(graph[i-1])
        stack.append(n)
        stack.append(graph[i-1])
    if  res[2] =='path':
      if i <= 11 and graph[i+4].searched== False :
        n.insertEdge(graph[i+4])
        stack.append(n)
        stack.append(graph[i+4])
    if  res[3] =='path':
      if i%4 <3 and graph[i+1].searched== False :
        n.insertEdge(graph[i+1])
        stack.append(n)
        stack.append(graph[i+1])

    #change dir after done search
    n.dir=(n.dir-90)%360
    n.searched=True
    return stack


def move_to(head, dest, duration):  # dest is node
    k = (head - dest) // 90
    print('k is  ', k)
    if k >= 0:
        if k == 3:
            rotate_left_motor()
        elif k == 2:
            rotate_right_motor()
            # calibration
            stop_motor()
            delay(500)
            rotate_right_motor()
            delay(30)

        elif k == 1:
            rotate_right_motor()
        else:
            pass
        move_forward_motor(duration)
        move_forward_motor(duration)
        stop_motor()

    else:
        if k == -3:
            rotate_right_motor()
        elif k == -2:
            rotate_left_motor()
            # calibration
            stop_motor()
            delay(500)
            rotate_left_motor()
            delay(30)
        else:
            rotate_left_motor()
        move_forward_motor(duration)
        move_forward_motor(duration)
        stop_motor()
def change_pos(n1,n2,duration):#dest is node
    pos1,pos2=n1.id,n2.id
    if pos2==pos1+1:
      n2.dir=0
      move_to(n1.dir,n2.dir,duration)
      return n2
    elif pos2==pos1-1:
      n2.dir=180
      move_to(n1.dir,n2.dir,duration)
      return n2
    elif pos2==pos1+4:
      n2.dir=270
      move_to(n1.dir,n2.dir,duration)
      return n2
    elif pos2==pos1-4:
      n2.dir=90
      move_to(n1.dir,n2.dir,duration)
      return n2
    else:#equall
      return n1

stack=[]
stack.append(graph[3])
center_node=stack[len(stack)-1]


while stack :
  if center_node.searched==False :
    length=len(stack)
    print('enter dir is : ',center_node.dir,end=' ---')
    stack=search(center_node,stack,1500)
    print('after done search -> ',center_node.dir)
    if len(stack)   > length:
      # delay(500)
      center_node= change_pos(center_node,stack[len(stack)-1],1888.2)
      print('now node is111 : ',center_node.id)
  else :
    print("this node searched")
    stack.pop()
    if len(stack) == 0:
      break
    center_node=change_pos(center_node,stack[len(stack)-1],1980)
    # delay(500)
    stack.pop()
    center_node=change_pos(center_node,stack[len(stack)-1],1980)
    #delay(500)
    print('now node is 2222 : ',center_node.id)
  print('stack is :',end=' ')
  for i in range(len(stack)):
    print(stack[i].id,end=' - ')
  print('\n\n')



