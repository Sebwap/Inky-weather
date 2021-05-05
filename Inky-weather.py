import html
import requests
import datetime
from random import randint
from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto

def display_future(i):
    if i==1:
        xs=0
        ys=56
    if i==4:
        xs=72
        ys=56        
    if i==7:
        xs=143
        ys=56           
    if i==10:
        xs=0
        ys=80         
    if i==13:
        xs=72
        ys=80         
    if i==16:
        xs=143
        ys=80

    #heure icone, temp, prop pluie
    message=ts_to_date(reponse['hourly'][i]['dt'],reponse['timezone_offset']).strftime('%H:%M')
    w, h = fontTEMP.getsize(message)
    x =xs
    y = ys-2
    draw.text((x, y), message, BLACK, fontTEMP)
    
    message=str(round(reponse['hourly'][i]['temp'],1))+"°C"
    w, h = fontTEMP.getsize(message)
    x =xs
    y = ys+6
    draw.text((x, y), message, BLACK, fontTEMP)

    message=html.unescape('&#xf078;')
    x =xs+1
    y = ys+13
    draw.text((x, y), message, BLACK, icomini)
    
    message=":"+str(round(reponse['hourly'][i]['pop']*100))+"%"
    w, h = fontTEMP.getsize(message)
    x =xs+7
    y = ys+13
    draw.text((x, y), message, BLACK, fontTEMP)

    message=icon_to_char(reponse['hourly'][i]['weather'][0]['icon'])
    w, h = ico.getsize(message)
    x =xs+32
    y = ys-6
    draw.text((x, y), message, BLACK, icomoy)    
    
def deg_to_direction(deg):
    direction=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N']
    return direction[round(deg/22.5)]

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

def draw_rain_next_hour():
    draw.rectangle([0,43,204,53],outline=BLACK,width=1)

    #chargement des images
    low_rain= Image.open('/home/pi/Images/low_rain.png')
    high_rain= Image.open('/home/pi/Images/high_rain.png')
    
    for i in range(12):
        #ligne de séparation
        draw.line([i*17,43,i*17,53],fill=BLACK,width=1)
        #remplissage selon la prévision
        prev=get_prev_pluie(i*5,5)
        # on ramène ça à une intensité par heure (ici en minute)
        intensite=prev*5/60
        #print(intensite)
        #Pluie faible continue 1 à 3 mm par heure
        #Pluie modérée 4 à 7 mm par heure
        #Pluie forte 8 mm par heure et plus

        if intensite <=4 and intensite>0:
            img.paste(low_rain,((i*17)+1,44))
        elif intensite<8 and intensite>0:
            img.paste(high_rain,((i*17)+1,44))
        elif intensite>=8:
            draw.rectangle([(i*17)+1,43,(i*17)+16,52],fill=BLACK)
            

        
def get_prev_pluie(start,duration):
    prev=0
    for j in range(duration):
        prev+=reponse['minutely'][start+duration]['precipitation']
    return prev        

URL='https://api.openweathermap.org/data/2.5/onecall?lat=XXXXX&lon=XXXXX&appid=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&units=metric&lang=fr'
# https://openweathermap.org/api/one-call-api pour avoir le détail de tous les champs possibles de la réponse
# police icone: https://erikflowers.github.io/weather-icons/
# 

#requête
requete=requests.get(URL)

#parse json
reponse=requete.json()

#print(reponse)
##
##print("Local time:"+ts_to_date(reponse['current']['dt'],reponse['timezone_offset']).strftime('%d/%m/%Y %H:%M:%S'))
##print("Sunrise:"+str(reponse['current']['sunrise']))
##print("Sunset:"+str(reponse['current']['sunset']))
##print("Temp:"+str(reponse['current']['temp'])+" °C")
##print("Temp ressentie:"+str(reponse['current']['feels_like'])+" °C")
##print("Pressure:"+str(reponse['current']['pressure'])+" hPa")
##print("Humidity:"+str(reponse['current']['humidity'])+" %")
##print("Dew point:"+str(reponse['current']['dew_point'])+" °C")
##print("Clouds:"+str(reponse['current']['clouds'])+" %")
##print("UV:"+str(reponse['current']['uvi']))
##print("Visibility:"+str(reponse['current']['visibility'])+" m")
##print("Wind speed:"+str(reponse['current']['wind_speed'])+" m/s")
##try:
##    print("Wind gust:"+str(reponse['current']['wind_gust'])+" m/s")
##except:
##    print("No Wind gust here")
##print("Wind deg:"+str(reponse['current']['wind_deg'])+" °")
##try:
##    print("Current rain 1h:"+str(reponse['current']['rain']['1h'])+" mm")
##except:
##    print("No current rain here")
##try:
##    print("Current snow 1h:"+str(reponse['current']['snow']['1h'])+" mm")
##except:
##    print("No current snow here")
##print("Current weather:"+reponse['current']['weather'][0]['main']+':'+reponse['current']['weather'][0]['description'])

