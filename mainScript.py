#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 04:16:00 2021

@author: abhishek
"""


# Import supporting functions for the main code
import Functions as Fn

# Os library to run system commands (on OS)
import os

# Module to get today's date
from datetime import date


# The main code
if __name__ == "__main__":

    # Path/FileName with extension. Here data file is excel member data
    dataFileName = "Member_Outstanding_Manokamna.xls"
    
    # template document file which is used as the base for demand letters
    templateFile = "TemplateMTC.docx"

    FlatNo, memberNo, nextMC = Fn.getInputs()

    # Name of the output folder where all files would be saved
    folderName = "Maintenance_Demand_" + date.today().strftime("%m-%Y") + "/"
    
    #Make folder to save all letters
    if os.path.isdir(folderName) == False:
        os.mkdir(folderName)

    Fn.main(dataFileName, FlatNo, memberNo, nextMC, templateFile, folderName)

