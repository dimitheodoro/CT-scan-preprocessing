
!pip install  pydicom

import  pydicom as dcm
import matplotlib.pyplot as plt


CT_IMAGE='path_to_CT_image"

# Function to take care of teh translation and windowing. 
def window_image(img, window_center,window_width, intercept, slope, rescale=True):
    img = (img*slope +intercept) #for translation adjustments given in the dicom file. 
    img_min = window_center - window_width//2 #minimum HU level
    img_max = window_center + window_width//2 #maximum HU level
    img[img<img_min] = img_min #set img_min for all HU levels less than minimum HU level
    img[img>img_max] = img_max #set img_max for all HU levels higher than maximum HU level
    if rescale: 
        img = (img - img_min) / (img_max - img_min)*255.0 
    return img
    
def get_first_of_dicom_field_as_int(x):
    #get x[0] as in int is x is a 'pydicom.multival.MultiValue', otherwise get int(x)
    if type(x) == dcm.multival.MultiValue: return int(x[0])
    else: return int(x)
    
def get_windowing(data):
    dicom_fields = [data[('0028','1050')].value, #window center
                    data[('0028','1051')].value, #window width
                    data[('0028','1052')].value, #intercept
                    data[('0028','1053')].value] #slope
    return [get_first_of_dicom_field_as_int(x) for x in dicom_fields]


def view_images(file):
    data = dcm.read_file(file)
    image = data.pixel_array
    window_center , window_width, intercept, slope = get_windowing(data)  
    print(window_center , window_width, intercept, slope )
    plt.figure(figsize=(15,15))
    plt.imshow(image,cmap='gray')
    plt.show()
    plt.figure(figsize=(15,15))
    plt.imshow(window_image(image,window_center , window_width, intercept, slope ),cmap='gray')
    plt.show()



view_images(CT_IMAGE)





