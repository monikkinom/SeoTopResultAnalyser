from django.shortcuts import render
from forms import MainForm
from django.http import HttpResponse
import csv


def index(request):
    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES)
        if form.is_valid():
            return createCSV(request.FILES['result_ranks'],request.FILES['website_list'])
    else:
        form = MainForm()

    return render(request, 'index.html', {
        'form': form,
    })


def createCSV(result_ranks,website_list,):

    websites = []

    lines = website_list.read().splitlines()
    reader = csv.reader(lines)
    i=0
    for row in reader:
        if i==0:
            i+=1
            continue
        if not row[0]:
            break
        websites.append(row[0])


    with result_ranks.file as f:
        content = f.readlines()

    p=""

    first_line = ['']+websites
    first_string = ','.join(first_line)

    p+=first_string

    current_line = []
    urls = []

    for i,elem in enumerate(content):
        if (i)%13 == 0:
            if i!=0:
                for website in websites:
                    cell = []
                    for rank,indi_link in enumerate(urls[1:]):
                        if website in indi_link:
                            tpr = rank+1
                            cell.append(str(tpr))
                    if not cell:
                        current_line.append("\"0\"")
                    else:
                        cellt = ','.join(cell)
                        current_line.append("\""+cellt+"\"")
                p+='\n'+','.join(current_line)
                urls = []
                current_line = []
        elif (i-1)%13 == 0:
            keyword = elem.split(',')[0]
            current_line.append(keyword)
        else:
            url = elem.split(',')[1]
            if not url:
                continue
            urls.append(elem.split(',')[1])


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    response.write(p)
    return response
