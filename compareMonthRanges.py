
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid, simpson
from coolingLoadFunctions import*


#Generates data for each range of months
# 1 Month, 2 month, 3 month, and 4 month ranges
def main(df, yearSelect, hourTick, hourTickInterval):


        for i in range(1,5):
            if i == 1:
                winterRange = [11,0]
                summerRange = [5,6]
                combinedSet1, compiledData1, intervalAverageData1, winterData1, summerData1, coolingData1, winterMonthIntervals1, weekIntervalAverageData1 = create_data_sets(summerRange, winterRange, df, yearSelect)
                continue
            elif i == 2:
                winterRange = [11,1]
                summerRange = [5,7]
                combinedSet2, compiledData2, intervalAverageData2, winterData2, summerData2, coolingData2, winterMonthIntervals2, weekIntervalAverageData2  = create_data_sets(summerRange, winterRange, df, yearSelect)
                continue
            elif i ==3 :
                winterRange = [11,2]
                summerRange = [5,8]
                combinedSet3, compiledData3, intervalAverageData3, winterData3, summerData3, coolingData3, winterMonthIntervals3, weekIntervalAverageData3 = create_data_sets(summerRange, winterRange, df, yearSelect)
                continue
            elif i == 4:
                winterRange = [11,3]
                summerRange = [5,9]
                combinedSet4, compiledData4, intervalAverageData4, winterData4, summerData4, coolingData4, winterMonthIntervals4, weekIntervalAverageData4 = create_data_sets(summerRange, winterRange, df, yearSelect)
                continue

        #Plot hourly average cooling over 1, 2, 3, and 4 month ranges
        #Plots are overlayed
        plt.figure(1)
        plt.plot(intervalAverageData1[2], label = "1 Month Average")
        plt.plot(intervalAverageData2[2], label = "2 Month Average")
        plt.plot(intervalAverageData3[2], label = "3 Month Average")
        plt.plot(intervalAverageData4[2], label = "4 Month Average")

        plt.xticks(hourTickInterval, hourTick, rotation=45)
        plt.xlabel("Time of Day (Hour)")
        plt.ylabel("kWh")
        plt.title("Cooling Data Average at Different Ranges (Starting in December/June)")
        plt.legend()

        #Plot hourly average winter over 1, 2, 3, and 4 month ranges
        #Plots are overlayed
        plt.figure(2)
        plt.plot(intervalAverageData1[1], label = "1 Month Average")
        plt.plot(intervalAverageData2[1], label = "2 Month Average")
        plt.plot(intervalAverageData3[1], label = "3 Month Average")
        plt.plot(intervalAverageData4[1], label = "4 Month Average")

        plt.xticks(hourTickInterval, hourTick, rotation=45)
        plt.xlabel("Time of Day (Hour)")
        plt.ylabel("kWh")
        plt.title("Winter Data Average at Different Ranges (Starting in December)")
        plt.legend()