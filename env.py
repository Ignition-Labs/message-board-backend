import sys
import logging

assert len(sys.argv) == 9, "Args!"
AES_KEY = str(sys.argv[1])
DB_HOST = str(sys.argv[2])
DB_PORT = str(sys.argv[3])
DB_USER = str(sys.argv[4])
DB_NAME = str(sys.argv[5])
DB_PASSWD = str(sys.argv[6])