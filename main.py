import re
from pprint import pprint
import csv

def read_file():
  with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
  return contacts_list

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
#1
def Add_title(lists: list):
  return lists[0]

def comma_pop(item: str) -> str:
  elem = item.split(',')
  elem = ' '.join(elem)
  if elem[0] == ' ':
    elem = elem[1:]
  if elem[len(elem)-1] == ' ':
    elem = elem[0:len(elem)-1]
  return elem

def phone_number(lists: list) -> list:
  regular = r"(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\-*)(\s*)(\d{3})(\-*)((\d{2})(\-*)(\d{2}))*(\s*)((\(*)((доб.))(\s*)(\d{4})(\)*))*"
  valid_phone = []

  for elem in lists[1:]:
    text = ','.join(elem)
    result = re.search(regular, text)
    if result is None:
      valid_phone.append([])
    else:
      valid_phone.append(result.group(0))
  return valid_phone

def valid_name(lists: list) -> list:
  regular = r"^([А-ё]+)(\s*)(\,?)([А-ё]+)(\s*)(\,?)([А-ё]+)"
  valid_name = []

  for elem in lists[1:]:
    text = ','.join(elem)
    result = re.search(regular, text)
    if result is None:
      valid_name.append([])
    else:
      valid_name.append(comma_pop(result.group(0)))
  return valid_name

def valid_departments(lists: list) -> list:
  regular = r"((\,)([А-ё]{6})(\,))|((\,)([А-яЁ]{3})(\,))"
  valid_depart = []

  for elem in lists[1:]:
    text = ','.join(elem)
    result = re.search(regular, text)
    if result is None:
      valid_depart.append([])
    else:
      valid_depart.append(comma_pop(result.group(0)))

  return valid_depart

def valid_email(lists: list) -> list:
  regular = r"([A-z]+)(\.*)(\@)([a-z]+)(\.)([a-z]+)|(\d+)(\@)([a-z]+)(\.)([a-z]+)"
  valid_email_ = []

  for elem in lists[1:]:
    text = ','.join(elem)
    result = re.search(regular, text)
    if result is None:
      valid_email_.append([])
    else:
      valid_email_.append(result.group(0))
  return valid_email_

def drop_duble(lists: list) -> list:
  res = []
  name = []
  ch = []
  finall = []
  for i in range(len(lists)-1):
    for j in range(i+1, len(lists)):
      lists[i] = list(lists[i])
      lists[j] = list(lists[j])
      if lists[i][0] in lists[j][0]:
        step = lists[i][1:]
        name.append(lists[i][0][1:])
        res.append(lists[j]+step)
        break
      elif lists[i][0] in lists[j][0] and lists[j][0] not in name:
        name.append(lists[j][0])
        res.append(lists[j])
      elif lists[i][0] not in lists[j][0] and lists[j][0] not in name:
        res.append(lists[j])
        name.append(lists[j][0])
  res = sorted(res, reverse=True)
  for elem in res:
    if elem[0][1:] not in ch:
      ch.append(elem[0][1:])
      finall.append(elem)


  return finall

def valid_description(lists: list) -> list:
  valid_descr = []
  for elem in lists[1:]:
    if elem[0][0].istitle() == True:
      valid_descr.append(elem[4])
    else:
      valid_descr.append([])
  return valid_descr



def result_valid(name: list, organiz: list, poz: list, phone: list, email: list):
  with open('phonebook_valid.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['lastname','firstname','surname','organization','position','phone','email'])
    res = []
    result = sorted(list(zip(name, organiz, poz, phone, email)), key=lambda x: x[0])
    result = drop_duble(result)
    for elem in result:
      writer.writerow(elem)

  return result

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
def ch_file():
  with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    contacts_list = read_file()
  return contacts_list

if "__main__" == __name__:
  con = ch_file()

  res = result_valid(name=valid_name(con), organiz=valid_departments(con), poz=valid_description(con), phone=phone_number(con), email=valid_email(con))
  print(res)


