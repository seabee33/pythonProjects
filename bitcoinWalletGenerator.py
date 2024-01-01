#Yes i know the heat death of the universe will happen before i find a wallet with coins, this is just a proof of concept

# This is a script to generate bitcon addresses and their corresponding private keys and add it to a database to later watch the addresses to see if the wallets ever receive any coins

from bitcoinaddress import Wallet
import mysql.connector

timesToRun = 10000


def writeToDB(timesToRun):
	conn = mysql.connector.connect(user='admin', password='password', host='localhost', database='bitcoin')
	if conn.is_connected():
		with conn.cursor() as cursor:
			remainingIterations = timesToRun
			for i in range(timesToRun):
				wallet = Wallet()
				wif = wallet.key.__dict__['mainnet'].__dict__['wif']
				wifc = wallet.key.__dict__['mainnet'].__dict__['wifc']
				
				pubKey1 = wallet.address.__dict__['mainnet'].__dict__['pubaddr1']
				pubKey2 = wallet.address.__dict__['mainnet'].__dict__['pubaddr1c']
				pubKey3 = wallet.address.__dict__['mainnet'].__dict__['pubaddr3']

				pubaddrbc1_P2WPKH = wallet.address.__dict__['mainnet'].__dict__['pubaddrbc1_P2WPKH']
				pubaddrbc1_P2WSH = wallet.address.__dict__['mainnet'].__dict__['pubaddrbc1_P2WSH']

				sql = "INSERT INTO main (priv_key_wif, priv_key_wif_compressed, pub_addr, pub_addr_compressed, pub_addr_3, pub_addr_bc1, pub_addr_bc1l) VALUES (%s, %s, %s, %s, %s, %s, %s)"
				values = (wif, wifc, pubKey1, pubKey2, pubKey3, pubaddrbc1_P2WPKH, pubaddrbc1_P2WSH)
				cursor.execute(sql, values)
				conn.commit()

				print(remainingIterations, "rows left")
				remainingIterations -= 1

		conn.close()

	else:
		print("Couldnt connect to DB")


writeToDB(timesToRun)
