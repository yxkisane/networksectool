from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import hashlib
import random
from pathlib import Path
from secrets import token_bytes
from typing import Tuple

app = Flask(__name__)
CORS(app)

@app.route('/api/XOR', methods=['POST'])
def XOR():
    def random_key(length:int) -> int:
        key:bytes = token_bytes(nbytes=length)
        key_int:int = int.from_bytes(key, 'big')
        return key_int

    # 编码密文
    def encrypt(raw:str) -> Tuple[int, int]:
        raw_bytes:bytes = raw.encode()
        raw_int:int = int.from_bytes(raw_bytes, 'big')
        key_int:int = random_key(len(raw_bytes))
        return raw_int ^ key_int, key_int

    # 解码密文
    def decrypt(encrypted:int, key_int:int) -> str:
        decrypted:int = encrypted ^ key_int
        length = (decrypted.bit_length() + 7) // 8
        decrypted_bytes:bytes = int.to_bytes(decrypted, length, 'big')
        return decrypted_bytes.decode()

    data = request.get_json()
    raw = data['data']
    encrypted, key = encrypt(raw)
    decrypted = decrypt(encrypted, key)
    return jsonify({'encrypted': str(encrypted), 'decrypted': str(decrypted), 'key': str(key)})

@app.route('/api/Caesar', methods=['POST'])
def Caesar():
    data = request.get_json()
    message = data['code']

    def caesar(message):
        message1 = message.upper()  # 把明文字母变成大写
        message1 = list(message1)  # 将明文字符串转换成列表
        list1 = []
        for i in range(len(message1)):
            if message1[i] == ' ':
                list1.append(message1[i])  # 若为空格不用移动
            elif ord(message1[i]) <= 90 - 3 + 1:  # A-X右移三位
                list1.append(chr(ord(message1[i]) + 3))
                result = ''.join(list1)  # 列表转换成字符串
            else:
                list1.append(chr(ord(message1[i]) - (26 - 3)))  # Y和Z回到A、B
                result = ''.join(list1)
        return result

    def decaesar(message):
        message1 = message.upper()  # 把明文字母变成大写
        message1 = list(message1)  # 将明文字符串转换成列表
        list1 = []
        for i in range(len(message1)):
            if message1[i] == ' ':
                list1.append(message1[i])  # 若为空格不用移动
            elif ord(message1[i]) <= 90 - 3 + 1:  # A-X右移三位
                list1.append(chr(ord(message1[i]) - 3))
                result = ''.join(list1)  # 列表转换成字符串
            else:
                list1.append(chr(ord(message1[i]) - (26 - 3)))  # Y和Z回到A、B
                result = ''.join(list1)
        return result

    encode_caesar = caesar(message)
    decaesar_ = decaesar(encode_caesar)
    return jsonify({'encode': str(encode_caesar), 'decode': str(decaesar_)})


@app.route('/api/Hill', methods=['POST'])
def Hill():
    data = request.get_json()
    matrix_data = data['matrix'].split('\n')
    matrix = np.array([list(map(int, row.split(' '))) for row in matrix_data])
    mode = data['mode']

    def judge_inverse_matrix(matrix):
        try:
            np.linalg.inv(matrix)
        except:
            return False
        return True

    if not judge_inverse_matrix(matrix):
        return jsonify({'error': '该矩阵不存在逆矩阵，请重修输入'})

    def generate_inverse_matrix(matrix):
        inverse_matrix = np.linalg.inv(matrix)
        for row in inverse_matrix:
            for num in row:
                num = round(num)
        return inverse_matrix

    def alphabet_number():
        alphabet_number_dict = {}
        for i in range(97, 123):
            alphabet_number_dict[chr(i)] = i % 97
        return alphabet_number_dict

    def encrypt(raw, matrix):
        num_list = []
        dic = alphabet_number()
        for i in raw:
            num_list.append(dic[i])

        row_num = len(matrix)
        supple_num = row_num - (len(num_list) % row_num)
        if len(num_list) % row_num != 0:
            for n in range(1, supple_num + 1):
                num_list.append(25)

        group_num = int(len(num_list) / row_num)
        whole_encrypt_num_list = []
        for g in range(0, group_num):
            plaintext_matrix = np.array(num_list[0 + g * row_num: (g + 1) * row_num])
            encrypt_num_list = np.matmul(plaintext_matrix, matrix)
            for num in encrypt_num_list:
                whole_encrypt_num_list.append(num)
    
        ciphertext = ""
        for ennum in whole_encrypt_num_list:
            if ennum > 25:
                ennum = ennum % 26
            for k in dic:
                if dic[k] == ennum:
                    ciphertext = ciphertext + k
        return ciphertext[:-supple_num]

    def decrypt(raw, matrix):
        num_list2 = []
        dic2 = alphabet_number()
        for i in raw:
            num_list2.append(dic2[i])

        row_num2 = len(matrix)
        supple_num2 = row_num2 - (len(num_list2) % row_num2)

        inserve_matrix = generate_inverse_matrix(matrix)
        group_num2 = int(len(num_list2) / row_num2)
        whole_decrypt_num_list = []
        for g in range(0, group_num2):
            plaintext_matrix = np.array(num_list2[0 + g * row_num2: (g + 1) * row_num2])
            decrypt_num_list = np.matmul(plaintext_matrix, inserve_matrix)
            for num in decrypt_num_list:
                whole_decrypt_num_list.append(num)

        plaintext = ""
        for denum in whole_decrypt_num_list:
            if denum > 25 or denum < -26:
                denum = denum % 26

            if denum < 0:
                denum = denum + 26
            for k in dic2:
                if dic2[k] == denum:
                    plaintext = plaintext + k
        return plaintext

    if mode == 'encode': 
        plaintext = data['plaintext']
        result = encrypt(plaintext, matrix)
    elif mode == 'decode':
        ciphertext = data['ciphertext']
        result = decrypt(ciphertext, matrix)
    else:
        return jsonify({'error': '无效的模式'})

    return jsonify({'result': result})

