##  **Easyxus**

方正教务系统GPA计算、加权平均分计算python脚本
没有接口，代码风格很乱，是两三年前做的东西，本着能用就行的态度
如果有愿意封装或者是部署的非常欢迎，毕竟python是个好东西
然而用的是OCR来识别验证码，所以说速度并没有保证，只能本机用用咯
个人觉得还是挺方便的，同时也推一下友链，学长人很好的
*   [野生工大助手](https://github.com/wangyufeng0615/bjuthelper)

###    Introduction

-   方正教务管理系统访问接口
-   使用了OCR识别验证码，可以实现自动化访问
-   **禁止用作任何非法行为**，使用者**一旦触犯法律，后果自负！**

###    Require Libs

-	Requests        - requesting the website
-	pytesseract     - OCR module 
-	PIL             - turn the image into bi-mode
-	BeautifulSoup4  - to parse the html
-   urllib          - encode the GB2312 code to match the url

```
python -m pip install -r requirements.txt
```