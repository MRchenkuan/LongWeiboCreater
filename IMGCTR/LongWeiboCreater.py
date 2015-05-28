#coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import math,base64
import os,sys
from cStringIO import StringIO

class ArticleCreate():
    def __init__(self):
        ##
        # 画布的初始属性定义
        ##
        self.ImageBackgroundColor = (255, 255, 255) # 背景色
        self.ImageMode = "RGBA" # 颜色模式
        self.ImageWidth = 640 # 图片宽度
        self.ImageHeight = 20 # 图片初始高度

        ##
        # 内容的定义
        ##
        self.elem_title=u'无\n'
        self.elem_coname=u'无\n'
        self.elem_cotype=u'无\n'
        self.elem_coindustry=u'无'
        self.elem_location=u'无'
        self.elem_yearcount=u'无'
        self.elem_degree=u'无'
        self.elem_treatment=u'无'
        self.elem_opinfo=u'无\n'
        self.elem_coinfo=u'无'
        self.elem_cosize=u'无'
        self.elem_duty=u'无'
        self.elem_require=u'无'
        self.elem_custname=u'无'
        self.elem_phone=u'无'
        self.elem_email=u'无'
        self.elem_recruiting=u'无'

        ## 内容样式的定义
        self.headheight=10
        self.cutlineheight=5
        self.fontsize = 16 # 字号
        self.lineHeight= 1.25 #行高，倍数
        self.font = ImageFont.truetype('./FONT/造字工房映力黑规体.otf',self.fontsize) # 字体
        self.padding = (20,40,20,30) # 边距，上右下左
        self.style={
            'title':{'fontsize':48,'fontstyle':'/library/fonts/华文黑体.ttf','fontcolor':'black','lineheight':1.25,'fontweight':900},
            'subtitle':{'fontsize':16,'fontstyle':'/library/fonts/华文黑体.ttf','fontcolor':'black','lineheight':1.25,'fontweight':900},
            'cotitle':{'fontsize':24,'fontstyle':'/library/fonts/华文黑体.ttf','fontcolor':'grey','lineheight':1.25,'fontweight':900},
            'subinfo':{'fontsize':16,'fontstyle':'/library/fonts/华文黑体.ttf','fontcolor':'grey','lineheight':1.25,'fontweight':900},
            'textAera':{'fontsize':16,'fontstyle':'/library/fonts/华文黑体.ttf','fontcolor':'black','lineheight':1.25,'fontweight':900},
            'contact':{'fontsize':16,'fontstyle':'/library/fonts/华文黑体.ttf','fontcolor':'grey','lineheight':1.25,'fontweight':900},
            }

        # 全局变量
        self.cursor=Cursor((self.padding[3],self.padding[0]+self.headheight),fontsize=self.fontsize,lineHeight=self.lineHeight)
        self.lineCount=0
        self.wordCount=0
        # self.wordpLine=math.ceil((self.ImageWidth-(self.padding[1]+self.padding[3]))/self.fontsize) #每行字数，
        self.innerWidth=self.ImageWidth-(self.padding[1]+self.padding[3]) #每行字数，

    #预处理内容并计算图片高度
    def prePro(self):
        self.ImageHeight =self.ImageHeight + self.headheight #顶部图片高度 默认300
        self.ImageHeight =self.ImageHeight + self.style['title']['fontsize']*self.style['title']['lineheight']*math.ceil(len(self.elem_title)/(self.innerWidth/float(self.style['title']['fontsize'])))#标题高度
        self.ImageHeight =self.ImageHeight + self.style['cotitle']['fontsize']*self.style['cotitle']['lineheight']*math.ceil(len(self.elem_coname)/(self.innerWidth/float(self.style['cotitle']['fontsize'])))#公司名高度
        self.ImageHeight =self.ImageHeight + self.style['subinfo']['fontsize']*self.style['subinfo']['lineheight']*4 #四行副信息的高度
        # self.ImageHeight =self.ImageHeight + 40*4 #4条分割线的高度 每条默认50
        #职位信息
        self.elem_opinfo = self.elem_opinfo.split('\n') or self.elem_opinfo
        for line in self.elem_opinfo :
            self.ImageHeight =self.ImageHeight + self.style['textAera']['fontsize']*self.style['textAera']['lineheight']*math.ceil(len(line)/(self.innerWidth/float(self.style['textAera']['fontsize'])))#职位信息高度
        #公司信息
        self.elem_coinfo = self.elem_coinfo.split('\n') or self.elem_coinfo
        for line in self.elem_coinfo :
            self.ImageHeight =self.ImageHeight + self.style['textAera']['fontsize']*self.style['textAera']['lineheight']*math.ceil(len(line)/(self.innerWidth/float(self.style['textAera']['fontsize'])))#公司信息高度
        #职责
        self.elem_duty = self.elem_duty.split('\n') or self.elem_duty
        for line in self.elem_duty :
            self.ImageHeight =self.ImageHeight + self.style['textAera']['fontsize']*self.style['textAera']['lineheight']*math.ceil(len(line)/(self.innerWidth/float(self.style['textAera']['fontsize'])))#职责内容高度
        #工作需求
        self.elem_require = self.elem_require.split('\n') or self.elem_require
        for line in self.elem_require :
            self.ImageHeight =self.ImageHeight + self.style['textAera']['fontsize']*self.style['textAera']['lineheight']*math.ceil(len(line)/(self.innerWidth/float(self.style['textAera']['fontsize'])))#工作需求高度

        self.ImageHeight =self.ImageHeight + self.style['contact']['fontsize']*self.style['contact']['lineheight']*3 #三行联系方式的高度
        self.ImageHeight =self.ImageHeight + 10*(self.lineHeight*self.fontsize) #五条分割线的高度

    #文章头尾
    def drawHead(self):

        bottom = Image.open('./img/_bottom.jpg')
        bottomx,bottomy = bottom.size
        # headimg=Image.open('./img/_top.png')
        # headimgx,headimgy=headimg.size

        self.ImageHeight = self.ImageHeight+int(self.ImageWidth*bottomy/bottomx)*2 #整张图片需要增加缩放后的高度
        self.img = Image.new(self.ImageMode,(self.ImageWidth,int(self.ImageHeight)), self.ImageBackgroundColor) # 创建图形
        self.draw = ImageDraw.Draw(self.img) # 创建画笔
        bottom = bottom.resize((self.ImageWidth, int(self.ImageWidth*bottomy/bottomx)), Image.ANTIALIAS)
        # headimg = headimg.resize((self.ImageWidth, int(self.ImageWidth*headimgy/headimgx)), Image.ANTIALIAS)
        #贴上去的图片要严格匹配上左下右，一旦此行报错，则需要去掉最后两个坐标
        # self.img.paste(headimg,(0,0))
        self.draw.line([(0,0),(self.ImageWidth,0)], fill = '#ff2600',width=15)
        self.img.paste(bottom,(0,int(self.ImageHeight-self.ImageWidth*bottomy/bottomx),int(self.ImageWidth),int(self.ImageHeight)))

        self.cursor.moveCursor('return')#不记得此处是否有算一行

    #打印标题/职位
    def drawTitle(self):
        self.cursor.refresh(self.style['title']['fontsize'],self.style['title']['lineheight'])
        for eachword in self.elem_title:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['title']['fontcolor'],font=ImageFont.truetype(self.style['title']['fontstyle'],self.style['title']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.ImageWidth-self.padding[1]:
                self.cursor.moveCursor('return') #换行
        self.cursor.moveCursor('return')

    #打印公司名
    def drawCoTitle(self):
        self.cursor.refresh(self.style['cotitle']['fontsize'],self.style['cotitle']['lineheight'])
        for eachword in self.elem_coname:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['cotitle']['fontcolor'],font=ImageFont.truetype(self.style['cotitle']['fontstyle'],self.style['cotitle']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.ImageWidth-self.padding[1]:
                self.cursor.moveCursor('return') #换行
        self.cursor.moveCursor('return')

    #打印副信息
    def drawSubinfo(self):
        self.cursor.refresh(self.style['subinfo']['fontsize'],self.style['subinfo']['lineheight'])
        #第一行
        self.draw.text((self.cursor.x,self.cursor.y),u'公司性质：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        startingY=self.cursor.y
        endingY=startingY
        for eachword in self.elem_cotype:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+(self.innerWidth/2):
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.y=startingY
        self.cursor.x = self.padding[3]+(self.innerWidth/2) #光标居中
        self.draw.text((self.cursor.x,self.cursor.y),u'公司行业：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        for eachword in self.elem_coindustry:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+self.innerWidth:
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.moveCursor('return')
        self.cursor.y= max(endingY,self.cursor.y) #从最下面开始新增行
        # 第二行
        self.draw.text((self.cursor.x,self.cursor.y),u'工作地点：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        startingY=self.cursor.y
        endingY=startingY
        for eachword in self.elem_location:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subtitle']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+(self.innerWidth/2):
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.y=startingY
        self.cursor.x = self.padding[3]+(self.innerWidth/2) #光标居中
        self.draw.text((self.cursor.x,self.cursor.y),u'公司规模：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        for eachword in self.elem_cosize:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subtitle']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+self.innerWidth:
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.moveCursor('return')
        self.cursor.y= max(endingY,self.cursor.y) #从最下面开始新增行
        #第三行
        self.draw.text((self.cursor.x,self.cursor.y),u'招聘人数：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        startingY=self.cursor.y
        endingY=startingY
        for eachword in self.elem_recruiting:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subtitle']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+(self.innerWidth/2):
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.y=startingY
        self.cursor.x = self.padding[3]+(self.innerWidth/2) #光标居中
        self.draw.text((self.cursor.x,self.cursor.y),u'学历要求：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        for eachword in self.elem_degree:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+self.innerWidth:
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.moveCursor('return')
        self.cursor.y= max(endingY,self.cursor.y) #从最下面开始新增行
        #第三行
        self.draw.text((self.cursor.x,self.cursor.y),u'工资待遇：',fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
        self.cursor.moveCursor(direction='pace',pace=5)#因为小标题固定文字的输出，要进5
        startingY=self.cursor.y
        endingY=startingY
        for eachword in self.elem_treatment:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['subinfo']['fontcolor'],font=ImageFont.truetype(self.style['subinfo']['fontstyle'],self.style['subinfo']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.padding[3]+self.innerWidth:
                self.cursor.moveCursor('return') #换行
                endingY=self.cursor.y
        self.cursor.y=startingY
        self.cursor.moveCursor('return')
        self.cursor.moveCursor('return')
        self.draw.line([(self.cursor.x,self.cursor.y),(self.cursor.x+self.innerWidth,self.cursor.y)], fill = '#ff2600',width=self.cutlineheight)
        self.cursor.moveCursor('return')#板块换行

    #打印岗位信息
    def drawOpinfo(self):
        self.cursor.refresh(self.style['subtitle']['fontsize'],self.style['subtitle']['lineheight'])
        self.draw.text((self.cursor.x,self.cursor.y),u'岗位信息',fill=self.style['subtitle']['fontcolor'],font=ImageFont.truetype(self.style['subtitle']['fontstyle'],self.style['subtitle']['fontsize']))
        self.cursor.moveCursor('return')
        self.cursor.refresh(self.style['textAera']['fontsize'],self.style['textAera']['lineheight'])
        for eachpara in self.elem_opinfo:
            self.cursor.moveCursor('pace',2)
            for eachword in eachpara:
                self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['textAera']['fontcolor'],font=ImageFont.truetype(self.style['textAera']['fontstyle'],self.style['textAera']['fontsize']))
                self.cursor.moveCursor(direction='pace',pace=1) #写字步进
                if self.cursor.x > self.ImageWidth-self.padding[1]:
                    self.cursor.moveCursor('return') #溢出换行
            self.cursor.moveCursor('return')#段落换行
        self.cursor.moveCursor('return')#板块换行
        self.draw.line([(self.cursor.x,self.cursor.y),(self.cursor.x+self.innerWidth,self.cursor.y)], fill = 'Grey',width=1)
        self.cursor.moveCursor('return')#板块换行

    #打印职责
    def drawDuty(self):
        self.cursor.refresh(self.style['subtitle']['fontsize'],self.style['subtitle']['lineheight'])
        self.draw.text((self.cursor.x,self.cursor.y),u'岗位职责：',fill=self.style['subtitle']['fontcolor'],font=ImageFont.truetype(self.style['subtitle']['fontstyle'],self.style['subtitle']['fontsize']))
        self.cursor.moveCursor('return')
        self.cursor.refresh(self.style['textAera']['fontsize'],self.style['textAera']['lineheight'])
        for eachpara in self.elem_duty:
            self.cursor.moveCursor('pace',2)
            for eachword in eachpara:
                self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['textAera']['fontcolor'],font=ImageFont.truetype(self.style['textAera']['fontstyle'],self.style['textAera']['fontsize']))
                self.cursor.moveCursor(direction='pace',pace=1) #写字步进
                if self.cursor.x > self.ImageWidth-self.padding[1]:
                    self.cursor.moveCursor('return') #溢出换行
            self.cursor.moveCursor('return')#段落换行
        self.cursor.moveCursor('return')#板块换行
        self.draw.line([(self.cursor.x,self.cursor.y),(self.cursor.x+self.innerWidth,self.cursor.y)], fill = 'Grey',width=1)
        self.cursor.moveCursor('return')#板块换行

    #打印工作要求
    def drawRequirement(self):
        self.cursor.refresh(self.style['subtitle']['fontsize'],self.style['subtitle']['lineheight'])
        self.draw.text((self.cursor.x,self.cursor.y),u'工作要求：',fill=self.style['subtitle']['fontcolor'],font=ImageFont.truetype(self.style['subtitle']['fontstyle'],self.style['subtitle']['fontsize']))
        self.cursor.moveCursor('return')
        self.cursor.refresh(self.style['textAera']['fontsize'],self.style['textAera']['lineheight'])
        for eachpara in self.elem_require:
            self.cursor.moveCursor('pace',2)
            for eachword in eachpara:
                self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['textAera']['fontcolor'],font=ImageFont.truetype(self.style['textAera']['fontstyle'],self.style['textAera']['fontsize']))
                self.cursor.moveCursor(direction='pace',pace=1) #写字步进
                if self.cursor.x > self.ImageWidth-self.padding[1]:
                    self.cursor.moveCursor('return') #溢出换行
            self.cursor.moveCursor('return')#段落换行
        self.cursor.moveCursor('return')#板块换行
        self.draw.line([(self.cursor.x,self.cursor.y),(self.cursor.x+self.innerWidth,self.cursor.y)], fill = '#ff2600',width=self.cutlineheight)
        self.cursor.moveCursor('return')#板块换行

    #打印公司信息
    def drawCoinfo(self):
        self.cursor.refresh(self.style['subtitle']['fontsize'],self.style['subtitle']['lineheight'])
        self.draw.text((self.cursor.x,self.cursor.y),u'公司信息：',fill=self.style['subtitle']['fontcolor'],font=ImageFont.truetype(self.style['subtitle']['fontstyle'],self.style['subtitle']['fontsize']))
        self.cursor.moveCursor('return')
        self.cursor.refresh(self.style['textAera']['fontsize'],self.style['textAera']['lineheight'])
        for eachpara in self.elem_coinfo:
            self.cursor.moveCursor('pace',2)
            for eachword in eachpara:
                self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['textAera']['fontcolor'],font=ImageFont.truetype(self.style['textAera']['fontstyle'],self.style['textAera']['fontsize']))
                self.cursor.moveCursor(direction='pace',pace=1) #写字步进
                if self.cursor.x > self.ImageWidth-self.padding[1]:
                    self.cursor.moveCursor('return') #溢出换行
            self.cursor.moveCursor('return')#段落换行
        self.cursor.moveCursor('return')#板块换行
        self.draw.line([(self.cursor.x,self.cursor.y),(self.cursor.x+self.innerWidth,self.cursor.y)], fill = '#ff2600',width=self.cutlineheight)
        self.cursor.moveCursor('return')#板块换行

    #打印联系方式
    def drawContact(self):
        self.cursor.refresh(self.style['contact']['fontsize'],self.style['contact']['lineheight'])
        self.draw.text((self.cursor.x,self.cursor.y),u'联系人：',fill=self.style['contact']['fontcolor'],font=ImageFont.truetype(self.style['contact']['fontstyle'],self.style['contact']['fontsize']))
        self.cursor.moveCursor(pace=4)
        for eachword in self.elem_custname:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['contact']['fontcolor'],font=ImageFont.truetype(self.style['contact']['fontstyle'],self.style['contact']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.ImageWidth-self.padding[1]:
                self.cursor.moveCursor('return') #换行
        self.cursor.moveCursor('return')
        self.draw.text((self.cursor.x,self.cursor.y),u'联系电话：',fill=self.style['contact']['fontcolor'],font=ImageFont.truetype(self.style['contact']['fontstyle'],self.style['contact']['fontsize']))
        self.cursor.moveCursor(pace=5)
        for eachword in self.elem_phone:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['contact']['fontcolor'],font=ImageFont.truetype(self.style['contact']['fontstyle'],self.style['contact']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.ImageWidth-self.padding[1]:
                self.cursor.moveCursor('return') #换行
        self.cursor.moveCursor('return')
        self.draw.text((self.cursor.x,self.cursor.y),u'联系邮箱：',fill=self.style['contact']['fontcolor'],font=ImageFont.truetype(self.style['contact']['fontstyle'],self.style['contact']['fontsize']))
        self.cursor.moveCursor(pace=5)
        for eachword in self.elem_email:
            self.draw.text((self.cursor.x,self.cursor.y),eachword,fill=self.style['contact']['fontcolor'],font=ImageFont.truetype(self.style['contact']['fontstyle'],self.style['contact']['fontsize']))
            self.cursor.moveCursor(direction='pace') #写字步进
            if self.cursor.x > self.ImageWidth-self.padding[1]:
                self.cursor.moveCursor('return') #换行

    def imgprint(self):
        self.prePro()
        self.drawHead()
        self.drawTitle()
        self.drawCoTitle()
        self.drawSubinfo()
        self.drawOpinfo()
        self.drawDuty()
        self.drawRequirement()
        self.drawCoinfo()
        self.drawContact()
        fileIO=StringIO()
        self.img.save(fileIO,'jpeg',quality=100)
        self.imgdata=fileIO.getvalue()
        fileIO.close()
        return base64.encodestring(self.imgdata)

#绘图游标@pace 下一个字符；@return 回车换行
class Cursor():
    def __init__(self,pos,fontsize,lineHeight):
        self.x,self.y = pos
        self.fontsize = fontsize
        self.lineHeight = lineHeight

        self.initX = pos[0]
        self.initY = pos[1]

    def refresh(self,fontsize,lineHeight):
        self.fontsize=fontsize
        self.lineHeight=lineHeight


    def moveCursor(self,direction='pace',pace=1):
        if direction=='pace':
            self.x += pace*self.fontsize
            return (self.x,self.y)
        if direction=='return':
            self.y += self.fontsize*self.lineHeight
            self.x = self.initX
            return (self.x,self.y)
        else:
            print 'no CursorOption named %s'%direction
            return (self.x,self.y)


if __name__=='__main__':
    article=ArticleCreate()
    article.prePro()
    article.imgprint()
