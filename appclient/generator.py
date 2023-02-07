#this is algorithm for generating id

def encrypt(code):
	try:
		str_code = str(code)
		convert_hex = hex(int(str_code))

		left = ['f','g','h','i','j','k','a','b','c','d','e','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		right =['Q','R','S','T','U','V','J','K','L','M','N','O','P','W','X','Y','Z','A','B','C','D','E','F','G','H','I',]
		up =   ['!','@','!','$','%','^','&','*','0','1','2','3','4','5','6','7','8','9','=','+','`','~','<','>','?','/']
		name = 'vtpcollege'
		name1= (name[::-1]).lower()
		myname = ''
		for i in range(len(convert_hex)):
			myname = myname+left[i]+name[i]+right[i]+up[i]+name1[i]+convert_hex[i]
		return myname
	except Exception:
		return "An exception occurred"
	

def decrypt(code):
	try:
		n_name = ''
		x = 5
		while True:
			n_name = n_name + code[x]
			x += 6
			if x >= len(code):
				break
		return int(n_name, 16)
	except Exception:
		error = "An exception occurred"
		return 