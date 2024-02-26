import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json
from eth_abi import decode
import secrets
import psycopg2
import sqlite3
import os
import requests
import string
import random

def generate_random_key():
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace

    # 隨機選擇字符來構建文本
    random_text = ''.join(random.choice(characters) for _ in range(16))
    print("random_text",random_text)

    return random_text  # 32字節的隨機金鑰

def generate_random_iv():
    return os.urandom(16)  # 16字節的隨機初始化向量

def encrypt(research_data):
  # Create a SHA256 hash of the research_data
  hash_object = hashlib.sha256()
  
  # Set encryption key and initialization vector
  # encryption_key = 'mysecretpassword'
  # encryption_key = generate_random_key()

  encryption_key = generate_random_key()
  file_path = os.path.join('/home','node1','BlockChain','password.txt')
  with open(file_path, 'w') as file:
      file.write(encryption_key)
  # iv = b'initialvector123'
  iv = generate_random_iv()

  # Create the AES-GCM cipher
  cipher = AES.new(encryption_key.encode(), AES.MODE_GCM, iv)
  
  research_data = str(research_data)
  hash_object.update(research_data.encode())
  hash_value = hash_object.digest()
  
  # Encrypt the hash with the cipher
  cipher_text, tag = cipher.encrypt_and_digest(research_data.encode())
  
  # Concatenate the iv, cipher text, and tag
  encrypted_data = iv + cipher_text + tag + hash_value

  # Encode the encrypted data using base64
  base64_data = base64.b64encode(encrypted_data)
  
  return base64_data


