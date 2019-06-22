import random
import string
import hashlib
import re
import sys
import getopt
from sys import argv

#main variables
flag = True
iter = 0
firstByte = "00"
stringLength = 10
fileName = "randomfile.txt"


try:
    opts, args = getopt.getopt(argv[1:],"hn:m:f:",["length=","firstbyte=","outputfile="])
except getopt.GetoptError:
    sys.stderr.write('md5p.py -n <length_of_string>  -m <firstByte_of_md5_hash> -f <outputfile>\n')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('md5p.py -n <length_of_string>  -m <firstByte_of_md5_hash> -f <outputfile>')
        sys.exit()
    elif opt in ("-n", "--length"):
        stringLength=arg
    elif opt in ("-m", "--firstbyte"):
        firstByte = arg
    elif opt in ("-f", "--outputfile"):
        fileName = arg



def checkInteger(s):
    try:
        i = int(s)
        if i<1:
            return False
        else:
            return True
    except ValueError:
        return False

def is_hex(s):
     return (re.search("[0-9a-fA-F][0-9a-fA-F]", firstByte)!=None) and (len(s) == 2)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#Проверям валидность данных
if checkInteger(stringLength)==False:
    sys.stderr.write("Введите валидное целочисленное число представлюящую собой длинну случайно генерируемой строки. Не может быть меньше единицы.\n")
    sys.exit(2)
else:
    stringLength = int(stringLength)

if is_hex(firstByte) == False:
    sys.stderr.write("Введите валидную строку представлюящую собой один байт в hexadecimal формате. Например AA или 00.\n")
    sys.exit(2)
else:
    firstByte = firstByte.lower()


#hash collision attack
while flag:
    iter = iter + 1
    str = randomString(stringLength)
    print ("Random String is ", str)
    result = hashlib.md5(str.encode())
    if result.hexdigest()[:2]==firstByte:
        flag = False

print("Всего итераций: ", iter)
print("Строка: " , str ," Длинна строки: ", stringLength)
print("The hexadecimal equivalent of hash is : ", result.hexdigest() )
print("First byte: ", result.hexdigest()[:2] )

#записываем в файл
with open(fileName, "w") as text_file:
    text_file.write(str)
