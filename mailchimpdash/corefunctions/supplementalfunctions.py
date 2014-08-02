import urllib2
import urllib
from mailchimpdash.models import *
# Create your views here.
from PIL import Image
from photohash import *
from fuzzywuzzy.fuzz import ratio


def urlfinder(thelink):
    try:
       dlink=urllib2.urlopen(thelink)
       return dlink.geturl()
    except:
        print "ERROR"
        return 'ERROR + thelink'
def ImageExtractor(text):
   #print text.encode('utf-8')
   #if 'https://gallery.mailchimp.com' in text:
       #print "IT IS HERE"
   imgs=[] 
   line=''
   for j in range(0,len(text),1):
        #print len(text), type(text), len(range(0,len(text),1))
        char=text[j]
        #print char, text[j+1], j
        line=line+char
        if '\n' in line:
           # print "AAPP"
            if 'https://gallery.mailchimp.com' in line:
            #    print " HAPPY DAY"
                li=''
                for i in line:
                    li=li+i
                    if 'src="' in li:
                        li=''
                    if '.jpg' in li:
                        #print "GOT URL"
                        imgs.append(li)
                        li=''
            line=''

   return imgs

def updateImages():
        emails=Email.objects.all()
        #print emails
        for msg in emails:
            imglinks=ImageExtractor(msg.Email_html.encode('utf-8'))
            imghashes=ImageHasher(imglinks)
            ImageMatcher(msg.Campaign_id, imghashes)


def ImageMatcher(cid,imglinks,imghashes):
    #Search Facebook
    posts=FacebookPost.objects.all() #TODO Restrict search
    for item in imghashes:
        posts=[post for post in posts if post.ImageSearch(item[1])]
        for post in posts:
            E=EmailPictures(idnum=post.postid+cid+item[1][0:53]+ImgURL,Campaign_id=cid, Image=item[1],ImgURL=item[0], ImgMatch=post)
            E.save()



def ImageHasher(imgs):
    images=[]
    for item in imgs:
        #get picture
	urllib.urlretrieve(item.encode('utf-8'),"temp_picM.jpg")
	img=Image.open('temp_picM.jpg')
        basewidth=130
        wpercent=(basewidth/float(trial1.size[0]))
        hsize=int((float(trial1.size[1])*float(wpercent)))
        img=img.resize((basewidth,hsize),Image.ANTIALIAS)
        img.save('temp_picM2.jpg')
        Img1 = average_hash("temp_picM2.jpg", hash_size =64)
        images.append([item,Img1])
    return images
    
def FacebookLinkExtractor(text):
  posts=[]
  line=''
  for char in text:
    line=line+char
    if char=='\n':
        if 'http://www.facebook.com/sharer/sharer.php?u=' in line:
           b= urllib.unquote(line[44:].encode('utf-8'))
           post=''
           for char in b:
                post=post+char
                if 'Share' in post:
                    post=post[:-5]
                    posts.append(urlfinder(post))
                    break
        line=''
  return posts


        

def ExtractTweets(text):
  Tweets=[]
  line=''
  for char in text:
    line=line+char
    if char=='\n':
        if 'http://twitter.com/intent/tweet?text=' in line:
           b= urllib.unquote(line[37:].encode('utf-8'))
           tweet=''
           for char in b:
                tweet=tweet+char
                if 'Tweet' in tweet:
                    tweet=tweet[:-5]
                    Tweets.append(tweet)
                    break
        line=''
  return Tweets

def fuzzsearch(q,d1,d2):

	    twittertweets = TwitterTweet.objects.filter(created_time__range=[d1,d2])
            print "APPLE"
	    twittertweets = [post for post in twittertweets if post.fuzzy_serach(q)]
        
            return twittertweets
