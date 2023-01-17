#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 15:15:41 2020

@author: abhishek
"""

# Import pandas, numpy library and sys Module to get acces to system arguments
import pandas as pd
import numpy as np

# Sytem, os and shutil module to run system commands and create new, copy, remove files
import sys

# Module to get today's date
from datetime import date

# Create template from docx file to efficienty edit
from docxtpl import DocxTemplate




def getInputs():
    '''
    This function handles the I/O part of the code, i.e. asks the user for flat no
    and membership no. It is essential to provide atleast one i.e. either flat no
    or member no.
    Returns
    -------
    flatNo : Flat no of the member
    membershipNo : Membership number
    NextMC : Maintenance Cost for the next period
    '''
   
    if len(sys.argv) == 3:
        flatNo = sys.argv[1]
        membershipNo = sys.argv[2]
        NextMC = sys.argv[3]
    else:
        flatNo = input("Enter Flat No. = ")
        membershipNo = input("Enter membership number = ")
        NextMC = input("Next Maintenance Charges = ")


    while(len(flatNo.strip()) == 0 and len(membershipNo.strip()) == 0):
        flatNo = input("Enter Flat No. = ")
        membershipNo = input("Enter membership number = ")


    while(NextMC.isnumeric() == False):
        NextMC = input("Next Maintenance Charges = ")
    
    # Convert user input to uppercase to remove user input discrepancy
    flatNo = flatNo.upper()
    # membershipNo = membershipNo.upper() // DON'T ADD THIS LINE here

    # Set data type as integer
    NextMC = int(NextMC)

    return flatNo, membershipNo, NextMC





def getData(dataFile):
    '''
    This function process the data, performs data cleaning and prepare it in format to 
    be efficiently used by other functions. It's a subroutine of search data function.

    Parameters
    ----------
    dataFile : Path/FileName of excel data file with extension (.xls or .xlsx)

    Returns
    -------
    df_Member : DataFrame of members
    df_Intrest : DataFrame of Intrest for each member
    '''

    # read an excel file and convert
    # into a dataframe object
    df = pd.DataFrame(pd.read_excel(dataFile))

    # Remove all white spaces and extra spaces from data column names for efficient calls
    for i in range(0, len(df.columns)):
        #df = df.rename({df.columns[i]:df.columns[i].strip()}, axis=1)
        df = df.rename({df.columns[i]:"".join(df.columns[i].split()).upper()}, axis=1)
    
    # Remove any possible spaces from maintenance
    for i in df.columns:
        if "MAINT" in i or "CONSTRUCT" in i:
            df[i].replace(" ", np.nan, inplace = True)
            # df[i].replace(np.nan, 0, inplace = True)



    # seperating member(memDrop) and intrest(intDrop) index to seperate member data
    # and their payable intrest data.
    memDrop = []
    intDrop = []

    # Clean data and fill empty(nan) spaces for intrest data frame
    # len(df)-1 to remove last row as it contains only Totalsum
    # Also, Remove white/unwated space from Flat No column

    #for i in range(1, len(df)-1): 
    for i in range(1, len(df)): 
        if i%2 == 0:
            if (np.isnan(df.loc[i,"FLATNO."])):
                df.loc[i, "FLATNO."] = df.loc[i-1, "FLATNO."]

            df.loc[i,"M.SHIPNO."] = df.loc[i-1,"M.SHIPNO."]
            intDrop.append(i)
        else:
            if (type(df.loc[i,"FLATNO."]) == str):
                df.loc[i,"FLATNO."] = df.loc[i,"FLATNO."][0] + df.loc[i,"FLATNO."][2:]

            memDrop.append(i)


    df = df.replace(np.nan, 0)

    df_Member = df.drop(labels = intDrop, axis=0)
    df_Intrest = df.drop(labels = memDrop, axis=0)

    # df_Member = df_Member.replace(np.nan, 0)
    # df_Intrest = df_Intrest.replace(np.nan, 0)

    totalMaint = []
    totalIntMaint = []
    for i, row in df_Member.iterrows():
        if i > 0 and row["NAME"] != 0 :
            # print(i, end=" ")
            totalMaint.append(round(sum([row[j] for j in df_Member.columns if "MAINT" in j])))
        else:
            totalMaint.append(0)


    for i, row in df_Intrest.iterrows():
        if i > 0 and row["NAME"] != 0:
            totalIntMaint.append(round(sum([row[j] for j in df_Intrest.columns if "MAINT" in j])))
        else:
            totalIntMaint.append(0)

    df_Member["Maintenance Dues"] = totalMaint
    df_Intrest["Interest on Maintenance"] = totalIntMaint

    return df_Member, df_Intrest





def searchData(flatNo, memNumber,membersDF, intrestDF):


    if (flatNo.isalnum()):
        xI = list(membersDF['FLATNO.']).index(flatNo)
    else:
        xI = list(membersDF['M.SHIPNO.']).index(memNumber)

    # Matching index with the index of excel file
    xI = xI*2 - 1

    dictMember = dict(membersDF.loc[xI])
    dictInterest = dict(intrestDF.loc[xI+1])

    # Chanaging key names to make easier for querry in document
    data = {"Name" : dictMember["NAME"], "FlatNo" : dictMember["FLATNO."],
            "MemberNo" : int(dictMember["M.SHIPNO."])}


    #Get All maintainence balance and intrest on the maintainence
    maintColName = [mc for mc in list(dictMember.keys()) if "MAINT" in mc]

    # Calculate the maintenance balance for selected member
    maintDue = [dictMember[maintColName[i]] for i in range(0,len(maintColName))]

    # Calculate interest on maintenance balance for selected member
    maintIntrest = [dictInterest[maintColName[i]] for i in range(0,len(maintColName))]

    ConstCost = [x for x in list(dictMember.keys()) if "CONSTRUCT" in x]


    # Adding total previous maintenance dues and interest to dictionary for querry
    data["PMB"] = round(sum(maintDue))
    data["PMI"] = round(sum(maintIntrest))

    # Construciton cost and interest
    if len(ConstCost) == 0:
        data["CCB"] = 0
        data["CCI"] = 0
    else:
        data["CCB"] = round(dictMember[ConstCost[0]])
        data["CCI"] = round(dictInterest[ConstCost[0]])

    data["PMTD"] = data["PMB"] + data["PMI"]
    data["CCTD"] = data["CCB"] + data["CCI"]
    data["Date"] = date.today().strftime("%d/%m/%Y")


    return data




def GenerateDocx(FlatNo, memberNo, nextMC, membersDF, intrestDF, templateFile, folderName):
    
    if memberNo.isnumeric():
        memberNo = int(memberNo)

    Data = searchData(FlatNo, memberNo, membersDF, intrestDF)
    # Next Maintenance Charges
    Data["NMC"] = nextMC

    # Total (Grand Total) of the maintenance charges
    Data["GT"] = Data["PMTD"] + Data["CCTD"] + Data["NMC"]

    if Data["MemberNo"] == 0:
        Data["MemberNo"] = "N/A"
    if Data["FlatNo"] == 0:
        Data["FlatNo"] = "N/A"

        
    doc = DocxTemplate(templateFile)
    doc.render(Data)
    
    # Path and name of new file created
    if (Data["FlatNo"].isalnum()):
        outfileName = folderName + Data["FlatNo"] + ".docx"
    else:
        outfileName = folderName + "MNo-" + str(Data["MemberNo"]) + ".docx"

    doc.save(outfileName)

    return



# Generate defaulter's list in an excel file
def generateDefaulters(membersDF, intrestDF, dirName):


    zeroRows = [i for i in membersDF.index if membersDF.loc[i]["NAME"] == 0]
    membersDF.drop(zeroRows, inplace = True)
    
    # Remove last row index
    zeroRows.remove(zeroRows[len(zeroRows)-1])

    # zeroRows = [i for i in intrestDF.index if intrestDF.loc[i]["NAME"] == 0]
    intrestDF.drop([i+1 for i in zeroRows], inplace = True)

    defaulterDF = membersDF.filter(["SL.NO.","NAME", "M.SHIPNO.", "FLATNO.", "Maintenance Dues"], axis=1)
    defaulterDF["Interest on Dues"] = intrestDF["Interest on Maintenance"].values



    #defaulterDF = defaulterDF.join(intrestDF["FlatNo.INT"])
    defaulterDF.rename(columns = {'FLATNO.':'Flat No.'}, inplace = True)
    defaulterDF.rename(columns = {'M.SHIPNO.':'Membership No.'}, inplace = True)
    defaulterDF["Total Maintenance Dues"] = defaulterDF["Maintenance Dues"] + defaulterDF["Interest on Dues"]

    # Get date of dues calculation form excel file
    excelDate = str(defaulterDF["NAME"][0])
    excelDate = excelDate.split()


    # Remove all 0 dues values i.e. non defaulters from Data Frame
    index_names = defaulterDF[ defaulterDF['Maintenance Dues'] == 0 ].index
    defaulterDF.drop(index_names, inplace = True)
    defaulterDF.replace(0, np.nan, inplace = True)

    # Adding final comment
    defaulterDF.loc[len(defaulterDF)] = [" " for _ in defaulterDF.columns]
    defaulterDF.loc[len(defaulterDF)] = ["##", " NOTE : The dues are calculated till ", excelDate[0], " ", " ", " ", " "]

    fileName = dirName + "Defaulters_List_" + date.today().strftime("%m-%Y") + ".xlsx"
    defaulterDF.to_excel(fileName, index = False)

    return




def main(dataFileName, FlatNo, memberNo, nextMC, templateFile, dirName):

    # Replace all Non available values (nan) by 0
    membersDF, intrestDF = getData(dataFileName)


    if (FlatNo.isalpha()):
        if FlatNo == 'ALL':
            print("All Flat numbers selected")
            allValues = membersDF["FLATNO."]
            FlatNo = [i for i in allValues if i!=0]
            for i in FlatNo:
                GenerateDocx(i, memberNo, nextMC, membersDF, intrestDF, templateFile, dirName)

        else:
            print("\nERROR INVALID INPUT :: Please check your input and run the code again\n")
            sys.exit("INVALID INPUTS")

    elif memberNo.isalpha():
        memberNo = memberNo.upper()
        if memberNo == 'ALL':
            print("All Member numbers selected")
            allValues = membersDF["M.SHIPNO."]
            memberNo = [str(int(i)) for i in allValues if i!=0]
            for i in memberNo:
                GenerateDocx(FlatNo, i, nextMC, membersDF, intrestDF, templateFile, dirName)

        else:
            print("\nERROR INVALID INPUT ::  Please check your input and run the code again\n")
            sys.exit("INVALID INPUTS")

    else:
        GenerateDocx(FlatNo, memberNo, nextMC, membersDF, intrestDF, templateFile, dirName)


    print("\nMaintenance demand letters generated in folder = {} ".format(dirName))
    _ = input("## PRESS ENTER TO EXIT ##\n")


    return




def mainDefaulter(dataFileName,dirName):

    # Replace all Non available values (nan) by 0
    membersDF, intrestDF = getData(dataFileName)


    # Defaulter list generation block
    generateDefaulters(membersDF, intrestDF, dirName)

    print("\nMaintenance defaulters's list generated in folder = {} ".format(dirName))
    _ = input("## PRESS ENTER TO EXIT ##\n")

    return


