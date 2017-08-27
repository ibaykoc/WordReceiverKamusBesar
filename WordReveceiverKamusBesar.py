import requests,urllib,re,string,sys
from lxml import etree

#Create session with header
session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'}

#Request token
tokenRequest = session.get('https://kbbi.kemdikbud.go.id/Account/Login',headers=headers)

#Get parsed verification token
parser = etree.HTMLParser()
tree = etree.fromstring(tokenRequest.text, parser)
verificationToken = tree.xpath('//form//input[@name="__RequestVerificationToken"]/@value')[0]

#Get session cookies
sessionCookies = tokenRequest.cookies

#Create and parse form payload
payload = {
    '__RequestVerificationToken': verificationToken,
    'Posel':'morelivemoredie@gmail.com',
    'KataSandi':'Trustonlyone1',
    'IngatSaya':'false'
}
raw = urllib.parse.urlencode(payload)

#Login
r = session.post('https://kbbi.kemdikbud.go.id/Account/Login', data=raw, cookies=sessionCookies, headers=headers)
if re.match('ibaykoc',r.text):
    print('Login Success')
else:
    print(r.text)
    print('Login Failed')
    sys.exit()
#Declare address
address = ''

# loop for all prefix word
for i in range(0,1):
    address = 'https://kbbi.kemdikbud.go.id/Cari/Alphabet?masukan=%s&masukanLengkap=%s&page=1' % (string.ascii_uppercase[i],string.ascii_uppercase[i])
    
    #Get last page in current prefix word
    page_source = session.get(address).text
    lastPageId = (int)(re.findall('page=(\d+)"\s+class="btn btn-default btn-xs"\s+title="Ke halaman terakhir">?',page_source,re.DOTALL)[0])
    print('Total page with prefix %s is: %d' % (string.ascii_uppercase[i],lastPageId))
    
    #Declare wordlist
    wordlist = []

    #loop for all page
    for x in range(1,lastPageId + 1):
        print('Getting word with prefix %s, in page: %d' % (string.ascii_uppercase[i],x))
        #Get page_source in current page
        address = 'https://kbbi.kemdikbud.go.id/Cari/Alphabet?masukan=A&masukanLengkap=A&page=%d' % x
        page_source = session.get(address).text
        #Get all the word in page
        wordsInPage = re.findall('<div class="col-md-3">\s*<a href="/entri/.*?">\s*(.*?)\s*</a>',page_source,re.DOTALL)

        #Remove tag <sup> & </sup> in all the word in page
        for x in range(0,len(wordsInPage)):
            wordsInPage[x] = re.sub('<sup>',' ',wordsInPage[x])
            wordsInPage[x] = re.sub('</sup>','',wordsInPage[x])

        #Insert all the word in page to wordlist
        wordlist.extend(wordsInPage)
        print('Total words received: %d' % len(wordlist))


    #Save all the words in file
    print('Saving to Wordlists/Indonesian Wordlist KBBI prefix(%s).csv" % string.ascii_uppercase[i]')
    with open("Wordlists/Indonesian Wordlist KBBI prefix(%s).csv" % string.ascii_uppercase[i], "w") as outfile:
            outfile.write(wordlist)