def get_data(inp_year, int_month, inp_day):
    shutil.rmtree('DATA/my_data', ignore_errors=True)
    os.mkdir('DATA/my_data')
    with open('DATA/my_data/C0_data.csv', 'w'):
        pass
    for year in range(22):
        with open(f'DATA/20{str(year).zfill(2)}/20{str(year).zfill(2)}_{str(int_month)}.html', 'r',
                  encoding='utf8') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        # mass_of_temp = []
        with open('DATA/my_data/C0_data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([f'20{str(year).zfill(2)}', f'{str(int_month)}', str(inp_day), str(sum(
                map(lambda x: int(x.text),
                    soup.find_all('tr', align='center')[inp_day - 1].find_all('td', class_='first_in_group'))) / 2)])
