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
import sys, os

# Module to get today's date
from datetime import date

# Create template from docx file to efficienty edit
from docxtpl import DocxTemplate

from werkzeug.utils import secure_filename



# Function to check if the given file extension is accepted for uploading or not.
def isAllowed(fileName, EXTENSIONS):
    nameSplit = fileName.split('.')
    nameSplit = nameSplit[len(nameSplit)-1]
    if nameSplit in EXTENSIONS:
        return True
    return False




# This function checks the uploaded file for the allowed extensions and returns "True" in case 
# all checks and preprocessing of the file was done successfully.
def fileUploadCheck_Preprocess(uploadedFileName, ALLOWED_EXTENSIONS, typeFile):

    result = True
    securedFileName = ""

    # Checking if uploaded data File in post request
    if isAllowed(uploadedFileName, EXTENSIONS=ALLOWED_EXTENSIONS):
        # session["allowedDataFile"] = True
        print("##{} File uploaded successfully in query page.\n".format(typeFile))
        securedFileName = secure_filename(uploadedFileName)
    else:
        print("!!!! # Error :: unable to upload file")
        # session["allowedDataFile"] = False
        result = False

    return result, securedFileName





def processUserInputs(flatNo, NextMC):

    flatNo = flatNo.upper()
    # membershipNo = membershipNo.upper() // DON'T ADD THIS LINE here

    # Set data type as integer
    NextMC = int(NextMC)
    return flatNo, NextMC



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
   
    if len(sys.argv) == 4:
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

    # read an excel file and convert into a dataframe object
    df = pd.DataFrame(pd.read_excel(dataFile))

    # Remove all white spaces and extra spaces from data column names for efficient calls
    for i in range(0, len(df.columns)):
        df = df.rename({df.columns[i]:"".join(df.columns[i].split()).upper()}, axis=1)

    # Remove any possible spaces from maintenance
    for i in df.columns:
        if "MAINT" in i or "CONSTRUCT" in i:
            df[i].replace(" ", np.nan, inplace = True)


    df = df.replace(np.nan, 0)

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
                df.loc[i, "FLATNO."] = "".join(df.loc[i,"FLATNO."].split())

            memDrop.append(i)


    df_Member = df.drop(labels = intDrop, axis=0)
    df_Intrest = df.drop(labels = memDrop, axis=0)


    totalMaint = []
    totalIntMaint = []
    totalConstructionBal = []
    interestConstruction = []
    for i, row in df_Member.iterrows():
        if i > 0 and row["NAME"] != 0 :
            # print(i, end=" ")
            totalMaint.append(round(sum([row[j] for j in df_Member.columns if "MAINT" and "CHARG" in j])))
            totalConstructionBal.append(round(sum([row[j] for j in df_Member.columns if "COST" and "CONSTR" in j])))
        else:
            totalMaint.append(0)
            totalConstructionBal.append(0)


    for i, row in df_Intrest.iterrows():
        if i > 0 and row["NAME"] != 0:
            totalIntMaint.append(round(sum([row[j] for j in df_Intrest.columns if "MAINT" and "CHARG" in j])))
            interestConstruction.append(round(sum([row[j] for j in df_Intrest.columns if "COST" and "CONSTR" in j])))
        else:
            totalIntMaint.append(0)
            interestConstruction.append(0)

    df_Member["Maintenance Dues"] = totalMaint
    df_Intrest["Interest on Maintenance"] = totalIntMaint

    df_Member["Construction Cost Due"] = totalConstructionBal
    df_Intrest["Interest on Construction Cost"] = interestConstruction

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
            "MemberNo" : int(dictMember["M.SHIPNO."]),
            "PMB" : dictMember["Maintenance Dues"], "PMI" : dictInterest["Interest on Maintenance"],
            "CCB" : dictMember["Construction Cost Due"], "CCI" : dictInterest["Interest on Construction Cost"]}


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
def generateDefaulters(membersDF, intrestDF, dirName, option):

    option = int(option)

    zeroRows = [i for i in membersDF.index if membersDF.loc[i]["NAME"] == 0]
    membersDF.drop(zeroRows, inplace = True)
    
    # Remove last row index
    zeroRows.remove(zeroRows[len(zeroRows)-1])

    # Drop all rows from interest Data frame with no member names (unalloted)
    intrestDF.drop([i+1 for i in zeroRows], inplace = True)

    defaulterDF = membersDF.filter(["SL.NO.","NAME", "M.SHIPNO.", "FLATNO."], axis=1)

    if option == 1 or option == 3:
        defaulterDF["Maintenance Dues"] = membersDF["Maintenance Dues"].values
        defaulterDF["Interest on Maintenance Dues"] = intrestDF["Interest on Maintenance"].values
        defaulterDF["Total Maintenance Dues"] = defaulterDF["Maintenance Dues"] + defaulterDF["Interest on Maintenance Dues"]
    if option == 2 or option == 3:
        defaulterDF["Construction Cost Due"] = membersDF["Construction Cost Due"].values
        defaulterDF["Interest on Construction Cost"] = intrestDF["Interest on Construction Cost"].values
        defaulterDF["Total Construction Const Due"] = defaulterDF["Construction Cost Due"] + defaulterDF["Interest on Construction Cost"]
    if option == 3:
        defaulterDF["Total Due"] = defaulterDF["Total Maintenance Dues"] + defaulterDF["Total Construction Const Due"]


    #defaulterDF = defaulterDF.join(intrestDF["FlatNo.INT"])
    defaulterDF.rename(columns = {'FLATNO.':'Flat No.'}, inplace = True)
    defaulterDF.rename(columns = {'M.SHIPNO.':'Membership No.'}, inplace = True)

    # Get date of dues calculation form excel file
    excelDate = str(defaulterDF["NAME"][0])
    excelDate = excelDate.split()

    # Remove all 0 dues values i.e. non defaulters from Data Frame
    if option == 1 or option == 3:
        noMaintDues_index= defaulterDF[ defaulterDF['Maintenance Dues'] == 0 ].index
    if option == 2 or option == 3:
        noConstDues_index = defaulterDF[ defaulterDF['Construction Cost Due'] == 0 ].index

    if option == 1:
        index_toDrop = [i for i in noMaintDues_index]
    elif option == 2:
        index_toDrop = [i for i in noConstDues_index ]
    else:
        index_toDrop = [i for i in noMaintDues_index if i in noConstDues_index ]

    # defaulterDF.drop(index_toDrop, inplace = True)
    defaulterDF.drop(index_toDrop, axis='index', inplace = True)
    defaulterDF["Membership No."].replace(0, np.nan, inplace = True)
    defaulterDF["Flat No."].replace(0, np.nan, inplace = True)

    # Adding space before final comment
    defaulterDF = defaulterDF.append(pd.Series([np.nan for _ in defaulterDF.columns], index=defaulterDF.columns), ignore_index=True)
    print("last 5 rows entries of DefaulterDF after append = \n", defaulterDF.tail())
    concatdefaulterDF = defaulterDF.concat(pd.Series([np.nan for _ in defaulterDF.columns], index=defaulterDF.columns), axis=0)
    print("last 5 rows entries of DefaulterDF after concat = \n", concatdefaulterDF.tail())

    if option == 1:
        defaulterDF.loc[len(defaulterDF)] = ["##", " NOTE : The dues are calculated till ", excelDate[0], excelDate[0], " ", "##", " "]
        fileName = dirName + "Maintenance_Defaulters_List_" + date.today().strftime("%m-%Y") + ".xlsx"
    elif option == 2:
        defaulterDF.loc[len(defaulterDF)] = ["##", " NOTE : The dues are calculated till ", excelDate[0], excelDate[0], " ", "##", " "]
        fileName = dirName + "Construction_Cost_Defaulters_List_" + date.today().strftime("%m-%Y") + ".xlsx"
    else:
        defaulterDF.loc[len(defaulterDF)] = ["##", " NOTE : The dues are calculated till ", excelDate[0], excelDate[0], " ", "##", " ", " ", " "," ", " "]
        fileName = dirName + "Defaulters_List_" + date.today().strftime("%m-%Y") + ".xlsx"

    # Export all data to excel file
    defaulterDF.to_excel(fileName, index = False)

    return fileName





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

    return





def mainDefaulter(dataFileName, dirName, option=""):

    # Replace all Non available values (nan) by 0
    membersDF, intrestDF = getData(dataFileName)

    if len(option) == 0:
        print("Please select tpye of defaulter List :: \n")
        print("[1] = Only Maintenance Dues Defaulters")
        print("[2] = Only Construction cost Defaulters")
        print("[3] = Both Construction and Maintenance Dues Defaulter\n")
        option = input("Type index of desired defaulter list then press ENTER = ")

    while(option.isnumeric() == False):
        print("\n## INVALID SELECTION ## please select again ##\n")
        option = input("Type index of desired defaulter list then press ENTER = ")

    while(int(option) > 4 or int(option) < 1 ):
        print("\n## INVALID SELECTION ## please select again ##\n")
        option = input("Type index of desired defaulter list then press ENTER = ")

    # Defaulter list generation block
    fileName = generateDefaulters(membersDF, intrestDF, dirName, option)

    # print("\nMaintenance defaulters's list generated in folder = {} ".format(dirName))
    # _ = input("## PRESS ENTER TO EXIT ##\n")

    return fileName

