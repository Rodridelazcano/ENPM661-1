import numpy as np
import sys
import cv2
import pylsd

def check_rectangle(point):
    
    x=point[0]
    y=point[1]

    
    coeff1=np.array(np.polyfit([95,100],[30,39],1))
    coeff2=np.array(np.polyfit([100,35],[39,77],1))
    coeff3=np.array(np.polyfit([35,30],[77,68],1))
    coeff4=np.array(np.polyfit([30,95],[68,30],1))
    line1 = round(y - coeff1[0] * x - coeff1[1])
    line2 = round(y - coeff2[0] * x - coeff2[1])
    line3 = round(y - coeff3[0] * x - coeff3[1])
    line4 = round(y - coeff4[0] * x - coeff4[1])

    if line1 >=0 and line2<=0 and line3<=0 and  line4>=0:
        return True
    else:
        return False



def check_rhombus(point):
    x=point[0]
    y=point[1]

    coeff1=np.array(np.polyfit([225,250],[10,25],1))
    coeff2=np.array(np.polyfit([250,225],[25,40],1))
    coeff3=np.array(np.polyfit([225,200],[40,25],1))
    coeff4=np.array(np.polyfit([200,225],[25,10],1))
    line1 = round(y - coeff1[0] * x - coeff1[1])
    line2 = round(y - coeff2[0] * x - coeff2[1])
    line3 = round(y - coeff3[0] * x - coeff3[1])
    line4 = round(y - coeff4[0] * x - coeff4[1])

    if line1 >=0 and line2<=0 and line3<=0 and  line4>=0:
        return True
    else:
        return False


def check_valid(initial_pos,final_pos):
	pass

def space():
	blank_image = 150*np.ones(shape=[200, 300, 1], dtype=np.uint8)

	cv2.circle(blank_image, (225, 50), 25, (0, 255, 0), 2)

	cv2.ellipse(blank_image, (150,100), (40, 20), 
           0, 0, 360, (0,255,0), 2) 

	rotrec = np.array([[[95,170],[95+5,170-9],[95+5-65,170-9 -38],[95-65,170-38]]], np.int32)
	weird_shape = np.array([[[25, 15], [75, 15], [100, 50], [75, 80], [50, 50], [20, 80]]], np.int32)
	rhombus = np.array([[[225,190], [250, 175], [225, 160], [200, 175]]], np.int32)

	cv2.polylines(blank_image, rotrec, True, (0,255,0),2)
	cv2.polylines(blank_image, weird_shape, True, (0,255,0) ,2)
	cv2.polylines(blank_image, rhombus, True, (0,255,0), 2)

	return blank_image


def check_move(act_number, current_pos, final_pos):

	temp_pos_x = current_pos[0]
	temp_pos_y = current_pos[1]

	if act_number==1:
		# Upwar ACTION
		# temp_pos_x = temp_pos_x + 1
		temp_pos_y = temp_pos_y - 1

	if act_number==2:
		# Top Right ACTION
		temp_pos_x = temp_pos_x + 1
		temp_pos_y = temp_pos_y - 1

	if act_number==3:
		# RIght ACTION
		temp_pos_x = temp_pos_x + 1
		# temp_pos_y = temp_pos_y - 1

	if act_number==4:
		# Bottom Right ACTION
		temp_pos_x = temp_pos_x + 1
		temp_pos_y = temp_pos_y + 1

	if act_number==5:
		# Bottom ACTION
		# temp_pos_x = temp_pos_x + 1
		temp_pos_y = temp_pos_y + 1

	if act_number==6:
		# Bottom Left ACTION
		temp_pos_x = temp_pos_x - 1
		temp_pos_y = temp_pos_y + 1

	if act_number==7:
		# Left ACTION
		temp_pos_x = temp_pos_x - 1
		# temp_pos_y = temp_pos_y - 1

	if act_number==8:
		# Top Left ACTION
		temp_pos_x = temp_pos_x - 1
		temp_pos_y = temp_pos_y - 1


	temp_pos = [temp_pos_x, temp_pos_y]

	dist = np.linalg.norm(np.array(final_pos)-np.array(temp_pos))

	return dist, temp_pos

