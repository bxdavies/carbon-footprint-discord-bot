################
### Imports ####
################
from discord.ext import commands
import discord
import mysql.connector
import datetime
import schedule 
import time
import asyncio

#########################
### Discord Variables ###
#########################
client = discord.Client()
TOKEN = ""
bot = commands.Bot(command_prefix='.')
#bot.remove_command('help')

##########################
### Database Conetcion ###
##########################
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)
global mycursor
mycursor = mydb.cursor()

#########################
### Declare Variables ###
#########################

########################################

##########################################
global vca_daily_food
vca_daily_food = 0.0
global vca_daily_transport
vca_daily_transport = 0.0
global vca_daily_spending
vca_daily_spending = 0.0
global vc_footprint
vc_footprint = 0.0
####################
### Bot Commands ###
####################
@bot.command(pass_context=True)
async def setup(ctx):
    await ctx.author.send("""
Welcome to Daily Carbon Foot Print Tracker
------------------------------------------

""")
    sql = "INSERT INTO tbl_users (UserID, UserName, RegistrationDate) VALUES (%s, %s, %s)"
    val = (ctx.author.id, ctx.author.name, datetime.date.today())
    mycursor.execute(sql, val)
    mydb.commit()
    



#########################
### Static Carbon Add ###
#########################
@bot.command(name="sca", description="Static Carbon Data - Add")
async def sca(ctx, arg1, arg2):
    global sca_people
    #sca_people = 0
    global sca_daily_electricity
    #sca_daily_electricity = 0.0
    global sca_green_supplier
    #sca_green_supplier = 'FALSE'
    global sca_daily_gas
    #sca_daily_gas = 0.0 
    global sca_daily_food_transport
    #sca_daily_food_transport = 0.0
    global sca_daily_heating_oil
    sca_daily_heating_oil = 0.0 
    global sca_daily_heating_coal
    sca_daily_heating_coal = 0.0
    global sca_daily_heating_wood
    sca_daily_heating_wood = 0.0
    global sca_daily_heating_bgas
    sca_daily_heating_bgas = 0.0
    if 'people' in arg1:
        arg2 = float(arg2)
        sca_people = arg2
    elif 'electricity' in arg1:
        arg2 = float(arg2)
        if arg2 == 2000:
            sca_daily_electricity = (0.527 * 2000) / 365
            sca_daily_electricity = sca_daily_electricity / sca_people
        elif arg2 == 3000:
            sca_daily_electricity = (0.527 * 3000) / 365
            sca_daily_electricity = sca_daily_electricity / sca_people
        elif arg2 == 4800:
            sca_daily_electricity = (0.527 * 4800) / 365
            sca_daily_electricity = sca_daily_electricity / sca_people
        elif arg2 == 7000:
            sca_daily_electricity = (0.527 * 7000) / 365
            sca_daily_electricity = sca_daily_electricity / sca_people
        elif arg2 != 2000 or 3000 or 4800 or 7000 or 0: 
            sca_daily_electricity = (0.527 * arg2) / 365
            sca_daily_electricity = sca_daily_electricity / sca_people
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'green' in arg1:
        if 'yes' in arg2:
            sca_green_supplier = 'TRUE'
            sca_daily_electricity = sca_daily_electricity - sca_daily_electricity * 0.068
        elif 'no' in arg2:
            sca_green_supplier = 'FALSE'
            sca_daily_electricity = sca_daily_electricity
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'gas' in arg1:
        arg2 = float(arg2)
        if arg2 == 0:
            sca_daily_gas = 0
            sca_daily_gas = sca_daily_gas / sca_people
        elif arg2 == 5000:
            sca_daily_gas = (0.185 * 5000) / 365 
            sca_daily_gas = sca_daily_gas / sca_people
        elif arg2 == 12000:
            sca_daily_gas = (0.185 * 12000) / 365 
            sca_daily_gas = sca_daily_gas / sca_people
        elif arg2 == 18000:
            sca_daily_gas = (0.185 * 18000) / 365 
            sca_daily_gas = sca_daily_gas / sca_people
        elif arg2 == 27000:
            sca_daily_gas = (0.185 * 27000) / 365 
            sca_daily_gas = sca_daily_gas / sca_people
        elif arg2 !=  0 or 5000 or 12000 or 18000 or 27000: 
            sca_daily_gas = (0.185 * arg2) / 365
            sca_daily_gas = sca_daily_gas / sca_people
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'food' in arg1:
        if 'where possible' in arg2:
            sca_daily_food_transport = 0.4 
        elif 'always' in arg2:
            sca_daily_food_transport = 0.14
        elif 'never' in arg2:
            sca_daily_food_transport = 0.8
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'heating_oil' in arg1:
        arg2 = float(arg2)
        sca_daily_heating_oil = (2.96 * arg2) / 365
        sca_daily_heating_oil = sca_daily_heating_oil / sca_people
    elif 'heating_coal'in arg1:
        arg2 = float(arg2)
        sca_daily_heating_coal = (3.26 * arg2) / 365
        sca_daily_heating_coal = sca_daily_heating_coal / sca_people
    elif 'heating_wood' in arg1:
        arg2 = float(arg2)
        sca_daily_heating_wood = (3.68 * arg2) / 365
        sca_daily_heating_wood = sca_daily_heating_wood / sca_people
    elif 'heating_bgas' in arg1:
        arg2 = float(arg2)
        sca_daily_heating_bgas = (0.10 * arg2) / 365
        sca_daily_heating_bgas = sca_daily_heating_bgas / sca_people
    else: 
        await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")

