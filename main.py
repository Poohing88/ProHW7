import re
import csv


def contact_book():
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    find_name = '(Ус|Ол|Ва|Ма|Ви|Ри|Ге|На|Вя|Лу|Ол|Вл|Па|Вл|Ла|Ив|Ал)([а-я]+)'
    find_number = '(8|\+7)(\ ?)(\(?)(\w{3})(\)?)(\-?)(\ ?)(\w{3})(\-?)(\w{2})(\-?)(\w{2})'
    find_dopnumber = '(доб\.\ [0-9]{4})'
    find_work = 'ФНС|Ми[а-я]+'
    find_email = '[A-Za-z1-9\.]+@[a-z]+\.[a-z]+'
    list_contact = []
    for contact in contacts_list:
        string = ' '.join(contact)
        number = re.findall(find_number, string)
        additional_number = re.findall(find_dopnumber, string)
        name_list = re.findall(find_name, string)
        work = re.findall(find_work, string)
        email = re.findall(find_email, string)
        cont = []
        for name in name_list:
            name = list(name)
            name = ''.join(name)
            if name not in cont:
                cont.append(name)
            else:
                pass
        for place in work:
            work_str = place
            cont.append(work_str)
        counter = 0
        for position in contact:
            counter += 1
            if counter == 5:
                cont.append(position)
        additional = str()
        for add_number in additional_number:
            additional = add_number
        for numb in number:
            numb = list(numb)
            numb = f'+7({numb[3]}){numb[7]}-{numb[9]}-{numb[11]} {additional}'
            cont.append(numb)
        for i in email:
            cont.append(i)
        list_contact.append(cont)
    del(list_contact[0])
    list_contact[3].append(list_contact[1][-1])
    del(list_contact[1])
    list_contact[-2].append(list_contact[-1][-1])
    del(list_contact[-1])

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_contact)


if __name__ == '__main__':
    contact_book()