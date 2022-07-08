
from common_utils import *
from folder_utils import *
from imdb_site import *
from imdb_py import *
from csv_util import *

##### START ######
service_decision = user_decision_for_service()

print_line('Input folder', 'Year', 'Title', 'Output folder', 'Action')
print('-' * (37 * 3 + 14))

headers = ['Input folder', 'Year', 'Title', 'Output folder', 'Action']
rows = []

for folder in folders():
    # remove BRRip/DvdRip from end of name
    raw_name, rip = strip_quality(folder)

    # check if movie is already rated
    if bool(re.search('R-[0-9]', raw_name)):
        title = ''
        year = ''
        action = 'Already Rated'
        print_change(folder, '', '', '', action)
        row = [folder, '', '', '', action]
        rows.append(row)
        continue

    extracted_name = get_name_from_folder(raw_name)
    is_year_present, year_from_folder = get_year_from_folder(raw_name)

    if service_decision == 'a':
        title, year, rating = use_imdb_scrapping(
            extracted_name, is_year_present, year_from_folder)
    elif service_decision == 'b':
        title, year, rating = use_imdbpy(
            extracted_name, is_year_present, year_from_folder)

    rename_to = ''
    action = 'Error'
    if title and year:
        # title = remove_subtitle(title)
        title = replace_colon(title)
        rename_to = title + ' (' + year + ') ' + rating + rip
        if folder == rename_to:
            action = 'Equal'
        elif compare_titles(extracted_name, title):
            if rename(folder, rename_to):
                action = 'Renamed'
            else:
                action = 'Error'
        elif user_decision_for_rename(extracted_name, title):
            if rename(folder, rename_to):
                action = 'Renamed'
            else:
                action = 'Error'
        else:
            action = 'Discarded'
    else:
        title = ''
        year = ''
        action = 'Not found'
    print_change(folder, year, title, rename_to, action)
    row = [folder, year, title, rename_to, action]
    rows.append(row)

write_to_csv(headers, rows)

print('')
os.system('pause')


# ToDo
# 1) Use any directory (take input from user)
# 2) create single file executable