############################
### Static Carbon Upatde ###
############################
@bot.command()
async def scu(ctx, arg1, arg2):
    global scu_people
    scu_people = 0
    global scu_daily_electricity
    scu_daily_electricity = 0.0
    global scu_green_supplier
    scu_green_supplier = 'FALSE'
    global scu_daily_gas
    scu_daily_gas = 0.0 
    global scu_daily_food_transport
    scu_daily_food_transport = 0.0
    global scu_daily_heating_oil
    scu_daily_heating_oil = 0.0 
    global scu_daily_heating_coal
    scu_daily_heating_coal = 0.0
    global scu_daily_heating_wood
    scu_daily_heating_wood = 0.0
    global scu_daily_heating_bgas
    scu_daily_heating_bgas = 0.0
    try:
        sql = "SELECT People FROM tbl_sc WHERE UserID = %s"
        val = (ctx.author.id, )
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        scu_people = float(str(myresult[0]).strip("(),"))
    except IndexError:
         await ctx.author.send("Error:202 - There is no User in the Database with your UserID. See ?help")
    if 'people' in arg1:
        arg2 = float(arg2)
        scu_people = arg2
    elif 'electricity' in arg1:
        arg2 = float(arg2)
        if arg2 == 2000:
            scu_daily_electricity = (0.527 * 2000) / 365
            scu_daily_electricity = scu_daily_electricity / scu_people
        elif arg2 == 3000:
            scu_daily_electricity = (0.527 * 3000) / 365
            scu_daily_electricity = scu_daily_electricity / scu_people
        elif arg2 == 4800:
            scu_daily_electricity = (0.527 * 4800) / 365
            scu_daily_electricity = scu_daily_electricity / scu_people
        elif arg2 == 7000:
            scu_daily_electricity = (0.527 * 7000) / 365
            scu_daily_electricity = scu_daily_electricity / scu_people
        elif arg2 != 2000 or 3000 or 4800 or 7000 or 0: 
            scu_daily_electricity = (0.527 * arg2) / 365
            scu_daily_electricity = scu_daily_electricity / scu_people
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'green' in arg1:
        if 'yes' in arg2:
            scu_green_supplier = 'TRUE' 
            scu_daily_electricity = scu_daily_electricity - scu_daily_electricity * 0.068
        elif 'no' in arg2:
            scu_green_supplier = 'FALSE'
            scu_daily_electricity = scu_daily_electricity
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'gas' in arg1:
        arg2 = float(arg2)
        if arg2 == 0:
            scu_daily_gas = 0
            scu_daily_gas = scu_daily_gas / scu_people
        elif arg2 == 5000:
            scu_daily_gas = (0.185 * 5000) / 365 
            scu_daily_gas = scu_daily_gas / scu_people
        elif arg2 == 12000:
            scu_daily_gas = (0.185 * 12000) / 365 
            scu_daily_gas = scu_daily_gas / scu_people
        elif arg2 == 18000:
            scu_daily_gas = (0.185 * 18000) / 365 
            scu_daily_gas = scu_daily_gas / scu_people
        elif arg2 == 27000:
            scu_daily_gas = (0.185 * 27000) / 365 
            scu_daily_gas = scu_daily_gas / scu_people
        elif arg2 !=  0 or 5000 or 12000 or 18000 or 27000: 
            scu_daily_gas = (0.185 * arg2) / 365
            scu_daily_gas = scu_daily_gas / scu_people
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'food' in arg1:
        if 'Where Possible' in arg2:
            scu_daily_food_transport = 0.4 
        elif 'Always' in arg2:
            scu_daily_food_transport = 0.14
        elif 'Never' in arg2:
            scu_daily_food_transport = 0.8
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'heating_oil' in arg1:
        arg2 = float(arg2)
        scu_daily_heating_oil = (2.96 * arg2) / 365
        scu_daily_heating_oil = scu_daily_heating_oil / scu_people
    elif 'heating_coal'in arg1:
        arg2 = float(arg2)
        scu_daily_heating_coal = (3.26 * arg2) / 365
        scu_daily_heating_coal = scu_daily_heating_coal / scu_people
    elif 'heating_wood' in arg1:
        arg2 = float(arg2)
        scu_daily_heating_wood = (3.68 * arg2) / 365
        scu_daily_heating_wood = scu_daily_heating_wood / scu_people
    elif 'heating_bgas' in arg1:
        arg2 = float(arg2)
        scu_daily_heating_bgas = (0.10 * arg2) / 365
        scu_daily_heating_bgas = scu_daily_heating_bgas / scu_people
    else: 
        await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")

