from django.shortcuts import render
from forms import MainForm
from django.http import HttpResponse
import csv


def index(request):
    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES)
        if form.is_valid():
            return createCSV(request.FILES['result_ranks'], request.FILES['website_list'])
    else:
        form = MainForm()

    return render(request, 'index.html', {
        'form': form,
    })


def createCSV(result_ranks, website_list, ):
    websites = []

    lines = website_list.read().splitlines()
    reader = csv.reader(lines)
    i = 0
    for row in reader:
        if i == 0:
            i += 1
            continue
        if not row[0]:
            break
        websites.append(row[0])

    with result_ranks.file as f:
        content = f.read().splitlines()

    p = ""

    first_line = [''] + websites
    first_string = ','.join(first_line)

    p += first_string

    current_line = []
    urls = []

    # counter = 0
    #
    # for elem in content[1:]:
    # if counter == 10:
    #         counter=0
    #     line_content = elem.split(',')
    #     keyword = line_content[0]
    #     website_url = line_content[2]
    #     website_rank = line_content[3]

    keyword_added = True
    for i, elem in enumerate(content):
        if i==0:
            continue

        if keyword_added==True:
            keyword = elem.split(',')[0]
            current_line.append(keyword)
            keyword_added = False
        url = elem.split(',')[2]
        if not url:
            continue
        urls.append(url)
        if i % 10 == 0:
            if i != 0:
                for website in websites:
                    cell = []
                    for rank, indi_link in enumerate(urls):
                        if website in indi_link:
                            tpr = rank + 1
                            cell.append(str(tpr))
                    if not cell:
                        current_line.append("\"0\"")
                    else:
                        cellt = ','.join(cell)
                        current_line.append("\"" + cellt + "\"")
                p += '\n' + ','.join(current_line)
                urls = []
                current_line = []
                keyword_added = True


    #
    # for i,elem in enumerate(content):
    #     if (i)%13 == 0:
    #         if i!=0:
    #             for website in websites:
    #                 cell = []
    #                 for rank,indi_link in enumerate(urls[1:]):
    #                     if website in indi_link:
    #                         tpr = rank+1
    #                         cell.append(str(tpr))
    #                 if not cell:
    #                     current_line.append("\"0\"")
    #                 else:
    #                     cellt = ','.join(cell)
    #                     current_line.append("\""+cellt+"\"")
    #             p+='\n'+','.join(current_line)
    #             urls = []
    #             current_line = []
    #     elif (i-1)%13 == 0:
    #         keyword = elem.split(',')[0]
    #         current_line.append(keyword)
    #     else:
    #         url = elem.split(',')[1]
    #         if not url:
    #             continue
    #         urls.append(elem.split(',')[1])


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    response.write(p)
    return response
