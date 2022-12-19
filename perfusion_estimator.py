#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODE FOR NIVEDITA AKKA'S PROJECT

Created on Sat Oct  1 11:32:14 2022

@author: Mr. Rohan Raju Dhanakshirur
@Designation: Project Scientist and PhD scholar
@Institution: IIT Delhi
@Contact Details: rohanrd@cse.iitd.ac.in 
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



################## Function to read the filename from the GUI ##################
def openfilename():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title ='"pen')
    return filename

################## Function to rotate image. It basically forms a warp matrix and uses it ##################
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

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

################## Function to add empty labels: Text, value and area ##################
def print_empty(random_num):
    lbl = Label(root, text="                                            ", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 160)
    add_label(str('         '),str('        '), "                                        ", 190, "green")
    add_label(str('         '),str('        '), "                                        ", 220, "green")
    add_label(str('         '),str('        '), "                                        ", 250, "green")
    add_label(str('         '),str('        '), "                                        ", 280, "green")
    add_label(str('         '),str('        '), "                                        ", 310, "green")
    add_label(str('         '),str('        '), "                                        ", 340, "green")
    
################## Functions to find the score of pixel: Thresholds are 40 and 280 ##################
def negative_pixel(hue_con):
    answer = 1-(hue_con-40)/240
    return answer*100

################## Function to find score of image ##################
################## Converts image to HSV and thresholds "hue" channel to get score ################## 
def get_score(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    sh = image.shape
    consider_pixels = 0
    total_pxel_sum = 0
    total_imp_pixels = 0
    for i in range(sh[0]):
        for j in range(sh[1]):
            pixel = image[i,j,:]
            pixel_val = sum(pixel)
            if pixel_val>15:
                hue_con = image_hsv[i,j,0]
                if hue_con>40 and hue_con<280:
                    total_pxel_sum += negative_pixel(hue_con)
                    consider_pixels+=1
                total_imp_pixels+=1
            
    return total_pxel_sum/consider_pixels, consider_pixels/total_imp_pixels*100

################## Function to devide image into half and score each parts ##################
################## It does everything for two parts of images ##################                
def one():
    global angle
    global roi
    global x
    global file_to_be_saved
    global panel
    
    img_raw = cv2.imread(x)
    img_raw = rotate_image(img_raw, angle)
        
    ######################## Generate two planes #############################
    roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    s = roi_cropped.shape
    first_half = roi_cropped[:,0:s[1]//2,:]
    second_half = roi_cropped[:,s[1]//2:s[1],:]
    ##########################################################################
    
    # ################ Check if the generated images are correct ################
    # cv2.imwrite('first_half.png',first_half)
    # cv2.imwrite('second_half.png',second_half)
    # ###########################################################################
    
    ####################### Get scores #######################################
    score_first_half,area_first = get_score(first_half)
    score_second_half,area_second = get_score(second_half)
    print(score_first_half)
    print(score_second_half)
    ###########################################################################
    
    ####################### Display results ###################################
    print_empty(0)
    lbl = Label(root, text="You have selected: One", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 160)
    add_label(str(round(area_first,2)),str(round(score_first_half,2)), "Result of VB Right = ", 190, "green",1)
    add_label(str(round(area_second,2)),str(round(score_second_half,2)), "Result of VB Left = ", 220, "green",1)
    # add_label(str(0),str(0), "Result of Third Part = ", 250, "green",1)
    # add_label(str(0),str(0), "Result of Fourth Part = ", 280, "green",1)
    ###########################################################################
    
    ###################### Save results #######################################
    filename = x[:-4]+'_one.txt'
    f = open(filename,'w')
    for index1 in file_to_be_saved:
        f.write(index1)
        f.write('\n')
    f.write('\n')
    f.write("You have chosen: One \n")
    f.write("Result of VB Right = "+str(round(score_first_half,2))+'\t Area = '+ str(round(area_first,2))+'\n')
    f.write("Result of VB Left = "+str(round(score_second_half,2))+'\t Area = '+ str(round(area_second,2))+'\n')
    f.close()
    ###########################################################################
    
    ########### Visualization code ########### 
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2],roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2]//2,roi[1]+roi[3]),(255,0,0),3)
    x_temp = x.split('/')
    x_temp_img = ""
    for i in range(len(x_temp)-1):
        x_temp_img+=x_temp[i]
        x_temp_img+='/'
    x_temp_img+='temp_myimg.png'
    cv2.imwrite(x_temp_img,img_vis)
    cv2.imwrite('temp.png',img_vis)
    ########### Visualization code ########### 
    
    ########### Visualization display ########### 
    
    img2 = Image.open(x_temp_img)
    img2.thumbnail((250,400), Image.ANTIALIAS)
    # PhotoImage class is used to add image to widgets, icons etc
    img2 = ImageTk.PhotoImage(img2)

    #create a label
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img2)


    # set the image as img
    panel.image = img2
    panel.grid(row = 5,column=1)
    os.remove(x_temp_img)
    ########### Visualization display ########### 


