def encryptedMessage(outgoingData, key):
	encrypted = ''
	for symbol in outgoingData:
        	if symbol.isalpha():
        	    num = ord(symbol)
        	    num += key
        	    if symbol.isupper():
        	        if num > ord('Z'):
        	            num -= 26
        	        elif num < ord('A'):
        	            num += 26
        	    elif symbol.islower():
        	        if num > ord('z'):
        	            num -= 26
        	        elif num < ord('a'):
        	            num += 26
        	    encrypted += chr(num)
        	else:
        	    encrypted += symbol

        return encrypted

def decryptedMessage(incommingData, key):
	key = -key
	decrypted = ''
	for symbol in incommingData:
        	if symbol.isalpha():
        	    num = ord(symbol)
        	    num += key
        	    if symbol.isupper():
        	        if num > ord('Z'):
        	            num -= 26
        	        elif num < ord('A'):
        	            num += 26
        	    elif symbol.islower():
        	        if num > ord('z'):
        	            num -= 26
        	        elif num < ord('a'):
        	            num += 26
        	    decrypted += chr(num)

        	else:
        	    decrypted += symbol

        return decrypted
