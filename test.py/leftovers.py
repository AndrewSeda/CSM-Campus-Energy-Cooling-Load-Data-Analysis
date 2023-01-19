if i == 13:
        splitTab = False
        df2013 = Create_df_weather(fileName, splitTab)
        continue
    elif i == 14:
        splitTab = True
        df2014 = Create_df_weather(fileName, splitTab)
        
    elif i == 15:
        splitTab = False
        df2015 = Create_df_weather(fileName, splitTab)
        continue
    elif i == 16:
        splitTab = False
        df2016 = Create_df_weather(fileName, splitTab)
        continue
    elif i == 17:
        splitTab = False
        df2017 = Create_df_weather(fileName, splitTab)
        writer = pd.ExcelWriter('epwTesting.xlsx')
        df2017.to_excel(writer, sheet_name= "2017")
        writer.save()
        close()
        continue
    elif i == 18:
        splitTab = True
        df2018 = Create_df_weather(fileName,splitTab)
        continue
    elif i == 19:
        splitTab = True
        df2019 = Create_df_weather(fileName, splitTab)
        
        continue