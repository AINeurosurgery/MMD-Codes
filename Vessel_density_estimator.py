#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 16:30:20 2022

@author: rohan
"""
##################Import Libraries ######################
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
from tkinter import filedialog,Label,Button,Tk
import copy

################## Global Variable Declaration ##################
device = "cpu"
panel = None
angle = 0
roi = []
file_to_be_saved = []
list_of_indices = []
#This will display all the available mouse click events  
events = [i for i in dir(cv2) if 'EVENT' in i]
print(events)

#This variable we use to store the pixel location
refPt = []
################## Function to read the filename from the GUI ##################
def openfilename():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title ='"pen')
    return filename

################## Function to add labels: Text, value and area ##################
def add_label(area,pred, text, y, color,choice=0):
    lbl = Label(root, text=text, fg=color, font=("Helvetica", 16))
    lbl.place(x  = 350,y = y)
    lbl2 = Label(root, text=pred+'   ', fg=color, font=("Helvetica", 16))
    lbl2.place(x  = 520,y = y)
    if choice ==1:
        lbl2 = Label(root, text="Area", fg=color, font=("Helvetica", 16))
        lbl2.place(x  = 570,y = y)
        lbl2 = Label(root, text=area+'%', fg=color, font=("Helvetica", 16))
        lbl2.place(x  = 620,y = y)
    else:
        lbl2 = Label(root, text="           ", fg=color, font=("Helvetica", 16))
        lbl2.place(x  = 570,y = y)
        lbl2 = Label(root, text=area+'         ', fg=color, font=("Helvetica", 16))
        lbl2.place(x  = 620,y = y)
        
        
def print_empty(random_num):
    lbl = Label(root, text="                                            ", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 160)
    add_label(str('         '),str('        '), "                                        ", 190, "green")
    add_label(str('         '),str('        '), "                                        ", 220, "green")
    add_label(str('         '),str('        '), "                                        ", 250, "green")
    add_label(str('         '),str('        '), "                                        ", 280, "green")
    add_label(str('         '),str('        '), "                                        ", 310, "green")
    add_label(str('         '),str('        '), "                                        ", 340, "green")


def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect
def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = pts
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped


def click_event(event, x, y, flags, param):
    global filename_var
    new_name1 = ""
    temp_new_name = filename_var.split('/')
    for iterator in range(len(temp_new_name)-1):
        new_name1+=temp_new_name[iterator]
        new_name1+='/'
    new_name1+="temp_"
    new_name1+=temp_new_name[-1]
    img = cv2.imread(new_name1)
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        list_of_indices.append([x,y])
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.putText(img, strXY, (x,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("image", img)
        cv2.imwrite(new_name1,img)

    if event == cv2.EVENT_RBUTTONDOWN:
        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        strBGR = str(blue)+", "+str(green)+","+str(red)
        cv2.putText(img, strBGR, (x,y), font, 0.5, (0,255,255), 2)
        cv2.imshow("image", img)
        
def warping_function():
    global filename_var
    global angle
    global roi
    global file_to_be_saved
    global list_of_indices
    img_raw = cv2.imread(filename_var)
    pts = np.array(list_of_indices,dtype="float32")
    
    warped = four_point_transform(img_raw, pts)
    new_name = ""
    temp_new_name = filename_var.split('/')
    for iterator in range(len(temp_new_name)-1):
        new_name+=temp_new_name[iterator]
        new_name+='/'
    new_name+="warped_"
    new_name+=temp_new_name[-1]
    cv2.imwrite(new_name,warped)     
    f = open(new_name[:-4]+'.txt','w')
    f.write(filename_var)
    f.write("\n")
    for i in list_of_indices:
        for j in i:
            f.write(str(j))
            f.write('\t')
        f.write('\n')
    f.close()
    lbl = Label(root, text="Image warped", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 190)
    
    new_name1 = ""
    temp_new_name = filename_var.split('/')
    for iterator in range(len(temp_new_name)-1):
        new_name1+=temp_new_name[iterator]
        new_name1+='/'
    new_name1+="temp_"
    new_name1+=temp_new_name[-1]
    os.remove(new_name1)
    Image = warped
    I1 = cv2.Canny(Image, 10, 240)
    I2,I2_out = cv2.connectedComponents(I1)
    lbl = Label(root, text="Vessel Density = "+str(I2), fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 220)
################## Function to call half, horizontal and vertical based on user's choice ##################
def evaluate():
    print("Hi")
    global filename_var
    global angle
    global roi
    global file_to_be_saved
    global list_of_indices
    
    img_raw = cv2.imread(filename_var)
    
    new_name1 = ""
    temp_new_name = filename_var.split('/')
    for iterator in range(len(temp_new_name)-1):
        new_name1+=temp_new_name[iterator]
        new_name1+='/'
    new_name1+="temp_"
    new_name1+=temp_new_name[-1]
    cv2.imwrite(new_name1,img_raw)
    #img_raw = rotate_image(img_raw, angle)
    cv2.imshow("image", img_raw)

    #calling the mouse click event
    
    
    cv2.setMouseCallback("image", click_event)
    
    

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #select ROI function
    #roi = cv2.selectROI(img_raw)
    #print rectangle points of selected roi
    #print(roi)
    #roi_str = [str(i) for i in roi]
    #roi_str_save = ""
    # for index in roi_str:
    #     roi_str_save+=index
    #     roi_str_save+='\t'
    # file_to_be_saved.append(str(angle))
    # file_to_be_saved.append(roi_str_save)

    lbl_spl = Button(root, text = 'Warp',command = warping_function)
    lbl_spl.place(x=350, y=70)
    # lbl_spl1 = Button(root, text = 'Two',command = two)
    # lbl_spl1.place(x=450, y=70)
    # lbl_spl2 = Button(root, text = 'Three',command = three)
    # lbl_spl2.place(x=350, y=100)
    # lbl_spl3 = Button(root, text = 'four',command = four)
    # lbl_spl3.place(x=450, y=100)
    # print_empty(0)
    #hold window
    k = cv2.waitKey(0)
    if k==27:
        cv2.destroyAllWindows()


 
################## Function to Load the image and display it ##################
def open_img():
    # Select the Imagename  from a folder
    global panel
    global filename_var
    global file_to_be_saved
    global list_of_indices
    list_of_indices = []
    file_to_be_saved = []
    filename_var = openfilename()
    file_to_be_saved.append(filename_var)
    img1 = Image.open(filename_var)
    img1.thumbnail((250,400), Image.ANTIALIAS)
    # PhotoImage class is used to add image to widgets, icons etc
    img1 = ImageTk.PhotoImage(img1)

    #create a label
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img1)


    # set the image as img
    panel.image = img1
    panel.grid(row = 5,column=1)
    # btn = Button(root, text = '+',command = plus).grid(row = 7,columnspan = 2)
    # btn1= Button(root, text = '-',command = minus).grid(row = 7,columnspan = 1)
    btn = Button(root, text = 'Annotate',command = evaluate).grid(row = 8,columnspan = 2)
    print_empty(0)



################## ACTUAL GUI CODE ##################

# Create a windoe
root = Tk()
# Set Title as Image Loader
root.title("Metric correction of Images")

# Set the resolution of window
root.geometry("700x470+300+300")

# Allow Window to be resizable
root.resizable(width = True, height = True)
# lbl_m=Label(root, text="NETS LAB, AIIMS and Department of CSE, IIT- Delhi's ", fg='black', font=("Helvetica", 25),anchor="center")
# lbl_m.grid(row = 1,columnspan = 20)

lbl_m=Label(root, text="System for Vessel Density Estimation", fg='black', font=("Helvetica", 25),anchor="center")
lbl_m.grid(row = 1,columnspan = 20)
# Create a button and place it into the window using grid layout
btn = Button(root, text ='open image', command = open_img).grid(row = 4,columnspan = 2)
root.mainloop()

###################################################