##############################
### Static Carbon Add Save ###
##############################
@bot.command()
async def scas(ctx):
    try:
        sc_footprint = sca_daily_electricity + sca_daily_gas + sca_daily_heating_bgas + sca_daily_heating_coal + sca_daily_heating_oil + sca_daily_heating_wood + sca_daily_food_transport + 3.01
        sql = "INSERT INTO tbl_sc (UserID, People, Electricity, GreenSupplier, Gas, FoodTransport, HeatingOil, Coal, Wood, BottledGas, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (ctx.author.id, sca_people, sca_daily_electricity, sca_green_supplier, sca_daily_gas, sca_daily_food_transport, sca_daily_heating_oil, sca_daily_heating_coal, sca_daily_heating_wood, sca_daily_heating_bgas, sc_footprint)
        mycursor.execute(sql, val)
        mydb.commit()

        await ctx.author.send("All the Data you Entered has been saved")
        await ctx.author.send("Your Daily Static Carboon Footprint is:")
        await ctx.author.send(sc_footprint)
    except:
        print ("Error:201 - General User Error. See ?help")

###################################
### Variable Carbon Update Save ###
###################################
@bot.command()
async def scus(ctx):
    scu_row = 0
    if scu_people != 0:
        sql = "UPDATE tbl_sc SET People = %s WHERE UserID = %s"
        val = (scu_people, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_electricity != 0.0:
        sql = "UPDATE tbl_sc SET Electricity = %s WHERE UserID = %s"
        val = (scu_daily_electricity, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if 'TRUE' in scu_green_supplier:
        sql = "UPDATE tbl_sc SET GreenSupplier = %s WHERE UserID = %s"
        val = (scu_green_supplier, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_gas != 0.0:
        sql = "UPDATE tbl_sc SET Gas = %s WHERE UserID = %s"
        val = (scu_daily_gas, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_food_transport != 0.0:
        sql = "UPDATE tbl_sc SET FoodTransport = %s WHERE UserID = %s"
        val = (scu_daily_food_transport, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_heating_oil != 0.0:
        sql = "UPDATE tbl_sc SET HeatingOil = %s WHERE UserID = %s"
        val = (scu_people, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_heating_coal != 0.0:
        sql = "UPDATE tbl_sc SET Coal = %s WHERE UserID = %s"
        val = (scu_daily_heating_coal, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_heating_wood != 0.0:
        sql = "UPDATE tbl_sc SET Wood = %s WHERE UserID = %s"
        val = (scu_daily_heating_wood, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_daily_heating_bgas != 0.0:
        sql = "UPDATE tbl_sc SET BottledGas = %s WHERE UserID = %s"
        val = (sca_daily_heating_bgas, ctx.author.id)
        mycursor.execute(sql, val)
        mydb.commit()
        scu_row = scu_row + 1
    if scu_row >= 1:
        try:
            message = "You have Updated: ", str(scu_row), " row/s"
            message = ''.join(message)
            await ctx.author.send(message)
            sql = "SELECT Total FROM tbl_sc WHERE UserID = %s"
            val = (ctx.author.id, )
            mycursor.execute(sql, val)
            scu_old_footprint_raw = mycursor.fetchall()
            scu_old_footprint = str(scu_old_footprint_raw[0]).strip("(),Decimal'')")
            ##
            sql = "SELECT * FROM tbl_sc WHERE UserID = %s"
            val = (ctx.author.id, )
            mycursor.execute(sql, val)
            sc_data = mycursor.fetchall()
            for row in sc_data:
                scd_daily_electricity = float(row[3])
                scd_daily_gas = float(row[5])
                scd_daily_food_transport = float(row[6])
                scd_daily_heating_oil = float(row[7])
                scd_daily_heating_coal = float(row[8])
                scd_daily_heating_wood = float(row[9])
                scd_daily_heating_bgas = float(row[10])

            scu_footprint = scd_daily_electricity + scd_daily_gas + scd_daily_heating_bgas + scd_daily_heating_coal + scd_daily_heating_oil + scd_daily_heating_wood + scd_daily_food_transport + 3.01
            message = 'Updating Static Carbon Footprint from: ', str(scu_old_footprint),' to: ', str(scu_footprint) 
            message = ''.join(message)
            await  ctx.author.send(message)
            sql = "Update tbl_sc SET Total = %s Where UserID = %s"
            val = (scu_footprint, ctx.author.id)
            mycursor.execute(sql, val)
            mydb.commit()
        except IndexError:
            await ctx.author.send("Error:202 - There is no User in the Database with your UserID. See ?help")
    else:
        print ("Error:203 - No Data Provided. See ?help")

@bot.command()
async def remove(ctx):
    sql = "DELETE * FROM tbl_users WHERE UserID = %s"
    val = (ctx.author.id, )
    mycursor.execute(sql, val)
    mydb.commit()

    


#################################    
### Variable Carbon FootPrint ###
#################################
@bot.command()
async def vca(ctx, arg1, arg2, arg3 : str = ""):
    global vca_daily_food
    global vca_daily_transport
    vca_daily_transport = 0.0
    global vca_daily_spending
    if 'food' in arg1:
        if '1' in arg2:
            if 'all' in arg3:
                vca_daily_food = vca_daily_food + 0
            elif 'some' in arg3:
                vca_daily_food = vca_daily_food + 1
            elif 'none' in arg3:
                vca_daily_food = vca_daily_food + 2
            else:
                await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
        elif '2' in arg2:
            if 'yes' in arg3:
                vca_daily_food = vca_daily_food + 1
            elif 'no' in arg3:
                vca_daily_food = vca_daily_food + 0
            else:
                await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
        elif '3'in arg2:
            if 'yes' in arg3:
                vca_daily_food = vca_daily_food + 0.63 + 0.49
            elif 'no' in arg3:
                vca_daily_food = vca_daily_food + 0.08 + 0.08
            else:
                await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
        elif '4' in arg2:
            if 'all' in arg3:
                vca_daily_food = vca_daily_food + 0.54
            elif 'some' in arg3:
                vca_daily_food = vca_daily_food + 0.56
            elif 'none' in arg3:
                vca_daily_food = vca_daily_food + 0.6
            else:
                await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
        else:
            print ("Error")
    elif 'transport' in arg1:
        arg3 = float(arg3)
        if '1' in arg2:
            vca_daily_transport = vca_daily_transport + 0.14 * arg3
        elif '2' in arg2: 
            vca_daily_transport = vca_daily_transport + 0.13 * arg3
        elif '3' in arg2:
            vca_daily_transport = vca_daily_transport + (0.03 * arg3) * 14.3
        elif '4' in arg2:
            vca_daily_transport = vca_daily_transport + (0.02 * arg3) * 14.3
        elif '5' in arg2:
            vca_daily_transport = vca_daily_transport + (0.017 * arg3) * 14.3
        elif '6'in arg2:
            vca_daily_transport = vca_daily_transport + 0.25 * arg3
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    elif 'money' in arg1:
        if '1' in arg2:
            vca_daily_spending = 13.69
        elif '2' in arg2: 
            vca_daily_spending = 9.32
        elif '3' in arg2:
            vca_daily_spending = 6.58
        elif '4' in arg2:
            vca_daily_spending = 3.84
        elif '5' in arg2:
            vca_daily_spending = 0.0
        else:
            await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")
    else:
        await ctx.author.send("Error:202 - The Data you entered was not accepted as it is not one of the options. See ?help")

@bot.command()
async def vcas(ctx):
    vc_footprint = vca_daily_food + vca_daily_transport + vca_daily_spending
    sql = "INSERT INTO tbl_vc(UserID_Date, UserID, Date, Food, Transport, Spending, Total) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    UserID_Date = str(ctx.author.id) + "|" + str(datetime.date.today())
    print (UserID_Date)
    val = (UserID_Date, ctx.author.id, datetime.date.today(), vca_daily_food, vca_daily_transport, vca_daily_spending, vc_footprint,)
    mycursor.execute(sql, val)
    mydb.commit()

    await ctx.author.send("All the Data you Entered has been saved")
    await ctx.author.send("Your Daily Static Carboon Footprint is:")
    await ctx.author.send(vc_footprint)

######################
### Anoncements ###
#######################
async def day_message():
    channel = bot.get_channel(730099302130516058)
    message = "Good Morning Everyone. Today is day: ", str(datetime.datetime.now().strftime("%j")), "/ 365 \n Don't forget to send your daily carbon footprint"
    message = ''.join(message)
    await channel.send(message)
    
async def reminder_message():
    channel = bot.get_channel(730099302130516058)
    await channel.send("Good Evening Everyone. Don't forget to send your daily carbon footprint in by 9PM")

### Leaderboard ###
async def leaderboard():
    a = 0 # UserID
    b = 0 # UserID_Date
    c = 3 # sc total
    d = 4 # vc total
    i = 0 # list count
    while True:
        try:
            mycursor.execute("SELECT UserID FROM tbl_users")

            UserID = mycursor.fetchall()
            UserID = str(UserID[a]).strip("(),")
            print (UserID)
            sql = "SELECT * FROM tbl_total WHERE Date = %s AND UserID = %s"
            val = (str(datetime.date.today()), UserID,  )
            mycursor.execute(sql, val)
            myresult = mycursor.fetchone()

            print (myresult)
            while True:
                UserID_Date = str(myresult[b])
                sc_total = float(myresult[c])
                vc_total = float(myresult[d])
                Total = sc_total + vc_total
                print (Total)
                print (UserID_Date)
                a += 1
                sql = "UPDATE tbl_total SET daily_total = %s WHERE UserID_Date = %s"
                val = (Total, UserID_Date, )
                mycursor.execute(sql, val)
                mydb.commit()
                break
        except IndexError:
            break
  
schedule.every().day.at("00:01").do(day_message)
schedule.every().day.at("20:00").do(reminder_message)
asyncio.run(leaderboard())
bot.run(TOKEN)

