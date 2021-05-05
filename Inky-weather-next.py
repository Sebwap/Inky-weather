import html
import requests
import datetime
from random import randint
from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto

def deg_to_direction(deg):
    direction=['N','NE','E','SE','S','SW','W','NW','N']
    return direction[round(deg/45)]


def wind_to_icon(direction):
    if direction=="N":
        return html.unescape('&#xf044;')
    if direction=="NE":
        return html.unescape('&#xf043;')
    if direction=="E":
        return html.unescape('&#xf048;')
    if direction=="SE":
        return html.unescape('&#xf087;')
    if direction=="S":
        return html.unescape('&#xf058;')
    if direction=="SW":
        return html.unescape('&#xf057')
    if direction=="W":
        return html.unescape('&#xf04d;')
    if direction=="NW":
        return html.unescape('&#xf088;')

    
def icon_to_char(icon):
    if icon=='01d':
        return html.unescape('&#xf00d;')
    if icon=='02d':
        return html.unescape('&#xf002;')
    if icon=='03d':
        return html.unescape('&#xf041;')
    if icon=='04d':
        return html.unescape('&#xf013;')
    if icon=='09d':
        return html.unescape('&#xf008;')
    if icon=='10d':
        return html.unescape('&#xf006;')
    if icon=='11d':
        return html.unescape('&#xf01e;')
    if icon=='13d':
        return html.unescape('&#xf076;')
    if icon=='50d':
        return html.unescape('&#xf063;')
    
    if icon=='01n':
        return html.unescape('&#xf02e;')
    if icon=='02n':
        return html.unescape('&#xf086;')
    if icon=='03n':
        return html.unescape('&#xf041;')
    if icon=='04n':
        return html.unescape('&#xf013;')
    if icon=='09n':
        return html.unescape('&#xf024;')
    if icon=='10n':
        return html.unescape('&#xf025;')
    if icon=='11n':
        return html.unescape('&#xf01e;')
    if icon=='13n':
        return html.unescape('&#xf076;')
    if icon=='50n':
        return html.unescape('&#xf063;')
    
def ts_to_date(ts,offset):
    return(datetime.datetime.utcfromtimestamp(ts+offset))


URL='https://api.openweathermap.org/data/2.5/onecall?lat=XXXXX&lon=XXXXX&appid=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX&units=metric&lang=fr'
# https://openweathermap.org/api/one-call-api pour avoir le détail de tous les champs possibles de la réponse
# police icone: https://erikflowers.github.io/weather-icons/
#

#requête
requete=requests.get(URL)

#parse json
reponse=requete.json()

###daily
##print("Jour par jour...")
##for item in reponse['daily']:
##    message=""
##    message+="Time: "+ts_to_date(item['dt'],reponse['timezone_offset']).strftime('%d/%m/%Y ')
##    message+="|"+str(item['temp'])+"°C"
##    #message+="|"+str(item['feels_like'])+"°C"
##    message+="|"+str(item['pressure'])+"hPa"
##    message+="|"+str(item['humidity'])+"%"
##    message+="|Cloud:"+str(item['clouds'])+"%"
##    message+="|Rain:"+str(round(100*item['pop']))+"%"
##    message+="|"+item['weather'][0]['description']
##    print(message)


# début
WIDTH=212
HEIGHT=104
WHITE=0
BLACK=1
RED=2

