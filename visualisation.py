import csv

files = ['data/daily_sales_data_0.csv', 'data/daily_sales_data_1.csv', 'data/daily_sales_data_2.csv']

for file in files:
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
        print(f"{header[0]} | {header[1]} | {header[2]} | {header[3]} | {header[4]}")

        for row in csv_reader:
            if row[0] == 'pink morsel':
                price = float(row[1].replace('$', '').replace(',', '').strip())
                quantity = int(row[2])
                sales = quantity * price
                date = row[3]
                region = row[4]

                print(f"{sales} | {date} | {region}")