################## Function to devide image into four parts (MCA, PCA) and score each parts ##################
################## It does everything for all four parts of images ##################   

def two():
    global angle
    global roi
    global x
    global panel
    
    img_raw = cv2.imread(x)
    img_raw = rotate_image(img_raw, angle)
    
    ################ Generate two planes ####################################
    roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    s = roi_cropped.shape
    first_half = roi_cropped[:,0:s[1]//2,:]
    second_half = roi_cropped[:,s[1]//2:s[1],:]
    s1 = first_half.shape
    s2 = second_half.shape
    ##########################################################################
    
    ################ Generate four parts #####################################
    first_part = first_half[:,0:2*s1[1]//3,:]
    # second_part = first_half[:,2*s1[1]//3:s1[1],:]
    # third_part = second_half[:,0:1*s2[1]//3,:]
    fourth_part = second_half[:,1*s2[1]//3:s2[1],:]
    sfi = first_part.shape
    sfo = fourth_part.shape
    MCA_r = first_part[0:2*sfi[0]//3,:,:]
    MCA_l = fourth_part[0:2*sfo[0]//3,:,:]
    PCA_r = copy.deepcopy(first_half)
    PCA_r[0:2*sfi[0]//3,0:sfi[1],0:sfi[2]] = np.uint8(np.zeros([2*sfi[0]//3,sfi[1],sfi[2]]))
    PCA_l = copy.deepcopy(second_half)
    PCA_l[0:2*s2[0]//3,s2[1]//3:s2[1],0:s2[2]] = np.uint8(np.zeros([2*sfo[0]//3,sfo[1],sfi[2]]))
    #########################################################################
    
    # ################ Check if the generated images are correct ################
    # cv2.imwrite('MCA_r.png',MCA_r)
    # cv2.imwrite('MCA_l.png',MCA_l)
    # cv2.imwrite('PCA_r.png',PCA_r)
    # cv2.imwrite('PCA_l.png',PCA_l)
    # ###########################################################################
    
    ################ Score four parts #######################################
    score_first_part,area_1 = get_score(MCA_r)
    score_second_part,area_2 = get_score(PCA_r)
    score_third_part,area_3 = get_score(PCA_l)
    score_fourth_part,area_4 = get_score(MCA_l)
    #########################################################################
    
    ################ Display results ########################################
    print_empty(0)
    lbl = Label(root, text="You have selected: two", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 160)
    add_label(str(round(area_1,2)),str(round(score_first_part,2)), "Result of MCA Right = ", 190, "green",1)
    add_label(str(round(area_2,2)),str(round(score_second_part,2)), "Result of PCA Right = ", 220, "green",1)
    add_label(str(round(area_3,2)),str(round(score_third_part,2)), "Result of PCA Left = ", 250, "green",1)
    add_label(str(round(area_4,2)),str(round(score_fourth_part,2)), "Result of MCA Left = ", 280, "green",1)
    ########################################################################
    
    ################# Save Results #########################################
    filename = x[:-4]+'_two.txt'
    f = open(filename,'w')
    for index1 in file_to_be_saved:
        f.write(index1)
        f.write('\n')
    f.write('\n')
    f.write("You have chosen: Two \n")
    f.write("Result of MCA Right = "+str(round(score_first_part,2))+'\t Area = '+ str(round(area_1,2))+'\n')
    f.write("Result of PCA Riht = "+str(round(score_second_part,2))+'\t Area = '+ str(round(area_2,2))+'\n')
    f.write("Result of PCA Left = "+str(round(score_third_part,2))+'\t Area = '+ str(round(area_3,2))+'\n')
    f.write("Result of MCA Left = "+str(round(score_fourth_part,2))+'\t Area = '+ str(round(area_4,2))+'\n')
    f.close()
    ########################################################################
    
    ########### Visualization code ############
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2],roi[1]+roi[3]),(255,0,0),3)
    # img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+2*roi[2]//6,roi[1]+roi[3]),(255,0,0),3)
    # img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+2*roi[2]//3,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2]//2,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw, (roi[0],roi[1]), (roi[0]+roi[2]//3,roi[1]+2*roi[3]//3), (255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0]+2*roi[2]//3,roi[1]),(roi[0]+roi[2],roi[1]+2*roi[3]//3),(255,0,0),3)
    x_temp = x.split('/')
    x_temp_img = ""
    for i in range(len(x_temp)-1):
        x_temp_img+=x_temp[i]
        x_temp_img+='/'
    x_temp_img+='temp_myimg.png'
    cv2.imwrite(x_temp_img,img_vis)
    ########### Visualization code ############
    
    ########### Image Visualization display ########### 
    
    img2 = Image.open(x_temp_img)
    img2.thumbnail((250,400), Image.ANTIALIAS)
    # PhotoImage class is used to add image to widgets, icons etc
    img2 = ImageTk.PhotoImage(img2)

    #create a label
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img2)


    # set the image as img
    panel.image = img2
    panel.grid(row = 5,column=1)
    os.remove(x_temp_img)
    ########### Visualization display ########### 
################## Function to devide image into six parts (MCA, ACA) and score each parts ##################
################## It does everything for all six parts of images ##################     
def three():
    global angle
    global roi
    global x
    global panel
    
    img_raw = cv2.imread(x)
    img_raw = rotate_image(img_raw, angle)
    
    ############# Generate two planes #####################################
    roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    s = roi_cropped.shape
    first_half = roi_cropped[:,0:s[1]//2,:]
    second_half = roi_cropped[:,s[1]//2:s[1],:]
    s1 = first_half.shape
    s2 = second_half.shape
    #######################################################################
    
    ############## Generate six parts #####################################
    first_part = first_half[:,0:2*s1[1]//3,:]
    second_part = first_half[:,2*s1[1]//3:s1[1],:]
    s3 = second_part.shape
    first_second_part = second_part[0:s3[0]//3,:,:]
    second_second_part = second_part[2*s[0]//3:s[0],:,:]
    third_part = second_half[:,0:1*s2[1]//3,:]
    s4 = third_part.shape
    first_third_part = third_part[0:s4[0]//3,:,:]
    second_third_part = third_part[2*s4[0]//3:s4[0],:,:]
    fourth_part = second_half[:,1*s2[1]//3:s2[1],:]
    #######################################################################
    
    # ################ Check if the generated images are correct ################
    # cv2.imwrite('third_MCA_r.png',first_part)
    # cv2.imwrite('third_PCA_r_1.png',first_second_part)
    # cv2.imwrite('third_PCA_r_2.png',second_second_part)
    # cv2.imwrite('third_PCA_l_1.png',first_third_part)
    # cv2.imwrite('third_PCA_l_2.png',second_third_part)
    # cv2.imwrite('third_MCA_l.png',fourth_part)
    # ###########################################################################
    
    ############ Get scores for six parts #################################
    score_first_part,area_1 = get_score(first_part)
    score_first_second_part,area_2a = get_score(first_second_part)
    score_second_second_part,area_2b = get_score(second_second_part)
    score_first_third_part,area_3a = get_score(first_third_part)
    score_second_third_part,area_3b = get_score(second_third_part)
    score_fourth_part,area_4 = get_score(fourth_part)
    #######################################################################
    
    ########### Display results #########################################
    print_empty(0)
    lbl = Label(root, text="You have selected: Three", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 160)
    add_label(str(round(area_1,2)),str(round(score_first_part,2)), "Result of MCA Right = ", 190, "green",1)
    add_label(str(round(area_2a,2)),str(round(score_first_second_part,2)), "Result of ACA Right 1 = ", 220, "green",1)
    add_label(str(round(area_2b,2)),str(round(score_second_second_part,2)), "Result of ACA Right 2 = ", 250, "green",1)
    add_label(str(round(area_3a,2)),str(round(score_first_third_part,2)), "Result of ACA Left 1 = ", 280, "green",1)
    add_label(str(round(area_3b,2)),str(round(score_second_third_part,2)), "Result of ACA Left 2 = ", 310, "green",1)
    add_label(str(round(area_4,2)),str(round(score_fourth_part,2)), "Result of MCA Left = ", 340, "green",1)
    #######################################################################
    
    ############ Save results #############################################
    filename = x[:-4]+'_three.txt'
    f = open(filename,'w')
    for index1 in file_to_be_saved:
        f.write(index1)
        f.write('\n')
    f.write('\n')
    f.write("You have chosen: Three \n")
    f.write("Result of MCA Right = "+str(round(score_first_part,2))+'\t Area = '+ str(round(area_1,2))+'\n')
    f.write("Result of ACA Riht 1= "+str(round(score_first_second_part,2))+'\t Area = '+ str(round(area_2a,2))+'\n')
    f.write("Result of ACA Riht 2= "+str(round(score_second_second_part,2))+'\t Area = '+ str(round(area_2b,2))+'\n')
    f.write("Result of ACA Left 1= "+str(round(score_first_third_part,2))+'\t Area = '+ str(round(area_3a,2))+'\n')
    f.write("Result of ACA Left 2= "+str(round(score_second_third_part,2))+'\t Area = '+ str(round(area_3b,2))+'\n')
    f.write("Result of ACA Left = "+str(round(score_fourth_part,2))+'\t Area = '+ str(round(area_4,2))+'\n')
    f.close()
    #######################################################################
    
    ########### Visualization code ############
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2],roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+2*roi[2]//6,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+2*roi[2]//3,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2]//2,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0]+roi[2]//3,roi[1]),(roi[0]+2*roi[2]//3,roi[1]+roi[3]//3),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0]+roi[2]//3,roi[1]+2*roi[3]//3),(roi[0]+2*roi[2]//3,roi[1]+roi[3]),(255,0,0),3)
    x_temp = x.split('/')
    x_temp_img = ""
    for i in range(len(x_temp)-1):
        x_temp_img+=x_temp[i]
        x_temp_img+='/'
    x_temp_img+='temp_myimg.png'
    cv2.imwrite(x_temp_img,img_vis)
    ########### Visualization code ############
    
    ########### Visualization display ########### 
    
    img2 = Image.open(x_temp_img)
    img2.thumbnail((250,400), Image.ANTIALIAS)
    # PhotoImage class is used to add image to widgets, icons etc
    img2 = ImageTk.PhotoImage(img2)

    #create a label
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img2)


    # set the image as img
    panel.image = img2
    panel.grid(row = 5,column=1)
    os.remove(x_temp_img)
    ########### Visualization display ########### 

################## Function to devide image into four vertical parts and score each parts ##################
################## It does everything for four parts of images ##################     
def four():
    global angle
    global roi
    global x
    global panel
    
    img_raw = cv2.imread(x)
    img_raw = rotate_image(img_raw, angle)
    
    ################ Generate two planes ####################################
    roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    s = roi_cropped.shape
    first_half = roi_cropped[:,0:s[1]//2,:]
    second_half = roi_cropped[:,s[1]//2:s[1],:]
    s1 = first_half.shape
    s2 = second_half.shape
    ##########################################################################
    
    ################ Generate four parts #####################################
    first_part = first_half[:,0:2*s1[1]//3,:]
    second_part = first_half[:,2*s1[1]//3:s1[1],:]
    third_part = second_half[:,0:1*s2[1]//3,:]
    fourth_part = second_half[:,1*s2[1]//3:s2[1],:]
    #########################################################################
    
    # ################ Check if the generated images are correct ################
    # cv2.imwrite('fourth_MCA_r.png',first_part)
    # cv2.imwrite('fourth_ACA_r.png',second_part)
    # cv2.imwrite('fourth_ACA_l.png',third_part)
    # cv2.imwrite('fourth_MCA_l.png',fourth_part)
    # ###########################################################################
    
    ################ Score four parts #######################################
    score_first_part,area_1 = get_score(first_part)
    score_second_part,area_2 = get_score(second_part)
    score_third_part,area_3 = get_score(third_part)
    score_fourth_part,area_4 = get_score(fourth_part)
    #########################################################################
    
    ################ Display results ########################################
    print_empty(0)
    lbl = Label(root, text="You have selected: Four", fg="green", font=("Helvetica", 16))
    lbl.place(x  = 350,y = 160)
    add_label(str(round(area_1,2)),str(round(score_first_part,2)), "Result of MCA Right = ", 190, "green",1)
    add_label(str(round(area_2,2)),str(round(score_second_part,2)), "Result of ACA Right = ", 220, "green",1)
    add_label(str(round(area_3,2)),str(round(score_third_part,2)), "Result of ACA Left = ", 250, "green",1)
    add_label(str(round(area_4,2)),str(round(score_fourth_part,2)), "Result of MCA Left = ", 280, "green",1)
    ########################################################################
    
    ################# Save Results #########################################
    filename = x[:-4]+'_four.txt'
    f = open(filename,'w')
    for index1 in file_to_be_saved:
        f.write(index1)
        f.write('\n')
    f.write('\n')
    f.write("You have chosen: Four \n")
    f.write("Result of MCA Right = "+str(round(score_first_part,2))+'\t Area = '+ str(round(area_1,2))+'\n')
    f.write("Result of ACA Riht = "+str(round(score_second_part,2))+'\t Area = '+ str(round(area_2,2))+'\n')
    f.write("Result of ACA Left = "+str(round(score_third_part,2))+'\t Area = '+ str(round(area_3,2))+'\n')
    f.write("Result of MCA Left = "+str(round(score_fourth_part,2))+'\t Area = '+ str(round(area_4,2))+'\n')
    f.close()
    ########################################################################
    
    ########### Visualization code ############
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2],roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+2*roi[2]//6,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+2*roi[2]//3,roi[1]+roi[3]),(255,0,0),3)
    img_vis = cv2.rectangle(img_raw,(roi[0],roi[1]),(roi[0]+roi[2]//2,roi[1]+roi[3]),(255,0,0),3)
    x_temp = x.split('/')
    x_temp_img = ""
    for i in range(len(x_temp)-1):
        x_temp_img+=x_temp[i]
        x_temp_img+='/'
    x_temp_img+='temp_myimg.png'
    cv2.imwrite(x_temp_img,img_vis)
    ########### Visualization code ############
    
    ########### Image Visualization display ########### 
    
    img2 = Image.open(x_temp_img)
    img2.thumbnail((250,400), Image.ANTIALIAS)
    # PhotoImage class is used to add image to widgets, icons etc
    img2 = ImageTk.PhotoImage(img2)

    #create a label
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img2)


    # set the image as img
    panel.image = img2
    panel.grid(row = 5,column=1)
    os.remove(x_temp_img)
    ########### Visualization display ########### 

################## Function to call half, horizontal and vertical based on user's choice ##################
def evaluate():
    print("Hi")
    global x
    global angle
    global roi
    global file_to_be_saved
    
    img_raw = cv2.imread(x)
    img_raw = rotate_image(img_raw, angle)

    #select ROI function
    roi = cv2.selectROI(img_raw)
    #print rectangle points of selected roi
    print(roi)
    roi_str = [str(i) for i in roi]
    roi_str_save = ""
    for index in roi_str:
        roi_str_save+=index
        roi_str_save+='\t'
    file_to_be_saved.append(str(angle))
    file_to_be_saved.append(roi_str_save)

    lbl_spl = Button(root, text = 'One',command = one)
    lbl_spl.place(x=350, y=70)
    lbl_spl1 = Button(root, text = 'Two',command = two)
    lbl_spl1.place(x=450, y=70)
    lbl_spl2 = Button(root, text = 'Three',command = three)
    lbl_spl2.place(x=350, y=100)
    lbl_spl3 = Button(root, text = 'four',command = four)
    lbl_spl3.place(x=450, y=100)
    print_empty(0)
    #hold window
    k = cv2.waitKey(0)
    if k==27:
        cv2.destroyAllWindows()

################## Function to rotate image in anti-clockwise direction ##################
def plus():
    global angle
    global x
    global panel
    
    img1 = Image.open(x)
    img1.thumbnail((250,400), Image.ANTIALIAS)
    angle+=5
    if angle>360:
        angle = angle%360
    print(angle)
    img1 = ImageTk.PhotoImage(img1.rotate(angle))
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img1)
    panel.image = img1
    panel.grid(row = 5,column=1)

################## Function to rotate image in clockwise direction ##################
def minus():
    global angle
    global x
    global panel
    
    img1 = Image.open(x)
    img1.thumbnail((250,400), Image.ANTIALIAS)
    angle-=5
    if angle<0:
        angle = 360+angle
    print(angle)
    img1 = ImageTk.PhotoImage(img1.rotate(angle))
    if panel:
        panel.image = None
        panel.grid(row = 5,column=1)
    panel = Label(root, image = img1)
    panel.image = img1
    panel.grid(row = 5,column=1)
 
################## Function to Load the image and display it ##################
def open_img():
    # Select the Imagename  from a folder
    global panel
    global x
    global file_to_be_saved
    file_to_be_saved = []
    x = openfilename()
    file_to_be_saved.append(x)
    img1 = Image.open(x)
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
    btn = Button(root, text = '+',command = plus).grid(row = 7,columnspan = 2)
    btn1= Button(root, text = '-',command = minus).grid(row = 7,columnspan = 1)
    btn = Button(root, text = 'Annotate',command = evaluate).grid(row = 8,columnspan = 2)
    print_empty(0)



################## ACTUAL GUI CODE ##################

# Create a windoe
root = Tk()
# Set Title as Image Loader
root.title("Nivedita Akka")

# Set the resolution of window
root.geometry("700x470+300+300")

# Allow Window to be resizable
root.resizable(width = True, height = True)
# lbl_m=Label(root, text="NETS LAB, AIIMS and Department of CSE, IIT- Delhi's ", fg='black', font=("Helvetica", 25),anchor="center")
# lbl_m.grid(row = 1,columnspan = 20)

lbl_m=Label(root, text="System for Nivedita Akka's Project", fg='black', font=("Helvetica", 25),anchor="center")
lbl_m.grid(row = 1,columnspan = 20)
# Create a button and place it into the window using grid layout
btn = Button(root, text ='open image', command = open_img).grid(row = 4,columnspan = 2)
root.mainloop()

###################################################