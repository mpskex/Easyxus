#coding:gb2312
from PIL import Image, ImageFilter, ImageDraw
import urllib
import requests
import pytesseract 
from bs4 import BeautifulSoup
##mpsk:北京工业大学
##访问教务管理系统并格式化获取消息
s = requests.session()

viewstate = 'dDwyODE2NTM0OTg7Oz59ca9xYUSOmxpdVOe+y/beTvvgZg=='
Usernum = str(15143103)
Username = ''
Password = ''
mode = '学生'
template_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'ASP.NET_SessionId=dvq1xt45aqrdpv55hfrt5lik',
            'Host':'gdjwgl.bjut.edu.cn',
            'Origin':'http://gdjwgl.bjut.edu.cn',
            'Referer':'http://gdjwgl.bjut.edu.cn/default2.aspx',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

##高斯模糊
class MyGaussianBlur(ImageFilter.Filter):
    name = "MyGaussianBlur"
    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds
 
    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


def ocr():
    threshold = 115
    table = []  
    ##生成 
    for i in range(256):  
        if i < threshold:  
            table.append(0)  
        else:  
            table.append(1)  
    #由于都是数字和字母 
    #对于识别成符号的 采用该表进行修正
    rep = {'/':'l'}
    '''
    rep = {'O':'0',  
    'I':'1','L':'1',  
    'Z':'2',  
    'S':'8'  
    }
    '''
    ## 使用pytesseract对验证码进行解码
    ##打开图像
    #imageobj = img
    imageobj = Image.open('code.gif')
    ##将图片高斯模糊   
    G_imageobj = imageobj.convert('RGB').filter(MyGaussianBlur(radius = 0.7))
    #G_imageobj = imageobj
    #G_imageobj.save('G_imageobj.bmp')
    ##将验证码灰度化
    L_imageobj = G_imageobj.convert('L')
    ##将图片保存
    #L_imageobj.save('L_code.bmp')
    ##二值化图片
    out = L_imageobj.point(table, '1')
    #out.save('B_code.bmp')
    ##粗文本输出
    outcode = pytesseract.image_to_string(out)
    ##格式化输出
    txtSecretCode = []
    for n in list(outcode):
        if (n.isdigit() or n.isalpha()): txtSecretCode.append(n)
    codetext = ''.join(txtSecretCode)
    #识别对吗    
    codetext = codetext.strip()    
    codetext = codetext.upper();      
    for r in rep:    
        codetext = codetext.replace(r,rep[r])
    print codetext
    return codetext

def login():
    while(1):
        ##下载验证码
        main = s.get('http://gdjwgl.bjut.edu.cn/')
        check = s.get('http://gdjwgl.bjut.edu.cn/checkcode.aspx')
        dimage = check.content
        with open("code.gif", 'wb') as img:
            img.write(dimage)
        img.close
        codetext = ocr()
        #codetext = raw_input();
        
        ##打包验证data包
        Auth = {'__VIEWSTATE':viewstate,
                'txtUserName': Usernum,
                'TextBox2': Password,
                'txtSecretCode': codetext,
                'RadioButtonList1': mode,
                'Button1':'',
                'lbLanguage':'',
                'hidPdrs':'',
                'hidsc':''}
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Host':'gdjwgl.bjut.edu.cn',
                    'Origin':'http://gdjwgl.bjut.edu.cn',
                    'Referer':'http://gdjwgl.bjut.edu.cn/default2.aspx',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        #print Auth
        req = s.post('http://gdjwgl.bjut.edu.cn/default2.aspx', Auth)
        Areq = s.get(('http://gdjwgl.bjut.edu.cn/xs_main.aspx?xh=' + Usernum), data = {'xh':Usernum})
        '''
        req = requests.post('http://gdjwgl.bjut.edu.cn/default2.aspx', data = Auth, headers = headers)
        Areq = requests.get(('http://gdjwgl.bjut.edu.cn/xs_main.aspx?xh=' + Username), cookies = req.cookies)
        print('HTTP GET CODE : %d\n'%(req.status_code))
        print Areq.url
        print Areq.headers
        '''
        print('>>HTTP GET CODE : %d'%(req.status_code))
        soup = BeautifulSoup(Areq.text, "lxml")
        if (soup.title.string.encode('gbk') == "正方教务管理系统"):
            print "命中"
            return req.cookies


def main():
    cookie = login()
    header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate,sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'gdjwgl.bjut.edu.cn',
            'Referer':'http://gdjwgl.bjut.edu.cn/xs_main.aspx?xh=15143103',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    print "成功登陆！"
    info = s.get('http://gdjwgl.bjut.edu.cn/xsgrxx.aspx?xh=' + Usernum + '&xm=' + urllib.quote(Username) + '&gnmkdm=N121501',headers = header)
    with open("self_info.html", 'wb') as f:
        f.write(info.content)
    f.close
    image = s.get('http://gdjwgl.bjut.edu.cn/readimagexs.aspx?xh=' + Usernum + '&xm=' + urllib.quote(Username) + '&gnmkdm=N121501',headers = header)
    with open("image.gif", 'wb') as f:
        f.write(image.content)
    f.close
    class_table = s.get('http://gdjwgl.bjut.edu.cn/xskbcx.aspx?xh=' + Usernum + '&xm=' + urllib.quote(Username) + '&gnmkdm=N121603',headers = header)
    with open("class_table.html", 'wb') as f:
        f.write(class_table.content)
    f.close
    

if __name__ == '__main__':
    main()