# **SLY WORKER**

A desktop application that arranges (sorts out) a bunch of your documents into folders.
Operates on MacOS.

<img width="859" alt="Screenshot 2021-07-01 at 00 44 32" src="https://user-images.githubusercontent.com/85253471/124035851-cc2b1800-da05-11eb-9aed-6ed2d9b07f75.png">


<img width="1247" alt="Screenshot 2021-07-01 at 00 10 59" src="https://user-images.githubusercontent.com/85253471/124032336-207fc900-da01-11eb-9b5e-4e984e593bc7.png">
<img width="469" alt="Screenshot 2021-07-01 at 00 12 37" src="https://user-images.githubusercontent.com/85253471/124032347-237ab980-da01-11eb-8a00-8255cfb1b92a.png">



## **INSTALLATION:**



  1. Install LibreOffice
  
  For the proper functioning of the app LibreOffice (ver 7.1.4) must be installed. 
  Please use the download link below: 

  https://www.libreoffice.org/download/download/
  
  2. Download SlyWorker.app by the link:
 
  https://www.libreoffice.org/download/download/
  
  3. Download "data.yaml" by the link:
  
  https://github.com/MSt-gh/git_practice/blob/7f342ddd15d8c496f8debae3525d7019f2e36b86/data.yaml
  
  4. Put downloaded files "SlyWorker.app" and "data.yaml" into the same folder.
     
## **USAGE:**
  
####  1. Customize YAML file.
     
 <img width="964" alt="Screenshot 2021-06-30 at 23 16 01" src="https://user-images.githubusercontent.com/85253471/124026170-0393c780-d9fa-11eb-9ed8-083edced2d6b.png">
     
     Open "data.yaml" file via the text editor you are comfortable with. 
  
     This file stipulates sorting criteria which the app governs by. You should specify the categories and subcategories 
     (if any) into which you would like to pigeonhole your documents. As soon as you start sorting, the program 
     will automatically create folders and subfolders by the names of categories and subcategories respectively. 
 
 **Feel free to establish your own criteria by amending the file!** :pencil2:   

     There are the following fields:
     
     1. Name of a type/subtype. That means the name of the category/subcategory. 
     2. "uniques" – the keywords that the document of certain category (type) has to contain. 
        Numerical value of each "unique" is the minimum number of keyword occurences in the document.
     3. "unq_req" – the minimum number of "uniques" validations. The document may have the required number for 
        keywords quantity (uniques) but at the same time it may not contain all of the unique keywords that you specified. 
        So, how much "uniques" shall be matched to recognize the document as belonging to the certain category?
     
     You can add, delete, rename contents with preservation of the current layout and indentation.
     
     Save the file after customization.
        

####  2. Sort your documents.
  
 <img width="1257" alt="Screenshot 2021-06-30 at 23 25 47" src="https://user-images.githubusercontent.com/85253471/124027273-57eb7700-d9fb-11eb-96e6-8cb0e1b96b9e.png">
     

     Insert a bunch of your documents that you are going to sort into a separate folder. 
     Launch "SlyWorker.app". Select the folder containing such documents (source folder). Select the folder 
     which will contain folders with allocated documents (output folder).
     Click "Sort" button!
     
     The process gonna take a while. The app will not respond during that time. That is OK. The app is at beta stage. 
     
 <img width="827" alt="Screenshot 2021-06-30 at 23 33 30" src="https://user-images.githubusercontent.com/85253471/124027577-b6b0f080-d9fb-11eb-8a5b-6be2752f7a18.png">
     

####  3. Put the screws on!

     Look at the statistics of the sorting. Are you satisfied with the result? If you feel that it could be better, 
     then reconfigure "data.yaml" file.
  
 <img width="823" alt="Screenshot 2021-06-30 at 23 50 01" src="https://user-images.githubusercontent.com/85253471/124029669-0e505b80-d9fe-11eb-9441-0437f530986f.png">

  Thank you for being interested in SlyWorker! :mage:
