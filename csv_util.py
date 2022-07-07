import csv


def write_to_csv(headers, rows):
    with open('renamed_status.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