def check_actions(current_pos, final_pos):

	cost_min = 1000
	chosen_act = 0
	temp_fin = list(current_pos)

	for i in range(0,7):
		
		cost, temp_pos = check_move(i, current_pos, final_pos)

		if cost<cost_min:
			cost_min = cost
			temp_fin = list(temp_pos)

	return cost_min, temp_fin


def check_valid(position, image):

	pass


def write_to_image(image, point):
	x = point[0]
	y = point[1]

	cv2.circle(image, (y, x), 1, (0, 255, 0), 2)

def main():

	img = space()
	# print(defset.shape)
	[xi, yi] = [78, 50]
	[xf, yf] = [130, 250]

	# [xi, yi] = input("Please enter the starting coordinates of your robot as [x , y]! \n")

	# [xf, yf] = input("Please enter the final coordinates of your robot as [x , y]!\n")

	initial_pos = [xi, yi]
	final_pos = [xf, yf]

	print("Chosen initial and final coordinates are, [{} {}] and [{} {}]".format(xi, yi, xf, yf))

	# check_valid(initial_pos, img)

	write_to_image(img, final_pos)

	current_pos = initial_pos

	cost = 1000

	while(cost) > 5:
		cost, temp_pos = check_actions(current_pos, final_pos)
		current_pos = list(temp_pos)
		write_to_image(img, current_pos)
		print(cost)

	cv2.imshow('Final', img)
	cv2.waitKey(0)


if __name__ == '__main__':
	main()

import numpy as np
import sys
import cv2

import math

