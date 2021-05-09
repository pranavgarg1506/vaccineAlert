from django.shortcuts import render
import requests
from django.http import HttpResponse
import datetime
from django.core.mail import send_mail
import pandas as pd
from email.mime.text import MIMEText

from .forms import SearchForm
# Create your views here.

def SearchView(request):
    print('method in SearchView is',request.method)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            pincode = form.cleaned_data['pincode']
            date = form.cleaned_data['date']
            email = form.cleaned_data['email']
            date = datetime.datetime.strftime(date, "%d-%m-%Y")

            url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode='\
                + str(pincode) + '&date=' + date
            
            status_code, records = getResponse(url)
            df = extractImpData(records)

            ## sending mail if information is critical
            imp_df = extractFilteredData(df)

            message ="""\
                <html>
                    <head></head>
                        <body>
                            {0}
                        </body>
                </html>
                """.format(imp_df.to_html())
            if len(imp_df) > 0:
                sendMailUtility(
                    subject = 'ALERT!!!!! at' + str(pincode),
                    html_message = message,
                    from_email = 'your_email_address@gmail.com',
                    To = email
                )


            return HttpResponse(imp_df.to_html())
            #return render(request, 'dashboard/centerList.html', {'df':df})
        else:
            print('form is corrupted')
    else:
        form = SearchForm()
        return render(request, 'dashboard/home.html', {"form":form})


def getResponse(url):
    print("url", url)
    headers = {
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    response = requests.get(url, headers = headers)
    print(response.status_code)
    if response.status_code == 200:
        records = response.json()['sessions']
    
    return response.status_code, records


def extractImpData(records):
    df = pd.DataFrame(records)
    print(df)
    print(type(df))
    ## extraction information from the DataFrame
    columns = ['state_name', 'block_name', 'district_name', 'center_id', 'from', 'to', 'lat', 'long',
                'session_id', 'slots', 'pincode'
            ]
    data_df = df.drop(columns, axis=1)
    print(type(data_df))
    print("data DF",data_df)
    return data_df


def sendMailUtility(subject,html_message,from_email,To):
    print('Sending the mail.....')
    send_mail(
            subject= subject,
            message = 'Importnat Information',
            html_message= html_message,
            from_email=from_email,
            recipient_list=[To],
        )
    print("Mail has been sent Successfuly")


def extractFilteredData(df):

    filter1 = df.available_capacity > 0
    filter2 = df.vaccine == 'COVISHIELD'
    imp_df = df[filter1 & filter2]
    print(imp_df)
    return imp_df

    




