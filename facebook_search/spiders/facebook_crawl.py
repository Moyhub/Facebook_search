# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from lxml import etree
#from facebook_search.main import username,password,topic

class FacebookCrawlSpider(scrapy.Spider):
    name = 'facebook_crawl'
    starturls = 'https://www.facebook.com/login'
    '''登录时使用的脚本，在lua脚本中设置代理很必要'''
    script = '''
    function main(splash,args)
        splash:on_request(function(request)
            request:set_proxy{
            host = "127.0.0.1",
            port = 8118,
            type = 'http',
            }
            end)
        local ok, reason = splash:go(args.url)
        user_name = args.user_name
        user_passwd = args.user_passwd
        user_text = splash:select("#email")
        pass_text = splash:select("#pass")
        login_btn = splash:select("#loginbutton")    
       if (user_text and pass_text and login_btn) then
           user_text:send_text(user_name)       
           pass_text:send_text(user_passwd)
           login_btn:mouse_click({})
      end
      splash:wait(math.random(5,10))
       return {
           url = splash:url(),
           cookies = splash:get_cookies(),
           headers = splash.args.headers,
        }
    end'''
    '''构造函数与传参'''
    # def __init__(self,*args,**kwargs):
        #super().__init__(*args,**kwargs)
        # if 'password' not in kwargs:
        #     print("F")
        # else:
        #     print("P")
        # if 'username' not in kwargs:
        #     print("F")
        # else:
        #     print("参数传入成功!")
    def start_requests(self):
        print("模拟登陆Facebook账号")
        print(self.starturls)
        yield SplashRequest(
            url=self.starturls,
            endpoint= "execute",
            args={
                "wait": 3,
                "lua_source": self.script,
                 # "user_name":username,
                 # "user_passwd":password,
                  "user_name": '1164068826@qq.com',                          #self.username,
                  "user_passwd": 'zdx19980818',                              #self.password,
                "timeout": 3600,
            },
            callback = self.parse,
        )
    '''直接构造URL进入到搜索界面'''
    search = '''
    function main(splash,args)
        splash:on_request(function(request)
            request:set_proxy{
            host='127.0.0.1',
            port=8118,
            type='http',
            }
            end)
      splash:init_cookies(splash.args.cookies)
      splash:go(args.url)
      splash.images_enabled = False
      splash.media_source_enabled = False
      splash:wait(math.random(5, 10))

      return{
      url = splash:url(),
      cookies = splash:get_cookies(),
      html = splash:html(),
      }
      end
      '''
    def parse(self, response):
        print("正在查询你所感兴趣的内容...")
        self.cookies = response.data["cookies"] #cookies是一个list
        self.url_searchtopic = "https://www.facebook.com/search/top/?q=" + "特朗普" #self.topic
        return (SplashRequest(
            url = self.url_searchtopic,
            endpoint="execute",
            args={"lua_source":self.search,"cookies":self.cookies,"timeout":3600,},
            callback=self.parse_search,
        ))
    '''这里是通过点击得到的新的页面，但是后期的URL不太一样，所以这里我要找到public里面蕴含的URL（实际可以通过这个URL搞定）'''
    public = '''
    function main(splash,args)
        splash:on_request(function(request)
            request:set_proxy{
            host='127.0.0.1',
            port=8118,
            type='http',
            }
            end)
    splash:init_cookies(splash.args.cookies)
    splash:go(args.url)
    splash:wait(4)
    
    public_btn = splash:select("[class='_4f3b']:nth-of-type(5)")
    public_btn:mouse_click({})
    splash.images_enabled = False
    splash.media_source_enabled = False
    splash:wait(math.random(5, 10))
    return{
    url = splash:url(),
    cookies = splash:get_cookies(),
    html = splash:html(),
    }
    end        
    '''
    def parse_search(self,response):
        print("正在切换")
        self.URL = response.xpath("//*[@class='_4f38']/div/a[5]/@href").extract()
        self.cookies_p = response.data["cookies"]
        self.url_prepublic = response.data["url"] #这个URL是要的，这是还没有点击public时的URL,就是上文构造的URL
        return (SplashRequest(
            url=self.url_prepublic,
            endpoint="execute",
            args ={
                "lua_source":self.public,
                "cookies":self.cookies_p,
                "timeout": 3600,
            },
            callback = self.parse_getallpage,
        ))
    Get = '''
     function main(splash, args)
     splash:init_cookies(splash.args.cookies)
     splash:on_request(function(request)
        request:set_proxy{
            host = "127.0.0.1",
            port = 8118,
            }
            end) 
        splash.images_enabled = False
        splash.media_source_enabled = False  
        splash:go(args.url)
        splash:wait(0.5)  
        height = 0
        height0 = 1000
     while (height0 ~= height)
     do
         height = height0
         local scroll_to = splash:jsfunc("window.scrollTo")
         scroll_to(0, height)
         splash:wait(math.random(2, 3))
         width, height0 = splash:set_viewport_full()
     end    
     
     allpost = splash:select_all("div[class='_6-cp']")
     Content_list = {}
     local key = 0
     if (allpost ~=nil)
     then
        Num = 1
        for key, post in pairs(allpost) do
            post: mouse_click({})
            splash:wait(8)
            Getcontent = splash:select("div[class='_3ccb']")
            if (Getcontent == nil)
            then
                Content_list[Num] = " "
                Num = Num + 1
                post: mouse_click(1, 1)
                splash:wait(0.2)
            else
                Content_list[Num] = Getcontent.node.innerHTML
                Num = Num + 1
                post: mouse_click(1, 1)
                splash:wait(0.2)
            end
            if (Num == 5)
            then
                break
            end
        end
      end
    return
    {
        Num = Num,
        Content_list = Content_list,
        height = height,
        height0 = height0,
        html = html,
        cookies = splash:get_cookies(),
    }
    end
    '''
    '''这里我持续下滑将Facebook中相关的主题的页面全部得到,这里发现得到的url并不是splash返回的URL所以这里我们自己寻找，返回的是lua元组'''
    def parse_getallpage(self,response):
        print("正在爬取你想要的内容...")
        self.url_public = self.URL[0]
        self.cookies_c = response.data["cookies"]
        print(self.cookies_c)
        return(SplashRequest(
            url = self.url_public,
            endpoint = "execute",
            args = {
                "lua_source":self.Get,
                "cookies":self.cookies_c,
                "timeout":3600,
            },
            callback=self.collect,
            meta = {"download_timeout":3600}
        ))
    '''已经下滑到最下端success'''
    def collect(self,response):
        print("正在解析...")
        self.cookies_click=response.data["cookies"]
        self.Content = response.data["Content_list"]
        #下面进行解析
        for article in self.Content.values():
            if(len(article) == 0):
                continue
            post = etree.HTML(article)
            self.topic = post.xpath('string(//div[@data-testid="post_message"])')
            print(self.topic)
            self.name = post.xpath('string(//div[@class="_6a _5u5j _6b"]/h5/span)')
            print(self.name)
            self.data = post.xpath('//div[@class="_6a _5u5j _6b"]/div/span/span/a/abbr/span/text()')
            print(self.data)
            self.recommond_all = post.xpath('string(//div[@class="_66lg"]/a/span[2]/span)')
            print(self.recommond_all)
            self.comment_number = post.xpath('//div[@class="_4vn1"]/span/a/text()')
            print(self.comment_number)
            self.share_number = post.xpath('//div[@class="_4vn1"]/span[2]/a/text()')
            print(self.share_number)





