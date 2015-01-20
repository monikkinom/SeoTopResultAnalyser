from django.shortcuts import render
from forms import MainForm
from django.http import HttpResponse


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
    fp = 0
    for line in iter(website_list):
        if fp==0:
            fp+=1
            continue
        url = str(line).replace(",","")
        websites.append(url)

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
                print urls,
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


    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    response.write(p)
    return response
