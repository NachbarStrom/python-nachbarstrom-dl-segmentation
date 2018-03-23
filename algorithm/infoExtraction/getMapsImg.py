from io import BytesIO
from PIL import Image
from urllib import request
#import matplotlib.pyplot as plt # this is if you want to plot the map using pyplot

def satImgDownload(latCenter, lonCenter, num):

    map_img_url = "https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=%s,%s&zoom=18&size=400x400&key=AIzaSyBV6-jGq4ciojBHuKZJ7CZryniRKxJTlFE" % (latCenter, lonCenter)

    buffer = BytesIO(request.urlopen(map_img_url).read())
    image = Image.open(buffer)

    imgName = "Image/img_%s.png" % (num+18376)
    image.save(imgName)