def algorithm(image,xi,yi):

    visited=[]
    queue=[]
    visited_info=[]
    nodes_visited=[]
    cost_map=np.inf*np.ones((200,300))
    goal=[150,200]
    initial_pos = np.array([[xi, yi],[0,0]])

    queue.append(initial_pos)


    cost_map[initial_pos[0,0],initial_pos[0,1]]=0


    while queue:


        min=0

        for i in range(len(queue)):
            if cost_map[queue[min][0][0],queue[min][0][1]]>cost_map[queue[i][0][0],queue[i][0][1]]:
                min=i

        current_node=queue.pop(min)
        current_position=[current_node[0,0],current_node[0,1]]

        parent_position=[current_node[1,0],current_node[1,1]]

        visited_info.append(current_node)

        nodes_visited.append(str(current_node[0]))


        image[current_position[0],current_position[1]]=170
        resized_new_1 = cv2.resize(image, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Figure", resized_new_1)
        cv2.waitKey(1)


        for i in range (1,9):
            new_position,cost=check_move(i,current_position)


            if new_position is not False:
                if new_position==goal:
                    print("Reached")
                    return visited_info
                new_cost=cost_map[current_position[0],current_position[1]]+cost




                if str(new_position) not in nodes_visited and cost_map[new_position[0],new_position[1]]>new_cost:
                    queue.append(np.array([new_position,current_position]))
                    cost_map[new_position[0],new_position[1]]=new_cost

                    for i in range(len(queue)):

                        if str(queue[i][0])==str(new_position) and str(queue[i][1])!=str(current_position):

                            queue[i]=np.array([new_position,current_position])
                            queue.pop(len(queue)-1)

            else:
                continue
    return None






def check_rectangle(point):

    x=point[0]
    y=point[1]


    coeff1=np.array(np.polyfit([95,100],[30,39],1))
    coeff2=np.array(np.polyfit([100,35],[39,77],1))
    coeff3=np.array(np.polyfit([35,30],[77,68],1))
    coeff4=np.array(np.polyfit([30,95],[68,30],1))
    line1 = round(y - coeff1[0] * x - coeff1[1])
    line2 = round(y - coeff2[0] * x - coeff2[1])
    line3 = round(y - coeff3[0] * x - coeff3[1])
    line4 = round(y - coeff4[0] * x - coeff4[1])

    if line1 >=0 and line2<=0 and line3<=0 and  line4>=0:
        return True
    else:
        return False



def check_rhombus(point):
    x=point[0]
    y=point[1]

    coeff1=np.array(np.polyfit([225,250],[10,25],1))
    coeff2=np.array(np.polyfit([250,225],[25,40],1))
    coeff3=np.array(np.polyfit([225,200],[40,25],1))
    coeff4=np.array(np.polyfit([200,225],[25,10],1))
    line1 = round(y - coeff1[0] * x - coeff1[1])
    line2 = round(y - coeff2[0] * x - coeff2[1])
    line3 = round(y - coeff3[0] * x - coeff3[1])
    line4 = round(y - coeff4[0] * x - coeff4[1])

    if line1 >=0 and line2<=0 and line3<=0 and  line4>=0:
        return True
    else:
        return False



def space():
    blank_image = 150*np.ones(shape=[200, 300, 1], dtype=np.uint8)

    cv2.circle(blank_image, (225, 50), 25, (0, 255, 0), 2)

    cv2.ellipse(blank_image, (150,100), (40, 20), 
           0, 0, 360, (0,255,0), 2) 

    rotrec = np.array([[[95,170],[95+5,170-9],[95+5-65,170-9 -38],[95-65,170-38]]], np.int32)
    weird_shape = np.array([[[25, 15], [75, 15], [100, 50], [75, 80], [50, 50], [20, 80]]], np.int32)
    rhombus = np.array([[[225,190], [250, 175], [225, 160], [200, 175]]], np.int32)

    cv2.polylines(blank_image, rotrec, True, (0,255,0),2)
    cv2.polylines(blank_image, weird_shape, True, (0,255,0) ,2)
    cv2.polylines(blank_image, rhombus, True, (0,255,0), 2)

    return blank_image


def check_move(act_number, current_pos):

    temp_pos_x = current_pos[0]
    temp_pos_y = current_pos[1]

    if act_number==1:
        # Upwar ACTION
        # temp_pos_x = temp_pos_x + 1
        temp_pos_y = temp_pos_y - 1
        cost=1
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  

    if act_number==2:
        # Top Right ACTION
        temp_pos_x = temp_pos_x + 1
        temp_pos_y = temp_pos_y - 1
        cost=math.sqrt(2)
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  


    if act_number==3:
        # RIght ACTION
        temp_pos_x = temp_pos_x + 1
        # temp_pos_y = temp_pos_y - 1
        cost=1
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  

    if act_number==4:
        # Bottom Right ACTION
        temp_pos_x = temp_pos_x + 1
        temp_pos_y = temp_pos_y + 1
        cost=math.sqrt(2)
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  


    if act_number==5:
        # Bottom ACTION
        # temp_pos_x = temp_pos_x + 1
        temp_pos_y = temp_pos_y + 1
        cost=1
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  

    if act_number==6:
        # Bottom Left ACTION
        temp_pos_x = temp_pos_x - 1
        temp_pos_y = temp_pos_y + 1
        cost=math.sqrt(2)
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  
    if act_number==7:
        # Left ACTION
        temp_pos_x = temp_pos_x - 1
        # temp_pos_y = temp_pos_y - 1
        cost=1
        new_position=[temp_pos_x,temp_pos_y]
        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]  


    if act_number==8:
        # Top Left ACTION
        temp_pos_x = temp_pos_x - 1
        temp_pos_y = temp_pos_y - 1
        cost=math.sqrt(2)

        if check_movement(current_pos)==True:
            new_position=False
        else:
            new_position=[temp_pos_x,temp_pos_y]   

    if temp_pos_x<0 or temp_pos_x>300 or temp_pos_y<0 or temp_pos_y>200:
        new_position=False

    return new_position,cost


def check_movement(position):

    if check_rhombus(position)==True or check_rectangle(position)==True:
        return True
    return False





def main():

    img = space()
    # print(defset.shape)

    # [xi, yi] = input("Please enter the starting coordinates of your robot as [x , y]! \n")

    # [xf, yf] = input("Please enter the final coordinates of your robot as [x , y]!\n")



    algorithm(img,1,0)


    # check_valid(initial_pos, img)







    cv2.imshow('Final', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()






