def get_html():
    for i in range(0, 22):
        shutil.rmtree(f'20{str(i).zfill(2)}', ignore_errors=True)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1488 Yowser/2.5 Safari/537.36'}
    for year in range(22):
        os.mkdir(f'DATA/20{str(year).zfill(2)}')
        for month in range(1, 13):
            data = requests.get(f'https://www.gismeteo.ru/diary/4368/20{str(year).zfill(2)}/{str(month)}/',
                                headers=headers)
            with open(f'DATA/20{str(year).zfill(2)}/20{str(year).zfill(2)}_{str(month)}.html', 'w',
                      encoding='utf8') as f:
                f.write(data.text)
