# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:57:43 2020

File Name: COIVD_Tracker.py

Mandar Limaye 
Steffie Rego 
Shubham Lalwani
"""

#importing the ncessary library
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#importing the custom made module to access its methods
import InvSolutions as ins


#This function requets user to select a market based on avaible options
#It also provides an option to return to the previous menu
#@Return Param: market selected option
def userChoice():
    print("We provide comparative analysis across multiple markets")
    print("-" * 90)
    ipFlag = True;
    while(ipFlag):
        #Requesting user for an input
        market_opt = input("Kindly Select the Market You Want to Analyze(1/2/3/4): "
                        "\n1) --> Stock Market (Nasdaq)"
                        "\n2) --> Cryptocurrency Market (Bitcoin)"
                        "\n3) --> Gold Market"
                        "\n4) --> US Mortgage Rates"
                        "\n5) --> Return to Previous Menu to Exit\n")
        
        try:
            #Requesting user for a proper input
            if(int(market_opt) > 5 or int(market_opt) < 1):
                ipFlag = True;
                print("----------Please Select the Proper Input(1/2/3/4)\n")
            else:
                ipFlag = False;
        except:
            #Handling the garbage input by user
            ipFlag = True;
            print("----------Please Select the Proper Input(1/2/3/4)\n")
            
    return int(market_opt)
        
    
#This function requets user to select a option for date range for summary stats
#@Return Param: summary review selected option
def reviewSummaryChoice():
    review_opt_flag = True
    while(review_opt_flag):
        #Requesting user for an input
        review_opt = input("Kindly Select a Date Range for Summary: "
                           "\n1) --> Last Available Date"
                           "\n2) --> Last 15 Days"
                           "\n3) --> Last 1 Month(30 Days)\n")
                           
        try:
            #Requesting user for a proper input
            if(int(review_opt) > 3 or int(review_opt) < 1):
                review_opt_flag = True;
                print("----------Please Select the Proper Input(1/2/3)\n")
            else:
                review_opt_flag = False;
        except:
            #Handling the garbage input by user
            review_opt_flag = True;
            print("----------Please Select the Proper Input(1/2/3)\n")
            
    return int(review_opt)

#This function requets user to select a option for date range for visualization of stats
#@Return Param: selected option for visualization
def vizCVEffectChoice():
    viz_opt_flag = True
    while(viz_opt_flag):
        #Requesting user for an input
        viz_opt = input("Kindly Select a Range of Data for Visualization: "
                           "\n1) --> Last 15 Days"
                           "\n2) --> Last 1 Month(30 Days)\n")
                           
        try:
            #Requesting user for a proper input
            if(int(viz_opt) > 2 or int(viz_opt) < 1):
                viz_opt_flag = True;
                print("----------Please Select the Proper Input(1/2/3)\n")
            else:
                viz_opt_flag = False;
        except:
            #Handling the garbage input by user
            viz_opt_flag = True;
            print("----------Please Select the Proper Input(1/2)\n")
            
    return int(viz_opt)


#This function requets user to input no of COVID cases to get an estimate for the specific selected market
#@Return Param: No of Positive COVID cases
def covidNumber():
    covid_no_flag = True
    while(covid_no_flag):
        #Requesting user for an input
        covid_cases = input("Kindly Input the No of Postive COVID Cases for prediction(Range: 100-10000000)\n")
        try:
            #Requesting user for a proper input in the given range
            if(int(covid_cases) > 10000000 or int(covid_cases) < 100):
                covid_no_flag = True;
                print("----------Please Select the Proper Input(Range: 100-10000000)\n")
            else:
                covid_no_flag = False;
        except:
            #Handling the garbage input by user
            covid_no_flag = True;
            print("----------Please Select the Proper Input(Range: 100-10000000)\n")
            
    return int(covid_cases)


#This function performs the main user interaction after user selects the market he wants to explore
def appMenuInteraction(df_merged,userChoiceVal):
    #Assinging Market name and a varaible called opt based on users market solution
    if(userChoiceVal == 1):
        marketName = "Stock Market(Nasdaq)"
        opt = "stock"
    elif(userChoiceVal == 2):
        marketName = "Cryptocurrency Market(Bitcoin)"
        opt = "bitcoin"
    elif(userChoiceVal == 3):
        marketName = "Gold Market"
        opt = "gold"
    elif(userChoiceVal == 4):
        marketName = "US Mortgage Rates"
        opt = "apr"    
        
    #Declaring a varible to be used later
    menuFlag = True
    #Running a loop till user provides an input to return to the menu
    while(menuFlag == True):
        #Running the application for a valid market selection
        if(userChoiceVal > 0 and userChoiceVal < 5):
            #Providing user with options to use application
            explore_opt = input("Kindly Select a Option to Explore " + marketName +
                "\n1) --> Review " + marketName + " Summary"
                "\n2) --> Visualize the effect of COVID-19 on " + marketName + ""
                "\n3) --> Comparative Study of Trends in all Markets"
                "\n4) --> Predict the value in " + marketName + " for specific COVID Postive Cases"
                "\n5) --> Return to Previous Menu To Exit\n")    
            try:
                if(int(explore_opt) == 1):
                    #Taking user summary option using a function
                    reviewOpt = reviewSummaryChoice()
                    #Fetching proper summary stats according to market and summary option selection
                    df_op = ins.reviewTable(opt,reviewOpt)
                    print(df_op.to_string(index=False))
                    menuFlag = True
                elif(int(explore_opt) == 2):
                    #Taking user visualization option using a function
                    vizCVOpt = vizCVEffectChoice()
                    #Displaying graphs according to market and visualization option selection
                    ins.visualization(df_merged,opt,vizCVOpt)
                    menuFlag = True
                elif(int(explore_opt) == 3):
                    #Displaying market trends using a method of InvSolutions module
                    ins.marketTrends(df_merged)
                    menuFlag = True
                elif(int(explore_opt) == 4):
                    #Requests user to input no of cases
                    covid_pNo = covidNumber()
                    output = ins.getPredictedValue(df_merged,covid_pNo,opt)
                    if(opt == 'apr'):
                        print("\n=====================================================================")
                        print("-------> Predictive Analytics ")
                        print("Market Selected: " + marketName)
                        print("No of Positive COVID cases given by you: " + str(covid_pNo))
                        print("Predicted Avg Mortgage APR: " + str(np.round(output,2)))
                        print("=====================================================================\n")
        
                    else:
                        print("\n=====================================================================")
                        print("-------> Predictive Analytics ")
                        print("Market Selected: " + marketName)
                        print("No of Positive COVID cases given by you: " + str(covid_pNo))
                        print("Predicted Closing Price: " + str(np.round(output,2)))
                        print("=====================================================================\n")
                    menuFlag = True
                elif(int(explore_opt) == 5):
                    #Breaking the loop based on the user selection
                    menuFlag = False
                elif(int(explore_opt) > 5 or int(explore_opt) < 1):
                    print("\nKindly Select the Proper Input (1/2/3/4/5)\n")
                    print("----- THANK YOU")
            except:
                #Handling the error handling
                print("\nKindly Select the Proper Input (1/2/3/4/5)\n")
                print("----- THANK YOU")
                menuFlag = True

#----------------------------------------------- Main Code Starts Here---------------------------------------------------

#Start of the main module of the project
if __name__ == '__main__':
    print("\n\n\t~~~~ Welcome to the PiedPiper InvSolution's COVID Impact Tracker ~~~~\n")
    print("-" * 90)
    #Application Information
    print("We understand that the market is highly fluctuating in the days of the COVID-19 pandemic")
    print("This is central aggregated source to study the effect of COVID-19 on different markets\n")
  
    validInput = True
    while(validInput):
        #Application Information to request user for input
        print("-" * 90)
        print("To provide a seamless user experience we offer multuple choices to our users")
        print("We request you to select the appropriate option according to your needs")
        print("-" * 90)
        #REquesting user for an input
        user_opt = input("Kindly Select a Data Source(1/2/3): "
                            "\n1) --> Previously Downloaded Data  (Date: 30th April 2020) "
                            "\n2) --> Download Latest Data (1-2 Minutes Wait Time)"
                            "\n3) --> Exit The Application\n")
        
        try:
            if (int(user_opt) == 1):
                #Reading the file from previously saved csv file
                df_merged = pd.read_excel("merged_data.xlsx")
                #Requesting user for first market selection
                userChoiceVal = userChoice()
                #Displaying the options as long as user does not choose to go back
                while(int(userChoiceVal) != 5):
                    #Passing dataframe and user market selecion to function to perform further activity
                    appMenuInteraction(df_merged,userChoiceVal)
                    userChoiceVal = userChoice()
                #Setting flag to continue the application
                validInput = True            
            elif (int(user_opt) == 2):
                print("Downloading Latest Data ......")
                print("Note: This Feature Takes approximately 1-2 Minutes.")
                print("....")
                print("....")
                print("....")
                print("....")
                print("....")
                print("....")
                #Reading the data using a method written in InvSolutions module
                df_merged = ins.getNewData()
                df_merged.reset_index(drop=True,inplace=True)
                #Commented the Code to enerate the most latest file
#                df_merged.to_excel("merged_data.xlsx")
                print("-----> Download Sucessfully Completed")
                print("-" * 90)
                print()
                #Requesting user for first market selection
                userChoiceVal = userChoice()
                #Displaying the options as long as user does not choose to go back
                while(int(userChoiceVal) != 5):
                    #Passing dataframe and user market selecion to function to perform further activity
                    appMenuInteraction(df_merged,userChoiceVal)
                    userChoiceVal = userChoice()
                #Setting flag to continue the application
                validInput = True
            elif (int(user_opt) == 3):
                #Setting flag to end the application
                validInput = False
            elif(int(user_opt) > 3 or int(user_opt) < 1):
                #Requesting the user for a proper input
                print("Kindly Select the Input in the given range (1/2/3)\n")
                #Setting flag to continue the application
                validInput = True
        except:
            #Handling the garbage input
            print("\nKindly Select the Proper Numeric Input (1/2/3)")
            print("----- THANK YOU \n\n")
            #Setting flag to continue the application
            validInput = True