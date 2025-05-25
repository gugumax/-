
# !!!!!!!!!!!ROBOT9th!!!!!!!!!!
import re
import socket
import time

client_socket = None
last_time=0
def connect_to_Main(): #死循环连接定位程序socket
	global client_socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.setblocking(True)#阻塞模式
	# connected = False
	# while not connected:
	try:
		client_socket.connect(('localhost', 23335))
		connected = True
		print("connect to Main success")
	except :
		time.sleep(1)
	# return client_socket

def send_to_Main(text): #发送给主程序yolo返回的数据
	try:
		global client_socket
		client_socket.send(text.encode())
	except :
		print(f"Send data error in port 23335")


need_remove=[]#box在一定范围内才发送，因为每次只能抓一格的东西,所以要剔除一些	

# def Get_True_box(boxin):
# 	global last_time
# 	# if(time.time()-last_time>=60):
# 	# 	last_time=time.time()
# 	# print("左上点的坐标为：(" + str(box[0+num*4]) + "," + str(box[1+num*4]) + ")，右下点的坐标为(" + str(box[2+num*4]) + "," + str(box[3+num*4]) + ")")
# 	# print("点{}:({},{})".format(num,box[0+num*2],box[1+num*2]))
# 	print(boxin)
# 	for box in boxin:
# 		if box[2]>195 and box[2]<285:

# 			send_to_Main(f"Name:{box[0]},num:{box[1]},x:{box[2]},y:{box[3]}")
# 	last_send_time = time.time()
jiantou_num = [46, 13]  # 箭头类别编号

last_send_time = 0  # 新增的全局变量
center_x = 400  # 中心点的 x 坐标
object_map_num = [[42],[21,48],[38],[33]] 
goods_list_name = [[41,43,45,47],[24,27,34,35,36,37],[9]]
def Get_True_box(boxin,Is_ocr_finished):
    global last_time
   
    global last_send_time
    print("Get_True_box: Is_ocr_finished =", Is_ocr_finished)
    center_x_left=center_x-45
    center_x_right=center_x+45
    # if time.time() - last_send_time < 0.2:  # 至少间隔 0.5 秒才发一次
    #     return
    # 先过滤 x 轴范围
    
    if Is_ocr_finished == 0:
        filtered_boxes = [box for box in boxin if (center_x_left - 40 < box[2] < center_x_right + 40 ) and (420>box[3] > 30)]
        # filtered_boxes= [box for box in boxin]
        # print("所有：",boxin,"规定视野：",filtered_boxes)
        print("规定视野：",filtered_boxes)
        # 只发送箭头类目标
        arrow_boxes = [box for box in filtered_boxes if box[1] in jiantou_num]
        print("箭头：",arrow_boxes)
        if not arrow_boxes:
            send_to_Main("empty")
        else:
            for box in arrow_boxes:
                send_to_Main(f"Name:{box[0]},num:{box[1]},x:{box[2]},y:{box[3]}")
    elif Is_ocr_finished == 1:
        filtered_boxes = [box for box in boxin if (center_x_left - 20 < box[2] < center_x_right + 20) and (420>box[3] > 30)]
        # filtered_boxes= [box for box in boxin]
        # print("所有：",boxin,"规定视野：",filtered_boxes)
        print("规定视野：",filtered_boxes)
        # 分类 boxes
        normal_boxes = []
        arrow_boxes = []

        for box in filtered_boxes:
            if box[1] in jiantou_num:
                arrow_boxes.append(box)
            elif any(box[1] in sublist for sublist in object_map_num + goods_list_name):
                normal_boxes.append(box)

        # 保留有效的箭头 box
        valid_arrow_boxes = []
        for abox in arrow_boxes:
            conflict = False
            for nbox in normal_boxes:
                if abs(abox[2] - nbox[2]) <= 40:
                    conflict = True
                    break
            if not conflict:
                valid_arrow_boxes.append(abox)

        # 合并最终要发送的 box
        final_boxes = normal_boxes + valid_arrow_boxes
        # final_boxes = normal_boxes + arrow_boxes
        print("最终：",final_boxes)
        if not final_boxes:
            send_to_Main("empty")
        else:
            for box in final_boxes:
                send_to_Main(f"Name:{box[0]},num:{box[1]},x:{box[2]},y:{box[3]}")
    last_send_time = time.time()

connect_to_Main()

# !!!!!!!!!!!test!!!!!!!!!!
# while True:
# 	send_to_Main("yolo_get_in x:120,y:20")#发送给主程序数据
# 	time.sleep(1)




# client_socket = connect_to_Main()#连接定位程序反馈socket


# last_time=0
# box=[]

	
	
# def send(dir,height):
# 	dir=(str(640-dir)+' ').encode("utf-8")
# 	h_send=''
# 	height=int(480-(height))
# 	h_send=str(height).encode("utf-8")
# 	send_str=bytes([0xA5])+dir+h_send
# 	for i in range(9-len(h_send)-len(dir)-1):
# 		send_str+=bytes([0x5A])
# 	# print(send_str)
# 	se.write(send_str)
# 	print("发送",send_str)

# def sendStr(str):

# 	h_send=str.encode("utf-8")
# 	send_str=bytes([0xA5])+h_send

# 	for i in range(9-len(h_send)-1):
# 		send_str+=bytes([0x5A])

# 	se.write(send_str)
# 	print("发送",send_str)

# def Commuication():
# 	global box

# 	try:
# 		confirm_box=[]
# 		#筛选一遍box
# 		for i in range(len(box)):
# 		#box在一定范围内才发送，因为每次只能抓一格的东西	
# 			if(box[i][0]<520 and box[i][0]>90):
# 				confirm_box.append(box[i])
		
# 		if(len(confirm_box)==0):
# 			sendStr("None")
# 			return
# 		else:
# 			sendStr("start") 
# 			time.sleep(0.01)
# 			for i in range(len(confirm_box)):
# 			#box在一定范围内才发送，因为每次只能抓一格的东西	
# 				send(confirm_box[i][0],confirm_box[i][1])

# 			sendStr("over")
		
# 	except:
# 		return 


# # Get_True_box([ [366, 161],[263, 350],[479, 350]])
# #[160, 300], [320, 300],[320, 170], 
# #[366, 162],[263, 161]
# # sendStr("None") 
