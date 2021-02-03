from bs4 import BeautifulSoup
import requests
import csv

f = open("z.csv", "w")
fieldnames = ['Questions', 'Answer']
writer = csv.DictWriter(f, fieldnames)
writer.writeheader()

html_text = requests.get('https://www.drugs.com/alpha/z.html').text
soup_temp = BeautifulSoup(html_text, 'lxml')
drugs_section = soup_temp.find('ul', class_='ddc-list-column-2')
drugs_list = drugs_section.find_all('li')
for drug in drugs_list:
    drug_url = 'https://www.drugs.com' + drug.a['href']
    drug_html = requests.get(drug_url).text
    soup = BeautifulSoup(drug_html, 'lxml')
    try:
        drug_name = soup.find('div', class_ = 'pronounce-title').h1.text
    except:
        drug_name = ''    
    main_div = soup.find('div', class_ = 'contentBox')
    headings = soup.find_all("h2", class_="ddc-anchor-offset")
    questions = []
    answers = []

    for i in range(0,(len(headings)-1)):
        if drug_name not in headings[i].text:
            question = headings[i].text + ' ' + drug_name
        else:
            question = headings[i].text    
        a = headings[i]
        final_answer = ''
        while(a.next_sibling != headings[i+1]):
            b = repr(a.next_sibling)
            b_soup = BeautifulSoup(b, 'lxml')
            answer = b_soup.strings
            final_ans = [string for string in answer]
            print(final_ans)
            try:
                if str(final_ans[len(final_ans)-1]) == '(more detail)':
                    final_ans = []
            except:
                final_ans = final_ans            
            final_ans = ''.join(final_ans)
            final_ans = final_ans.replace('\n', '')
            final_ans = final_ans.replace('\r', '')
            final_ans = final_ans.replace(r'\n', '')
            final_answer += final_ans.strip()
            a = a.next_sibling
        writer.writerows([
            {'Questions': question, 'Answer': final_answer}
        ])
f.close()