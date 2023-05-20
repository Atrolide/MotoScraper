import requests
from bs4 import BeautifulSoup

html = '<img class="bigImage landscape" data-nr="0" data-tracking="gallery_open" onload="(this.className+=this.clientWidth>this.clientHeight?\' landscape\':\' portrait\')" alt="Opel Mokka Innovation 1.7ctdi Automat Xenon Wyposażona Opłacona - 1" src="https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImFoa2V4c2Q5c2o1OS1PVE9NT1RPUEwiLCJ3IjpbeyJmbiI6IndnNGducXA2eTFmLU9UT01PVE9QTCIsInMiOiIxNiIsInAiOiIxMCwtMTAiLCJhIjoiMCJ9XX0.PxmswA0ajpcMzcADf2OiME9vWXvaMuFxRHjbSCxlAs0/image;s=1080x720" style="opacity: 1;">'
start = html.find('src="') + len('src="')
end = html.find('"', start)
img_url = html[start:end]
print(img_url)


