from telegram.ext import Application,CommandHandler,MessageHandler,ConversationHandler,CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json 
import requests
t1 = 0
t2 = 1
t3 = 2
t4 = 3
tp1 = 4
tp2 = 5
tp3 = 6
tp4 = 7
async def top(update,context):
    
    user_id = update.effective_user.id
    city = context.user_data.get("cty",0)
    wo = context.user_data.get("wo",0)
    pa = context.user_data.get("pa",0)
    woc = context.user_data.get("woc",0)
    pac = context.user_data.get("pac",0)
    key = [[
    InlineKeyboardButton("Sign Up",callback_data="sign")
    ]]    
    try :
               with open("do.json","r") as f :
                   data = json.load(f)
               if str(user_id)  in data :
                   keysta = [[InlineKeyboardButton("City Weather" , callback_data="dama" ) , 
                   InlineKeyboardButton("Search Hotels",callback_data ="searchotl"),
                   InlineKeyboardButton("Help",callback_data ="del")],]
                   ve1 = InlineKeyboardMarkup(keysta)
                   await update.message.reply_text("            Menu            ",reply_markup = ve1)
                   return ConversationHandler.END
                   #await update.message.reply_text("to start") 
                 #  await update.message.text("yjdh")             
                   
             #  await par.edit_message_text("user....") 
               else   :
                   ve = InlineKeyboardMarkup(key)
                   await update.message.reply_text("♧♧",reply_markup=ve)
    except Exception as e :
        print(e)          
async def btno(update,context):
       userhaver = "@NHGTS4"
       par= update.callback_query
       await par.answer()
       if par.data == "dama":
           await par.edit_message_text("city : ")
           return tp3
       if par.data == "sign":
           await par.edit_message_text("user...")
           return t1
       if par.data == "searchotl" :
           await par.edit_message_text("city :")
           return tp4    
       if par.data == "del"  :
           
           await par.edit_message_text(f""" Welcome to City Assistant!

What can I do for you?

🌤️ Current Weather
Check temperature, wind and weather conditions.

🏨 Hotel Search
Find hotels around a city.

for help
Contact : {userhaver}""")
async def ctywthr(update,context): 
           try :
               context.user_data["cty"] = update.message.text
               print("pr")
               url = "https://geocoding-api.open-meteo.com/v1/search"
               parame = {
           "name" : context.user_data["cty"] ,
           "count" : 1 ,
           "language" : "en"
               }
               respne = requests.get(url, params=parame)
               data = respne.json()
               if "results" not in data or not data["results"] :
                   await update.message.reply_text("Error 808")
                   return ConversationHandler.END  
               place = data["results"][0]              
               lat = place["latitude"]
               lon = place["longitude"] 
           
               weather = {
           0 : "Clear sky" ,         
           1 : "Mainly clear",           
           2 : "Partly cloudy",
           3 : "Overcast",
           45 : "Fog",
           48 : "Freezing fog",
           51 : "Light drizzle",
           55 : "Heavy drizzle",
           61 : "Light rain",
           63 : "Moderate rain",
           65: "Heavy rain",
           71: " Light snow",
           73: " Moderate snow",
           75: "Heavy snow",
           80: "Light rain showers",
           81: "Moderate rain showers",
           82: "Heavy rain showers",
           95: "Thunderstorm",
           96: "Thunderstorm with hail",
           99: "Severe thunderstorm with hail"
               }                 
                                                                                       
               url1 = "https://api.open-meteo.com/v1/forecast"
           
               parm = {
           "latitude": lat,
           "longitude": lon,
           "current":"temperature_2m,wind_speed_10m,weather_code"
               }
               respon = requests.get(url1, params=parm)
               wthr = respon.json()
               country = place["country"]
               curt = wthr["current"]
               temp = curt["temperature_2m"]
               wind = curt["wind_speed_10m"]
               code = curt["weather_code"]
               cond = weather.get(code,"None")
               await update.message.reply_text(f"country :{country}\n tempreture : {temp} c \n wind : {wind} km/h \n condition : {cond}")                     
               return ConversationHandler.END
           except Exception as eroa :
              print(eroa)
              return ConversationHandler.END             
           
