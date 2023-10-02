import language_tool_python
import csv

def content_filtration(body):
    points=0
    body_lower=body.lower()
    body_list=body_lower.split(" ")
    f=open("spam_emails.csv","r")
    s=csv.reader(f)
    for j in s:
        count=0
        list=j[0].split(" ")
        list=list[1:]
        if len(body_list)<len(list):
            for i in range (len(body_list)):
                if list[i]==body_list[i]:
                    count+=1
        else:
            for i in range (len(list)):
                if list[i]==body_list[i]:
                    count+=1        
        if count>7 or len(body_list)<7:
            points=5
            break
    f.close()
    error_tool=language_tool_python.LanguageTool("en-US")
    error=error_tool.check(body)
    if (len(body_list)>=25 and len(error)>=8) or (len(body_list)<25 and len(error)>0.25*len(body_list)):
        points+=5
    if points>=5  and count!=len(body_list):
        with open("spam_emails.csv",'a',newline="", encoding='utf-8') as f:
            csvwriter=csv.writer(f)
            column1="Subject: "+body_lower
            row=[column1,'1']
            csvwriter.writerow(row)
    return points

def domain_filtration(id):
    f=open("domains.csv","r")
    domain_list=id.split("@")[1].split(".")
    s=csv.reader(f)
    a,b=0,0
    c,d=0,0
    counter=0
    domain_points=0
    if len(domain_list)<=2 and len(domain_list)>0:
        for j in s:
            if domain_list[0]==j[0][1:]:
                a=1
                c=counter
            if domain_list[1]==j[0][1:]:
                b=1
                d=counter
            counter+=1
        if c!=d:
            if a==1 and b==1:
                domain_points=0
            else:
                domain_points=5
        else:
            domain_points=5
    else:
        domain_points=5
    f.close()
    username=id.split("@")[0]
    username_points=0
    if " " in username or "+" in username or username.count(".")>2:
        username_points=5
    return domain_points+username_points

def header_filtration(header):
    header_lower=header.lower()
    header_list=header_lower.split(" ")
    f=open("headers.csv","r")
    points=0
    s=csv.reader(f)
    for j in s:
        count=0
        list=j[1].split(" ")
        list=list[1:]
        if len(header_list)<len(list):
            for i in range (len(header_list)):
                if list[i]==header_list[i]:
                    count+=1
        else:
            for i in range (len(list)):
                if list[i]==header_list[i]:
                    count+=1      
        if count>=len(header_list)-1:
            points=5
            break
    f.close()
    error_tool=language_tool_python.LanguageTool("en-US")
    error=error_tool.check(header)
    if (len(header_list)>=25 and len(error)>=8) or (len(header_list)<25 and len(error)>0.25*len(header_list)):
        points+=5
    if points>=5  and count!=len(header_list):
        with open("headers.csv",'a',newline="", encoding='utf-8') as f:
            csvwriter=csv.writer(f)
            column2="Subject: "+header_lower
            row=['spam',column2,'1']
            csvwriter.writerow(row)
    return points

def mark_as_spam(header,body):
    with open("spam_emails.csv",'a',newline="", encoding='utf-8') as f:
        csvwriter=csv.writer(f)
        column1="Subject: "+body.lower()
        row=[column1,'1']
        csvwriter.writerow(row)
    with open("headers.csv",'a',newline="", encoding='utf-8') as f1:
        csvwriter=csv.writer(f1)
        column2="Subject: "+header.lower()
        row=['spam',column2,'1']
        csvwriter.writerow(row)
    return "Email marked as spam successfully"

id=input("Enter the email id of the sender for domain filtration: ")
id=id.lower()
header=input("Enter the header of the email for header filtration: ")
body=input("Enter the content of the email for content filtration: ")
print("-------------Checking--------------")
id_points=domain_filtration(id)
header_points=header_filtration(header)
print("-----This might take some time-----")
body_points=content_filtration(body)
if id_points+header_points+body_points>=5:
    print("It is a spam email.")
else:
    print("It is not a spam email")
    if "sale" in id or "lottery" in id or "product" in id or "congrat" in body.lower():
        choice=input("Do you want to classify this email as spam? (Y/N)")
        if choice.lower()=="y":
            choice1=input("All such future emails will be marked as spam. Do you want to continue? (Y/N)")
            if choice1.lower()=="y":
                print(mark_as_spam(header,body))
