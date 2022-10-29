
from flask import Flask,render_template,request
from bs4 import BeautifulSoup as but
from urllib.request import urlopen as uropen
import requests



app=Flask(__name__)
@app.route("/",methods=["GET"])
def tag_1():
         return render_template("indexflip.html")


@app.route('/review',methods=["GET","POST"])
def new_line():
    if request.method=="POST":
        try:
            searchString=request.form['content'].replace(" ","")
            print(searchString)
            Tv_Url="https://www.flipkart.com/search?q="+searchString
            scrap_amezon = uropen(Tv_Url)
            scrap_detail = scrap_amezon.read()
            scrap_amezon.close()
            scrap_buti = but(scrap_detail, "html.parser")
            # print(scrap_buti)
            scrap_2 = scrap_buti.find_all("div", {"class": "_1AtVbE col-12-12"})
            del scrap_2[0:2]
            tv_product_link= "https://www.flipkart.com" +scrap_2[0].div.div.div.a["href"]
            all_1=but(tv_product_link, "html.parser")
            All_2 = requests.get(all_1)
            All_2.encoding="utf-8"
            All_tv = but(All_2.text, "html.parser")
            Tv_review = All_tv. find_all("div", {"class": "_16PBlm"})

            # filename=searchString+".csv"
            # file=open(filename,"w")
            # headers="product,user_name,rating,price,comment,h_comment"
            # file.write(headers)

            reviews=[]

            for comment_all in  Tv_review:
                try:
                    name = comment_all.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name=" name is not avilable for this product"
                try:
                    price = All_tv.find_all('div', {'class': '_30jeq3 _16Jk6d'})[0].text
                except:
                    price= " price is not avilable on this product"
                try:
                    rating=comment_all.div.div.div.div.text
                except:
                    rating= " rating is not avilable for this product"
                try:
                    comment=comment_all.div.div.find_all("div",{"class":"t-ZTKy"})
                    comments=comment[0].div.div.text
                except:
                    comments = " comments is not avilable for this product"
                try:
                    header_1=comment_all.div.div.div.p.string
                except:
                    header_1=" headers is not available for this product"

                dict_1={"product":searchString,"user_name":name,"rating":rating,"price":price,"h_comment":header_1,"comment":comments
                }
                reviews.append(dict_1)

            return render_template("resultflip.html", review=reviews[0:(len(reviews)-1)] )
        except:
            return "something went wrong"
    else:
        return render_template("indexflip.html")

if __name__=="__main__":

   app.run(debug=True)