async def searchhot(update,context):
                          try :
                              
                              city = update.message.text
                              url = "https://geocoding-api.open-meteo.com/v1/search"
                              parm = {
                              "name" : city ,
                              "count" : 1,
                              "language" : "en"
                              }
                              respon = requests.get(url, params=parm)
                              data = respon.json()
                              print("-")
                              if "results" not in data or not data["results"]:
                                  await update.message.reply_text("Error 808")
                                  return ConversationHandler.END
                              place = data["results"][0]
                              lat = place["latitude"]
                              lon = place["longitude"]
                              country = place["country"]
                              headers = {
                              "User-Agent": "MyTelegramBot/1.0"
                              } 
                              overpass_url = "https://overpass-api.de/api/interpreter"
                              query = f"""
[out:json][timeout:10];
node["tourism"="hotel"](around:14000,{lat},{lon});
out;
"""
     
                              hotel_respon = requests.post(
                              overpass_url,
                              data={"data": query},
                              headers=headers,
                              timeout=20 
                              
                              )
                              
                              print("STATUS:", hotel_respon.status_code)
                              print("RESPONSE:", hotel_respon.text[:1000])
                              if hotel_respon.status_code != 200 :
                                  await update.message.reply_text("Error 707")
                                  return ConversationHandler.END
                              hotel_data = hotel_respon.json()
                              hotels = hotel_data.get("elements", [])
                              print("-")
                              if not hotels :
                                  await update.message.reply_text("Error 808")
                                  return ConversationHandler.END
                              message = f"Country : {country}\nHotels in {city}\n\n"
                              count = 0
                              for hotel in hotels :
                                  tags = hotel.get("tags",{})
                                  name = tags.get("name")
                                  if not name :
                                      continue
                                  address = tags.get("addr:street",
                                      "Address unavailable")                                     
                                  message += (
                                      f"🔺️{name}\n"
                                      f"location : {address}\n\n"
                                      )
                                  count += 1
                                  if count >= 7 :
                                      break 
                              if count == 0 :
                                  await update.message.reply_text("Error 707") 
                              else :
                                      await update.message.reply_text(message)
                                      return ConversationHandler.END    
                          except Exception as e :
                              print(e,"Erro") 
                              
async def na(update,context):
    context.user_data["wo"] = update.message.text
    await update.message.reply_text("pass...")
    return t2
async def nb(update,context):
    print("@")
    user_id = update.effective_user.id    
    context.user_data["pa"]=update.message.text    
    with open("do.json","r") as f :
           data = json.load(f)
    data[str(user_id)] = {"wo":context.user_data["wo"] ,
            "pa":context.user_data["pa"]
           }
    
           
    with open("do.json","w") as f :
        json.dump(data,f,indent=4)
    await update.message.reply_text("re start")
    return ConversationHandler.END
    
                                                                                                                                                                                                                                                                                                                             
async def do(update,context):
    user_id = str(update.effective_user.id)
    context.user_data["pac"] = update.message.text   
    with open("do.json","r") as f :
        data = json.load(f)
        ur = data.get(user_id)
##async def 
      #  if ur is None :
       ##     await update.message.reply_text("None")
       #     return ConversationHandler.END
        wy = ur["wo"]
        pu = ur["pa"]
        if  wy == context.user_data["woc"] and pu ==  context.user_data["pac"] :
            await update.message.reply_text("Restart")
            return ConversationHandler.END
        else :
            await update.message.reply_text("false")
            return ConversationHandler.END
async def start(update,context):
  #  print(":)")
    keysta = [[InlineKeyboardButton("City Weather" , callback_data="dama" ) , 
    InlineKeyboardButton("Search Hotels",callback_data ="searchotl")]]
    ve1 = InlineKeyboardMarkup(keysta)
    await update.message.reply_text("lest",reply_markup = ve1)
    return ConversationHandler.END
#async def damaser(update,context):
    
conv = ConversationHandler(
entry_points=[CommandHandler("start", top)
,
CallbackQueryHandler(btno, pattern="^(sign|dama|searchotl|del)$")
    ],
    states={
    t1 :[
    MessageHandler(filters.TEXT,na)],
    t2 :[
    MessageHandler(filters.TEXT,nb)
    ],    
    t4 :[
    MessageHandler(filters.TEXT,do)
    ],
    tp1 : [
    MessageHandler(filters.TEXT,start)
    ],
    tp3 : [
    MessageHandler(filters.TEXT & ~filters.COMMAND,ctywthr)
    ],
    tp4 : [
    MessageHandler(filters.TEXT,searchhot)
    ],
    },fallbacks=[]   
)   
app = app = Application.builder().token("8851173084:AAGqcwviDp9C3AxVBhZh5KUIbsgSXU14eMI").build()
app.add_handler(conv)
try :
    app.run_polling()
except Exception as drop :
    print(drop)
    
    