@app.route('/api/DH', methods=['POST'])
def DH():
    data = request.get_json()
    p = int(data['number'])
    XA = random.randint(0, p - 1)
    XB = random.randint(0, p - 1)

    def isPrime(p):
        if p <= 1:
            return False
        i = 2
        while i * i <= p:
            if p % i == 0:
                return False
            i += 1
        return True

    def get_generator(p):
        a = 2
        list = []
        while a < p:
            flag = 1
            while flag != p:
                if (a ** flag) % p == 1:
                    break
                flag += 1
            if flag == (p - 1):
                list.append(a)
            a += 1
        return list

    def get_calculation(p, a, X):
        Y = (a ** X) % p
        return Y

    def get_key(X, Y, p):
        key = (Y ** X) % p
        return key

    if not isPrime(p):
        return jsonify({'error': '输入的不是素数'})

    list = get_generator(p)
    YA = get_calculation(p, int(list[-1]), XA)
    YB = get_calculation(p, int(list[-1]), XB)
    key_A = get_key(XA, YB, p)
    key_B = get_key(XB, YA, p)

    if key_A == key_B:
        return jsonify({'key': key_A})
    else:
        return jsonify({'error': '密钥不匹配'})

@app.route('/api/RSA', methods=['POST'])
def RSA():
    data = request.get_json()
    msg = int(data['msg'])
    p = int(data['p'])
    q = int(data['q'])
    e = int(data['e'])

    class RSA:
        def is_prime(self, n):
            '''primality test'''
            if n <= 3:
                return n > 1
            elif (n % 2 == 0) or (n % 3 == 0):
                return False
            i = 5
            while i * i <= n:
                if (n % i == 0) or (n % (i + 2) == 0):
                    return False
                i += 6
            return True

        def gcd(self, a, b):
            '''返回a、b的最大公约数'''
            return a if b == 0 else self.gcd(b, a % b)

        def lcm(self, a, b):
            '''返回a、b的最小公倍数'''
            return a // self.gcd(a, b) * b

        def ex_gcd(self, a, b, d, x, y):
            '''
            函数结束时，（x + b) % b为 (a % b)的乘法逆元
            '''
            if b == 0:
                d[0], x[0], y[0] = a, 1, 0
            else:
                self.ex_gcd(b, a % b, d, y, x)
                y[0] -= a // b * x[0]

        def quick_power(self, a, b, mod):
            res = 1
            while b != 0:
                if (b & 1) == 1:
                    res = (res * a) % mod
                a = a * a % mod
                b >>= 1
            return res

        def generate(self, p, q, e):
            '''
            Generates a k-bit RSA public/private pair
            @param 
            @returns 返回密钥对
            '''
            lambdan = self.lcm(p - 1, q - 1)
            d = [0]
            self.ex_gcd(e, lambdan, [0], d, [0])
            d = d[0] % lambdan
            return {
                'n': p * q,  # public key (part I)
                'e': e,  # public key (part II)
                'd': d,  # private key
            }

        def encrypt(self, m, e, n):
            '''
            明文m，指数e，模数n 
            '''
            c = self.quick_power(m, e, n)
            return c

        def dencypt(self, c, d, n):
            m = self.quick_power(c, d, n)
            return m

    alice = RSA()
    keys = alice.generate(p, q, e)

    '''bob使用alice的公钥加秘明文，alice收到密文后使用私钥解密'''
    c = alice.encrypt(m=msg, e=keys['e'], n=keys['n'])
    d = keys['d']
    n = keys['n']

    return jsonify({'c': c, 'd': d, 'n': n})

@app.route('/api/HASH', methods=['POST'])
def HASH():
    def get_file_md5(f):
        m = hashlib.md5()
        while True:
            data = f.read(1024)  #将文件分块读取
            if not data:
                break
            m.update(data)
        return m.hexdigest()

    txt1 = request.json.get('txt1', '')
    txt2 = request.json.get('txt2', '')
    with open('1.txt', 'w', encoding='utf-8') as f1, open('2.txt', 'w', encoding='utf-8') as f2:
        f1.write(txt1)
        f2.write(txt2)

    with open('1.txt', 'rb') as f1, open('2.txt', 'rb') as f2:
        file1_md5 = get_file_md5(f1)
        file2_md5 = get_file_md5(f2)
        if file1_md5 != file2_md5:
            result = '文件已改变'
        else:
            result = '文件未改变'
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True, port=25565)
