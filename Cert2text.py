import M2Crypto
# all_files = list of SSL certificate files 
all_files = open("all.txt","r").readlines()
all_path=[]
for i in all_files:
	all_path.append(i.strip())
for i in all_path:
	crt = open(i,"r").read().strip()
	if "NULL" not in crt:
		m2cert = M2Crypto.X509.load_cert_string(crt)
		v = open(i+".txt","w")
		v.write(m2cert.as_text())
		v.close()