img = Image.new("P", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

fontTIME = ImageFont.truetype( "/home/pi/Inky-scripts/Ubuntu Nerd Font Complete.ttf",20)
fontDATE = ImageFont.truetype( "/home/pi/Inky-scripts/Ubuntu Nerd Font Complete.ttf",10)
fontTEMP=  ImageFont.truetype( "/home/pi/Inky-scripts/Ubuntu Nerd Font Complete.ttf",9)
icomini= ImageFont.truetype( "/home/pi/Inky-scripts/weathericons-regular-webfont.ttf",19)
icom= ImageFont.truetype( "/home/pi/Inky-scripts/weathericons-regular-webfont.ttf",9)

draw.line([0,10,212,10],fill=BLACK)

for i in range(7):
    #date
    message=ts_to_date(reponse['daily'][i+1]['dt'],reponse['timezone_offset']).strftime(' %d')
    jour= ts_to_date(reponse['daily'][i+1]['dt'],reponse['timezone_offset']).strftime('%u')

    if jour=="1":
        message="Lu"+message
    if jour=="2":
        message="Ma"+message
    if jour=="3":
        message="Me"+message
    if jour=="4":
        message="Je"+message
    if jour=="5":
        message="Ve"+message
    if jour=="6":
        message="Sa"+message
    if jour=="7":
        message="Di"+message
        
    x=i*26+27
    y = 0
    w,h=fontTEMP.getsize(message)

    x+=round((25-w)/2)
    draw.text((x, y), message, BLACK, fontTEMP)
    draw.line([i*26+28-1,10,i*26+28-1,104],fill=BLACK)

    #icone
    message=icon_to_char(reponse['daily'][i+1]['weather'][0]['icon'])
    x=i*26+30
    y = 10
    if reponse['daily'][i+1]['weather'][0]['icon']=="13n":
        x=x+2
    if reponse['daily'][i+1]['weather'][0]['icon']=="13d":
        x=x+2    
    draw.text((x, y), message, BLACK, icomini)

    #sunrise sunset
    message=ts_to_date(reponse['daily'][i+1]['sunrise'],reponse['timezone_offset']).strftime('%H:%M')
    x=i*26+28
    y = 32
    draw.text((x, y), message, BLACK, fontTEMP)    
    message=ts_to_date(reponse['daily'][i+1]['sunset'],reponse['timezone_offset']).strftime('%H:%M')
    x=i*26+28
    y = 42
    draw.text((x, y), message, BLACK, fontTEMP)

    #temp: min, max.
    message=str(round(reponse['daily'][i+1]['temp']['min']))+"°C"
    x=i*26+28
    y = 52
    draw.text((x, y), message, BLACK, fontTEMP)
    message=str(round(reponse['daily'][i+1]['temp']['max']))+"°C"
    x=i*26+28
    y = 62
    draw.text((x, y), message, BLACK, fontTEMP)

    #Wind
    message=str(round(3.6*reponse['daily'][i+1]['wind_speed']))
    x=i*26+28
    y = 72
    draw.text((x, y), message, BLACK, fontTEMP)
    message=wind_to_icon(deg_to_direction(reponse['daily'][i+1]['wind_deg']))
    x=(i+1)*26+28-12
    y = 65
    draw.text((x, y), message, BLACK, icomini)    
    
    #Pluie
    message=str(round(reponse['daily'][i+1]['pop']*100))+"%"
    x=i*26+28
    y = 82
    draw.text((x, y), message, BLACK, fontTEMP)

    #Clouds
    message=str(round(reponse['daily'][i+1]['clouds']))+"%"
    x=i*26+28
    y = 92
    draw.text((x, y), message, BLACK, fontTEMP)
    
# libellés
# soleil
message=html.unescape('&#xf051;')
x=0
y = 30
draw.text((x, y), message, BLACK, icomini) 
#temp
message=html.unescape('&#xf054;')
x=10
y = 48
draw.text((x, y), message, BLACK, icomini)
#vent
message=html.unescape('&#xf050;')
x=8
y = 71
draw.text((x, y), message, BLACK, icom)
#pluie
message=html.unescape('&#xf078;')
x =10
y = 82
draw.text((x, y), message, BLACK, icom)
#nuage
message=html.unescape('&#xf041;')
x =8
y = 92
draw.text((x, y), message, BLACK, icom)

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))


inky_display.set_border(inky_display.WHITE)

#img.putpalette([255,255,255,0,0,0,255,0,0], rawmode='RGB')
img = img.transpose(Image.ROTATE_180)
#img.show()

inky_display.set_image(img)
inky_display.show()