def write_data_to_contract(base64_data):
  # print("@write_data_to_contract, beginning")

  # Connect to the web3 provider and middleware
  web3_http = Web3(HTTPProvider('http://127.0.0.1:5002'))
  web3_http.middleware_onion.inject(geth_poa_middleware, layer=0)

  private_key = secrets.token_bytes(32)

  # Set account address and contract address
  # myAccount = '0x280bA7e0730F73Ae31604698211aA493CC485eE6'
  myAccount = '0xb04ACED9EBe5C1a53f3482065500717aFa199058'
  #contractAddress = '0x7b2A0D4Ac83bb00b48f82ef25DE19f1edd33A7e2'
  # contractAddress = '0x9C2Cc6d46780A37511eeF963be26D514aEA1F590'
  contractAddress = '0xd4cf925386a41Fcf096Fe03C59cA2cc67512AdFf'

  # Load the contract ABI from myAbi.json
  # with open('myAbi.json', 'r') as f:

  abi = [{'inputs': [], 'name': 'read', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': '_str', 'type': 'string'}], 'name': 'write', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}]

  # with open('upload_abi.json', 'r') as f:
  # abi = json.load(upload_abi)
  # print("abi",abi)
  # Load the contract using the ABI and the contract address
  contract = web3_http.eth.contract(address=web3_http.to_checksum_address(contractAddress), abi=abi)
  print("contract123",contract)
  # Write the encrypted data to the contract
  tx_hash = contract.functions.write(base64_data.decode()).transact({'from': myAccount})
  print("tx_hash",tx_hash)
  # print("@write_data_to_contract, tx_hash: ", tx_hash)
  # Wait for the transaction to be mined
  receipt = web3_http.eth.wait_for_transaction_receipt(tx_hash)
  print("receipt",receipt)
  # 寫入檔案開始
  # 获取交易收据对象的所有字段
  receipt_fields = vars(receipt)

  # 指定要写入的文件名
  file_name = '研究紀錄上傳區塊鏈紀錄.txt'
  # print("要写入的文件名: ", file_name)

  # 打开文件以进行写入
  with open(file_name, 'w') as file:
      # 遍历所有字段并将其写入文件
      # print("遍历所有字段并将其写入文件")
      for field, value in receipt_fields.items():
        file.write(f'{field}: {value}\n')
      # print("交易收据已写入文件: ", file_name)  
  # 寫入檔案結束
  
  try:
    print("this function in try")
    # Convert HexBytes data to a string before insertion
    hex_bytes_text = tx_hash.hex()
    # print("convert", hex_bytes_text)

    # Connect to the database
    db_path = '/home/node1/BlockChain/serch.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert the HexBytes data as text
    # cursor.execute("INSERT INTO upload_record (transaction_hash) VALUES (?)", (hex_bytes_text,)) DW_2023_9_10_10_19
    cursor.execute("INSERT INTO upload_record (transaction_hash, current_date) VALUES (?, datetime('now', 'localtime'))", (hex_bytes_text,))
    conn.commit()

  except sqlite3.Error as e:
    # 打開一個文件以進行寫入，如果文件不存在，則會自動創建
    with open('dailyUpload.log', 'w') as file:
        # Handle any errors that occur during the database operations
        file.write("Error:", e)
    # 文件在離開"with"區塊後自動關閉
  
  finally:
      # Close the database connection
      if conn:
          conn.close()
  
  return tx_hash
  
def read_data_from_sqlite():
    try:
        # Connect to the database
        conn = sqlite3.connect('serch.db')
        cursor = conn.cursor()

        # Execute the query to retrieve data
        # cursor.execute("SELECT transaction_hash, current_date FROM upload_record ORDER BY current_date DESC") DW_2023_9_10_10_18
        # cursor.execute("SELECT upload_time, '《' || transaction_hash || '》'  FROM upload_record ORDER BY upload_time DESC") 
        cursor.execute("SELECT current_date, transaction_hash FROM upload_record ORDER BY current_date DESC") 

        # Fetch all results
        results = cursor.fetchall()
        print("results",results)
        return results


    except sqlite3.Error as e:
        # 打开文件以进行写入
        with open(file_name, 'w') as file:
            # 遍历所有字段并将其写入文件
            # print("遍历所有字段并将其写入文件")
            # Handle any errors that occur during the database operation
            file.write("Error:", e)
        # print("交易收据已写入文件: ", file_name)  
        # 寫入檔案結束

        return None  # Return None to indicate an error

    finally:
        # Close the database connection
        if conn:
            conn.close()

def read_data_from_contract(tx_hash):
  # connect to a local Ethereum node
  web3 = Web3(HTTPProvider('http://127.0.0.1:5002'))
  
  # load the ABI file for the contract that generated the transaction
  # with open('myAbi.json', 'r') as f:
  with open('upload_abi.json', 'r') as f:
      abi = json.load(f)

  # create a Contract object using the ABI and the contract address
  # contract_address = web3.to_checksum_address('0x7b2A0D4Ac83bb00b48f82ef25DE19f1edd33A7e2')
  # contract_address = web3.to_checksum_address('0x9C2Cc6d46780A37511eeF963be26D514aEA1F590')
  contract_address = web3.to_checksum_address('0xd4cf925386a41Fcf096Fe03C59cA2cc67512AdFf')
  contract = web3.eth.contract(address=contract_address, abi=abi)

  # get the transaction object
  tx = web3.eth.get_transaction(tx_hash)
  # decode the input data of the transaction using the Contract object
  fn_name, args = contract.decode_function_input(tx.input)  
  
  return args['_str']
    

def decrypt(encrypted_data):
  # encryption_key = 'mysecretpassword'
  
  
  # Decode the base64-encoded input string
  decoded_data = base64.b64decode(encrypted_data)
  
  
  # Extract the iv, cipher text, and tag from the decoded input data
  iv1 = decoded_data[:16]
  cipher_text1 = decoded_data[16:-16]
  tag1 = decoded_data[-16:]
 
  # Create the AES-GCM cipher using the encryption key and iv
  encode_enc_key=encryption_key.encode()
  cipher = AES.new(encode_enc_key, AES.MODE_GCM, iv1)
  
  # Try to decrypt the cipher text using the cipher and tag
  try:
      decrypted_data = cipher.decrypt_and_verify(cipher_text1, tag1).decode()
      
      return decrypted_data
  except ValueError:
      # 打开文件以进行写入
      with open(file_name, 'w') as file:
          print("Decryption unsuccessful: Incorrect tag or padding")
      # 寫入檔案結束
      
