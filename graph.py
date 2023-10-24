import matplotlib.pyplot as plt

# Plots the daily average electricity load in 15 minute increments for each season
def plot_continuous_average_electricity_load(figure_number: int, df_interval_average_data):
    hour_tick_interval = []
    hour_tick = []
    b = 1
    # Generates an hour count which corresponds to each time interval
    for i in range(0,len(df_interval_average_data[2])):
        if(i%4 == 0):
            hour_tick_interval.append(i)
            hour_tick.append(b)
            b +=1
            
    plt.figure(figure_number)
    plt.plot(df_interval_average_data)
    plt.xticks(hour_tick_interval, hour_tick, rotation=45)
    plt.xlabel("Time of Day (Hour)")
    plt.legend(["Summer", "Winter" , "Average"])
    plt.title("Average Electricity Load Over a Day by Season")



#Violin Plots
'''
plt.figure(figure_number)
plt.violinplot(df_week_interval_average_data, showmeans=True, showextrema=True, showmedians=True)
plt.title('Weekday/Weekend 2019 Violin Plot (July/Aug)')
plt.xticks([1,2,3,4,5,6],["Summer Weekend", "Winter Weekend", "Summer Weekday", "Winter Weekday", "Cooling Weekend", "Cooling Weekday"])
plt.ylabel("kWh")
figure_number+=1

plt.figure(figure_number)
plt.violinplot(df_week_interval_average_data_2, showmeans=True, showextrema=True, showmedians=True)
plt.title('Weekday/Weekend 2019 Violin Plot (Aug/Sept)')
plt.xticks([1,2,3,4,5,6],["Summer Weekend", "Winter Weekend", "Summer Weekday", "Winter Weekday", "Cooling Weekend", "Cooling Weekday"])
plt.ylabel("kWh")
figure_number+=1

plt.figure(figure_number)
plt.violinplot(df_cooling_data[0:12], showmeans=True, showextrema=True, showmedians=True)
plt.title('Entire Season Cooling Violin Plot')
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],column_names[0:12])
plt.ylabel("kWh")
figure_number+=1

plt.figure(figure_number)
plt.violinplot(df_summer_data[0:12], showmeans=True, showextrema=True, showmedians=True)
plt.title('Entire Summer Violin Plot')
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],column_names[0:12])
plt.ylabel("kWh")
figure_number+=1

plt.figure(figure_number)
plt.violinplot(df_winter_data[0:12], showmeans=True, showextrema=True, showmedians=True)
plt.title('Entire Winter Violin Plot')
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],column_names[0:12])
plt.ylabel("kWh")
figure_number+=1



plt.figure(figure_number)
#print(df_interval_average_data)

winterNames = ["December", "January", "February", "March", "April"]
monthLength = 30*24*60/15
winterIntervals = [monthLength*0,monthLength*1, monthLength*2, monthLength*3, monthLength*4 ]
col = column_names[year_selected]

plt.plot(df_winter_data[col])
plt.title("Winter Data over 4 month span")
plt.xticks(winterIntervals, winterNames, rotation=45)

figure_number+=1

plt.figure(figure_number)
#Plot Summer, winter, wooling, and radiation data over 4 month span
list_radiation_summer_season = create_radiation_data(df_epw_files[df_name], summer_range)
list_radiation_winter_season = create_radiation_data(df_epw_files[df_name], winter_range)
df_radiation_summer_season = pd.DataFrame(list_radiation_summer_season)
df_radiation_winter_season = pd.DataFrame(list_radiation_winter_season)
#print(type(df_compiled_data), " and ", type(dfRadiationSeason))
#newData = pd.concat([df_compiled_data[0], df_radiation_summer_season])
#plt.plot(df_radiation_summer_season, label = "Radiation")
#plt.plot(df_compiled_data[0], label = "Summer Electrical Load")
#plt.legend = ["Summer", "Winter" , "Average"]
#axNew = axTest.twinx()
#axNew.plot(radiationSeason, color = 'r')
figure7, ax7 = plt.subplots()
color = 'tab:blue'
ax7.set_xlabel('Month')
ax7.set_ylabel('kWh', color = color)
ax7.plot(df_radiation_summer_season, label = "Radiation", color = color)
ax7twin = ax7.twinx()
color = 'tab:red'

ax7twin.set_ylabel('W/m^2', color = color)
ax7twin.plot(df_compiled_data["Summer"], label = "Summer Electrical Load", color=color)
plt.xticks(winter_set[1], combined_set[0], rotation=45)
plt.legend()
plt.title("Summer Electrical Load Relative to Solar Radiation")



#plt.figure(8)
figure8, ax8 = plt.subplots()
color = 'tab:blue'
ax8.set_xlabel('Month')
ax8.set_ylabel('kWh', color = color)
ax8.plot(df_radiation_winter_season, label = "Radiation", color = color)
ax8twin = ax8.twinx()
color = 'tab:red'

ax8twin.set_ylabel('W/m^2', color = color)
ax8twin.plot(df_compiled_data["Winter"], label = "Winter Electrical Load", color=color)
#plt.plot(df_radiation_winter_season, label = "Radiation")
#plt.plot(df_compiled_data[1], label = "Winter Electrical Load")
plt.legend()
plt.title("Winter Electrical Load Relative to Solar Radiation")
plt.xticks(combined_set[1], combined_set[0], rotation=45)




#Plot cooling load, temperature, and radiation hourly data
fig, ax = plt.subplots()
# Twin the x-axis twice to make independent y-axes.
axes = [ax, ax.twinx(), ax.twinx()]
# Make some space on the right side for the extra y-axis.
fig.subplots_adjust(right=0.75)
# Move the last y-axis spine over to the right by 20% of the width of the axes
axes[-1].spines['right'].set_position(('axes', 1.2))
# To make the border of the right-most axis visible, we need to turn the frame
# on. This hides the other plots, however, so we need to turn its fill off.
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
# And finally we get to plot things...
colors = ('Green', 'Red', 'Blue')
holdArray = [df_interval_average_data[2],df_epw_files[df_name]['average_temperature'] , df_epw_files[df_name]['average_radiation']]
nameArray = ["Average Cooling Load", "Average Temperature", "Average Solar Radiation"]
yArray = ["kWh" , "Degrees Celcius" ,"W/m^2"]
yArrayTemp = ["Average Cooling Load (kWh)" , "Average Temperature (Celcius)" ,"Average Solar Radiation (W/m^2)"]
b = 0
for ax, color in zip(axes, colors):
    ax.plot(holdArray[b],  color=color, label = nameArray[b])
    ax.set_ylabel(yArrayTemp[b], color=color)
    ax.tick_params(axis='y', colors=color)
    b +=1

ax.set_xticks(hour_tick_interval, hour_tick, rotation = 45)
#fig.xticks(hour_tick_interval, hour_tick, rotation=45)
axes[0].set_xlabel('Time of Day (Hour)')

ax.set_title("2017 Average Cooling Load Compared to Temperaturand Solar Radiation")

figure_number+=1
'''