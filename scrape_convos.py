
''' Code to scrape the conversations for ESL learning that we want to use to 
get baselines for human responses to natural conversations. Scraping foundation is courtesy of the 
tutorial found at https://realpython.com/python-web-scraping-practical-introduction/, specifically
the functions simple_get, is_good_response, log_error. All other code was written by Eddie Cohen.''' 

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)



def main():

    baseURLs = ['https://www.rong-chang.com/easyspeak/', 'https://www.eslfast.com/robot/',
    'https://www.rong-chang.com/speak/', 'https://www.eslfast.com/easydialogs/']

    URLs = ['https://www.rong-chang.com/easyspeak/index.htm', 'https://www.eslfast.com/robot/', 
    'https://www.rong-chang.com/speak/', 'https://www.eslfast.com/easydialogs/index.html']

    convo_count = 0

    for i,url in enumerate(URLs):
        identifier = url.split("/")[3]      # identifier will be used to name our directories
        if not os.path.exists(identifier):
            os.mkdir(identifier)
            print("Directory ", identifier, " Created ")
        else:
            print("Directory ", identifier, " already exists")

        
        #with open(os.path.join(identifier,filename),'w') as temp_file:    # example code for putting a file into a certain directory
        #    temp_file.write("yo")
        #dirc = "test_dir"
        #path = os.path.join(identifier,dirc)                              # creates path that is directory/subdirectory
        #if not os.path.exists(path):                                      # example code for creating a directory inside a directory 
        #    os.mkdir(path)
        #    print("Directory ", path, " Created ")
        #else:
        #    print("Directory ", path, " already exists")

        '''This block below captures the links to all of the different topics for each ESL site'''

        raw_html = simple_get(url)          
        html = BeautifulSoup(raw_html, 'html.parser')       
        ps = html.select('p')
        if not identifier=='easydialogs':   
            for p in ps:
                if 'class' in p.attrs:
                    if p.attrs['class']==['MsoNormal']:
                        links_p = p
                        topic_links =links_p.select('a')
        else:
            plinks = ps[0:17]
            topic_links = []
            for a in list(map(lambda l: l.select("a"), plinks)):
                topic_links = topic_links + a

        '''This block below captures the links to all of the different conversations once within a topic'''

        for topic_link in topic_links:
            topic_url = baseURLs[i]+topic_link.attrs["href"]
            topic_raw_html = simple_get(topic_url)
            topic_html = BeautifulSoup(topic_raw_html, 'html.parser')

            topic_name = topic_html.select('title')[0].text                         # creates a directory in the ESL directory for the specific topic 
            topic_path = os.path.join(identifier, topic_name)
            if not os.path.exists(topic_path):
                os.mkdir(topic_path)
                print("Directory ", topic_path, " Created ")
            else:
                print("Directory ", topic_path, " already exists")

            convo_links = topic_html.select('a')
            convo_links = convo_links[0:len(convo_links)-1]

            '''This block below accesses each conversation page and puts the convesation into a text file which is saved in the appropriate directory based on the ESL site and topic'''
            for convo_link in convo_links:
                convo_count+=1
                if i!=1:                                                        # this if-else is to handle a formatting difference in the urls for different conversations
                    convo_url = baseURLs[i]+convo_link.attrs["href"]
                else:
                    convo_url = topic_url[0:topic_url.rfind("/")+1]+convo_link.attrs["href"]
                convo_raw_html = simple_get(convo_url)
                convo_html = BeautifulSoup(convo_raw_html, 'html.parser')
                

                title = convo_html.select("b")[0].text                      # gets the title of the conversation for the purpose of naming the txt file
                if title=="":
                    title = convo_html.select("b")[1].text
                
                # for each ESL page the conversations are formatted in a different way. This if-else block captures the differences appropriately.
                if i==1:
                    convo_count+=2                                                    # some pretty poor code right here but it gets the job done
                    big_mess = convo_html.select("td")[1].text
                    less_big_mess = big_mess[big_mess.find("Repeat")+6:]
                    convo1 = less_big_mess[0:less_big_mess.find("so.addVariable")]
                    less_mess = less_big_mess[less_big_mess.find("Repeat")+6:]
                    convo2 = less_mess[0:less_mess.find("so.addVariable")]
                    almost_no_mess = less_mess[less_mess.find("Repeat")+6:]
                    convo3 = almost_no_mess
                    with open(os.path.join(topic_path,title),'w') as convo_file:
                        convo_file.write(str(convo1))
                        convo_file.write(str(convo2))
                        convo_file.write(str(convo3))           
                elif i==2:
                    convo = convo_html.select("blockquote")[0].text
                    with open(os.path.join(topic_path,title),'w') as convo_file:
                        convo_file.write(str(convo))
                else:                                                            # the first and the fourth ESL sitess are formatted the same way so both are handled with this else block
                    convo = convo_html.find_all("p",class_="MsoNormal")[0]       # figured out a better way to do the code in lines 87-91 lol
                    with open(os.path.join(topic_path,title),'w') as convo_file:
                        convo_file.write(str(convo))

    #print(convo_count)             # in total we have 2658 conversations, some of the conversation pages have multiple conversations on them, so we have even more than that

            
if __name__=="__main__":
    main()

