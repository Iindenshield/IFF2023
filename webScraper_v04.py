import bs4, requests, webbrowser

#FILE --------------------------------------------------------------------------------------------------------
html_file = 'C:/Users/lindenshield/Downloads/A Runner - FilmFreeway.html'
info_file = 'C:/Users/lindenshield/Desktop/info.txt'
#------------------------------------------------------------------------------------------------------------

credits_diz = {'Director': [], 'Writer': [], 'Producer': []}
bio_str = ''
overview_str = ''

soup = bs4.BeautifulSoup(open(html_file, encoding="utf8"), 'html.parser')

#GET CREDITS --------------------------------------------------------------------------------------------------
parent_ul = soup.find('ul', class_="credit-details list list--no-padding list--bordered")
all_li_tags = list(parent_ul.descendants)
li_list = [li.text.replace('\n', '') for li in all_li_tags if li.text.strip() != '']


for li in li_list:
    if 'Director' in li and len(li) != len('Director'):
        if li.removesuffix('Director') not in credits_diz['Director']:
            credits_diz['Director'].append(li.removesuffix('Director'))
    elif 'Writer' in li and len(li) != len('Writer'):
        if li.removesuffix('Writer') not in credits_diz['Writer']:
            credits_diz['Writer'].append(li.removesuffix('Writer'))
    elif 'Producer' in li and len(li) != len('Producer'):
        if li.removesuffix('Producer') not in credits_diz['Producer']:
            credits_diz['Producer'].append(li.removesuffix('Producer'))

#print(credits_diz)

#GET BIO -----------------------------------------------------------------------------------------------------
for bio_div_tag in soup.find_all('div', class_="press-kit__director-biography"):
    for bio in bio_div_tag.find_all('p'):
        bio_str = bio.text

#print(bio_str)

#GET OVERVIEW ------------------------------------------------------------------------------------------------
for overview_div_tag in soup.find_all('div', class_="project-details press-kit HACK-removeParagraphMargin"):
    for overview in overview_div_tag.find_all('p'):
        overview_str = overview.text
    
#print(overview_str)

#WRITE INFO.TXT ------------------------------------------------------------------------------------------------
with open(info_file, 'w', encoding="utf8") as info:
    info.write(overview_str)
    info.write(bio_str)
    for k,vv in credits_diz.items():
        for v in vv:
            info.write(v + ':' + k)

#crea cartella per ogni corto con:
#    info.txt
#    jpg e trailer

#GET TRAILER
"""
base_url = 'https://filmfreeway-production-storage-01.s3.us-west-2.amazonaws.com/press_kits/trailers/'

trailer_list = soup.find_all('div', class_="project-steps__step project-steps__step--3 active show")

for item in trailer_list:
    for link in item.find_all('a', href=True):
        print(link['href'])
"""
