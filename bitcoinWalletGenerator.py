#Yes i know the heat death of the universe will happen before i find a wallet with coins, this is just a proof of concept

# This is a script to generate bitcon addresses and their corresponding private keys and add it to a database to later watch the addresses to see if the wallets ever receive any coins

from bitcoinaddress import Wallet
import mysql.connector

timesToRun = 10000
timesLeftToRun = timesToRun


def writeToDB(val1, val2, val3, val4, val5, val6, val7):
	conn = mysql.connector.connect(user='admin', password='password', host='localhost', database='bitcoin')
	if conn.is_connected():
		timesLeftToRun = 10
		with conn.cursor() as cursor:
			sql = "INSERT INTO main (priv_key_wif, priv_key_wif_compressed, pub_addr, pub_addr_compressed, pub_addr_3, pub_addr_bc1, pub_addr_bc1l) VALUES (%s, %s, %s, %s, %s, %s, %s)"
			values = (val1, val2, val3, val4, val5, val6, val7)
			cursor.execute(sql, values)
			conn.commit()

		conn.close()
	
	else:
		print("Couldnt connect to DB")

def newWallet():
	wallet = Wallet()
	wif = wallet.key.__dict__['mainnet'].__dict__['wif']
	wifc = wallet.key.__dict__['mainnet'].__dict__['wifc']
	
	pubKey1 = wallet.address.__dict__['mainnet'].__dict__['pubaddr1']
	pubKey2 = wallet.address.__dict__['mainnet'].__dict__['pubaddr1c']
	pubKey3 = wallet.address.__dict__['mainnet'].__dict__['pubaddr3']

	pubaddrbc1_P2WPKH = wallet.address.__dict__['mainnet'].__dict__['pubaddrbc1_P2WPKH']
	pubaddrbc1_P2WSH = wallet.address.__dict__['mainnet'].__dict__['pubaddrbc1_P2WSH']
	
	writeToDB(wif, wifc, pubKey1, pubKey2, pubKey3, pubaddrbc1_P2WPKH, pubaddrbc1_P2WSH)
	


for i in range(timesToRun):
	newWallet()
	print(timesLeftToRun, " rows left")
	timesLeftToRun -= 1
