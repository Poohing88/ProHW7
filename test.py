import re
import csv
from pprint import pprint
import json


def dict_for_list(dict_contact):
    list_contacts = []
    for key in dict_contact:
        contact_list = []
        name = key.split(' ')
        contact_list.append(name[0])
        contact_list.append(name[1])
        contact_list.append(dict_contact[key]['Отчество'])
        contact_list.append(dict_contact[key]['Организация'])
        contact_list.append(dict_contact[key]['Должность'])
        contact_list.append(dict_contact[key]['Номер телефона'])
        contact_list.append(dict_contact[key]['email'])
        list_contacts.append(contact_list)
    return list_contacts


def contact_book():
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    find_name = '([А-Я]+[а-я]*\s[А-Я]+[а-я]*)'
    find_key = '([А-Я]+[а-я]*)'
    find_number = '(8|\+7)(\s?)(\(?)(\w{3})(\)?)(\-?)(\s?)(\w{3})(\-?)(\w{2})(\-?)(\w{2})'
    find_dopnumber = '(доб\.\s[0-9]{4})'
    find_email = '[A-Za-z1-9\.]+@[a-z]+\.[a-z]+'
    dict_contact = {}
    for contact in contacts_list:
        all_string = ' '.join(contact)
        work_dict = {
            'Отчество': '',
            'Должность': '',
            'Номер телефона': '',
            'email': '',
            'Организация': ''
                }
        list_contact = []
        counter = 0
        string = ''
        # telethon = ''
        for i in contact:
            counter += 1
            if counter <= 4:
                list_contact.append(i)
                string = ''.join(list_contact)
            elif counter == 5:
                position = i
                if position:
                    work_dict['Должность'] = position
            elif counter == 6:
                number = re.findall(find_number, i)
                additional_number = re.findall(find_dopnumber, all_string)
                additional = str()
                # telethon = []
                for add_number in additional_number:
                    additional = add_number
                for numb in number:
                    telethon = list(numb)
                    telethon = f'+7({telethon[3]}){telethon[7]}-{telethon[9]}-{telethon[11]} {additional}'
                    if telethon:
                        work_dict['Номер телефона'] = telethon
            else:
                email = re.findall(find_email, i)
                if email:
                    work_dict['email'] = email[0]
        key = re.findall(find_key, string)
        key_dict = re.findall(find_name, string)
        count = 0
        # dict_key = ''
        # father_name = ''
        # work = ''
        for i in key:
            count += 1
            if count == 3:
                father_name = i
                if father_name:
                    work_dict['Отчество'] = father_name
            else:
                work = i
                if work:
                    work_dict['Организация'] = work
        if key_dict:
            dict_key = key_dict[0]
            if dict_key not in dict_contact:
                dict_contact[dict_key] = work_dict
            else:
                if not dict_contact[dict_key]['email']:
                    dict_contact[dict_key]['email'] = work_dict['email']
                if not dict_contact[dict_key]['Должность']:
                    dict_contact[dict_key]['Должность'] = work_dict['Должность']
                if not dict_contact[dict_key]['Номер телефона']:
                    dict_contact[dict_key]['Номер телефона'] = work_dict['Номер телефона']
                if not dict_contact[dict_key]['Организация']:
                    dict_contact[dict_key]['Организация'] = work_dict['Организация']
                if not dict_contact[dict_key]['Отчество']:
                    dict_contact[dict_key]['Отчество'] = work_dict['Отчество']
    list_contacts = dict_for_list(dict_contact)
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_contacts)
    with open('phonebook.json', mode='w', encoding='utf8') as f:
        json.dump(dict_contact, f, ensure_ascii=False, indent=2)
    return dict_contact


contact_book()