### minute par minute
##print("Minute par minute...")
##for item in reponse['minutely']:
##    print("Time: "+ts_to_date(item['dt'],reponse['timezone_offset']).strftime('%H:%M')+" : "+str(item['precipitation'])+ "mm")
####
##### hourly:
##print("Heure par heure...")
##for item in reponse['hourly']:
##    message=""
##    message+="Time: "+ts_to_date(item['dt'],reponse['timezone_offset']).strftime('%d/%m/%Y %H:%M')
##    message+="|"+str(item['temp'])+"°C"
##    message+="|"+str(item['feels_like'])+"°C"
##    message+="|"+str(item['pressure'])+"hPa"
##    message+="|"+str(item['humidity'])+"%"
##    message+="|Cloud:"+str(item['clouds'])+"%"
##    message+="|Rain:"+str(round(100*item['pop']))+"%"
##    message+="|"+item['weather'][0]['description']
##    print(message)
##
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
##
###alerts
##print("Alertes...")
##try:    
##    for item in reponse['alerts']:
##        print(item['sender_name'])
##        print(item['event']+" de "+ts_to_date(item['start'],reponse['timezone_offset']).strftime('%d/%m/%Y %H:%M')+" à "+ts_to_date(item['end'],reponse['timezone_offset']).strftime('%d/%m/%Y %H:%M'))
##        print(item['description'])
##except:
##    print("No weather alert...")

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
ico= ImageFont.truetype( "/home/pi/Inky-scripts/weathericons-regular-webfont.ttf",35)
icomini= ImageFont.truetype( "/home/pi/Inky-scripts/weathericons-regular-webfont.ttf",9)
icomoy= ImageFont.truetype( "/home/pi/Inky-scripts/weathericons-regular-webfont.ttf",25)

# barre pluie prochaine heure
draw_rain_next_hour()

#timestamp
message=datetime.datetime.now().strftime("%H:%M")
#w, h = fontTIME.getsize(message)
x =0
y = 0
draw.text((x, y), message, BLACK, fontTIME)

message=datetime.datetime.now().strftime("%a, %d/%m")
#w, h = fontDATE.getsize(message)
x =0
y = 18
draw.text((x, y), message, BLACK, fontDATE)

message="Vincennes"
#w, h = fontDATE.getsize(message)
x =0
y = 28
draw.text((x, y), message, BLACK, fontDATE)

#temp et hum
message="T:"+str(round(reponse['current']['temp'],1))+"°C"
message2="R:"+str(round(reponse['current']['feels_like'],1))+"°C"
message3="H:"+str(round(reponse['current']['humidity'],1))+"%"
message4="P:"+str(round(reponse['current']['pressure'],1))+"hPa"

draw.text((55, 0), message, BLACK, fontTEMP)
draw.text((55, 10), message2, BLACK, fontTEMP)
draw.text((55, 20), message3, BLACK, fontTEMP)
draw.text((55, 30), message4, BLACK, fontTEMP)

#sunrise, sunset
message=ts_to_date(reponse['current']['sunrise'],reponse['timezone_offset']).strftime('%H:%M')+'-'+ts_to_date(reponse['current']['sunset'],reponse['timezone_offset']).strftime('%H:%M')
w, h = fontTEMP.getsize(message)
x =WIDTH-w
y = 0
draw.text((x, y), message, BLACK, fontTEMP)

message="UV:"+str(round(reponse['current']['uvi']))
w, h = fontTEMP.getsize(message)
x =WIDTH-w
y = 10
draw.text((x, y), message, BLACK, fontTEMP)

message="N: "+str(round(reponse['current']['clouds']))+"% V:"+str(round(reponse['current']['visibility']/1000))+"km"
w, h = fontTEMP.getsize(message)
x =WIDTH-w
y = 20
draw.text((x, y), message, BLACK, fontTEMP)

message="V: "+str(round(3.6*reponse['current']['wind_speed']))+"km/h "+deg_to_direction(reponse['current']['wind_deg'])
w, h = fontTEMP.getsize(message)
x =WIDTH-w-2
y = 30
draw.text((x, y), message, BLACK, fontTEMP)

#icone

message=icon_to_char(reponse['current']['weather'][0]['icon'])
w, h = ico.getsize(message)
x =100
y = -5
draw.text((x, y), message, BLACK, ico)


# prévision
#grid ligne 55

draw.line([0,55,212,55],fill=BLACK,width=1)
draw.line([0,79,212,79],fill=BLACK,width=1)
draw.line([0,103,212,103],fill=BLACK,width=1)

draw.line([71,55,71,103],fill=BLACK,width=1)
draw.line([142,55,142,103],fill=BLACK,width=1)

#H+1,h+4,+7,+10,+13,+16
for i in [1,4,7,10,13,16]:
    display_future(i)

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
