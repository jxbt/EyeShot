# About
EyeShot is a tool written in python3 designed to take screenshots for a list of websites and collect basic info about.


# Features

* simple & multi-threaded.
* the ability to collect info about the websites that you want to screenshot.
* decide which websites that you want screenshot or collect info about based in response status code.
* decide which websites that you do not want screenshot or collect info about based in response status code.




# Usage

the below command will display all the options that you can use and some examples.
```
eyeshot -h
```



### Flags


| Flag            | Description                                                                        | 
| --------------- |------------------------------------------------------------------------------------|
| -f, --file      |  the file containing URLS to screenshot and collect info about (required)          |                    
| -o, --outdir    |  the output folder path (required)                                                 |                    
| -t, --threads   |  the amount of threads (optional) (default is 1)                                   |                    
| -h, --help      |  show the help menu (optional)          |                    
| -v, --verbose   |  verbose mode (optional)          |                    
| --cc            |  specify which responses/pages you want to screenshot and collect info about according to the response status code (optional)          |                    
| --dc            |  specify which responses/pages you don't want to screenshot and collect info about according to the response status code (optional)          |                    
| --lt            |  page loading timeout in seconds before taking the screenshot (optional) (default is 90)          |                    
| --rt            |  request timeout in seconds (optional) (default is 60)          |                    
| --cl            |   collect info about the URLs that you want to screenshot and store it in 00_meta.json (optional) (default is False)          |    


### Demo

#### ```eyeshot -f urls.txt -o shots -t 5 -v```

![demo 1](https://github.com/Jxbt/EyeShot/blob/main/img/1.gif)




#### ```eyeshot -f urls.txt -o shots -t 10 --cc 2xx,302 --cl```

![demo 2](https://github.com/Jxbt/EyeShot/blob/main/img/2.gif)




# Installation

#### run the following command to install eyeshot along with all dependencies and requirements.

```
chmod +x install.sh; sudo ./install.sh
```

# Notes: 

* before installation make sure that you have the latest version of geckodriver.
* you can't use both --cc &  --dc options at the same time.
