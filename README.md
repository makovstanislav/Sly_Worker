**SLY WORKER**

DESCRIPTION: an application that allocates a bunch of your documents into folders.

Table of contents:

**INSTALLATION:**

  1. Install LibreOffice
  
  For the proper functioning of the app LibreOffice (ver 7.1.4) must be installed. 
  Please use the download link below: 

  https://www.libreoffice.org/download/download/
  
  2. Download SlyWorker.app by the link:
 
  https://www.libreoffice.org/download/download/
  
  3. Download "data.yaml" by the link:
  
  https://www.libreoffice.org/download/download/
  
  4. Put downloaded files "SlyWorker.app" and "data.yaml" into the same folder.
     
**USAGE:**
  
  1. Customize YAML file.
     
     Open "data.yaml" file via any text editor you are comfortable with. 
  
     This file stipulates sorting criteria which the app governs by. You should specify the categories and subcategories 
     (if any) into which you would like to pigeonhole your documents. As soon as you start sorting, the program 
     will automatically create folders and subfolders by the names of categories and subcategories respectively. 
     
     **Feel free to customize it as you like!**
     
     There are the following fields:
     
     1. Name of a type/subtype. That means the name of the category/subcategory. 
     2. "uniques" – the keywords that the document of certain category (type) has to contain. 
        Numerical value of each "unique" is the minimum number of keyword occurences in the document.
     3. "unq_req" – the minimum number of "uniques" validations. The document may have the required number for keywords quantity (uniques)
        but at the same time it may not contain all of the unique keywords that you specified. So, how much "uniques" shall be matched
        to recognize the document as belonging to the certain category?
     
     You can add, delete, rename fields with preservation of the current layout and indentation. The number of fields "type"/"subtype"/"uniques"
     is not limited. The maximum number of the field "unq_req" for each type/subtype is 1.
     
     Save the file after customization.
        
  2. Sort
  
     Insert a bunch of your documents that you are going to sort into a separate folder. Launch "SlyWorker.app". Select the folder
     containing such documents (source folder). Select the folder which will contain folders with allocated documents (output folder).
     
     Click "Sort" button!
     
     The process gonna take a while. The app will not respond during that time. That is OK. The app is at beta stage. 

  3. Put the screws on!

     Look at the statistics of the sorting. Are you satisfied with the result? If you feel that it could be better, reconfigure "data.yaml" file.
  
  
  Thank you for being interested in SlyWorker!
