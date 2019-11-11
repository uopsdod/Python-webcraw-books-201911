### [ how to run the project ]
#### 1. install python3 
#### 2-1. install git 
#### 2-2. git clone this project

git clone https://github.com/uopsdod/Python-webcraw-books-201911.git

#### 2-3. go to the project folder 

cd Python-webcraw-books-201911

#### 3. create and use a python virtual environment

https://samcomlearning.blogspot.com/2019/11/python-create-virtual-environemnts-for.html

#### 4. install package 

pip install scrapy

#### 5. run the scrapy project 

scrapy crawl books

#### 6. leave the python virtual environment

deactivate



### [ how to check the result ]

ls CrawlBookPython3001/output

you should see following three output files: 

bookcrawler_result.jl  categoryworker_result.txt  discountworker_result.txt


### [ custom Configurations ]

CrawlBookPython3001/settings.py: DISCOUNTWORKER_RELATIVE_NTH parameter

this defines the top n% book to be returned according to the discounts 


