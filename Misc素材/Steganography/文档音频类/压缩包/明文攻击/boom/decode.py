#'491e18fd8378590ce3fb93f484a18495'=key_*******?_wakaka
#int *******
#char ?
import hashlib

str_src=list('key_*******?_wakaka')
str_md5='491e18fd8378590ce3fb93f484a18495'
str1_list=list('abcdefghijklmnopqrstuvwxyz')
str2_list = list('0123456789')
for a in range(len(str2_list)):
    str_src[4]=str2_list[a]
    for b in range(len(str2_list)):
		str_src[5]=str2_list[b]
		for c in range(len(str2_list)):
			str_src[6]=str2_list[c]
			for d in range(len(str2_list)):
				str_src[7]=str2_list[d]
				for e in range(len(str2_list)):
					str_src[8]=str2_list[e]
					for f in range(len(str2_list)):
						str_src[9]=str2_list[f]
						for g in range(len(str2_list)):
							str_src[10]=str2_list[g]
							for h in range(len(str1_list)):
								str_src[11]=str1_list[h]
								stry_md5=str(hashlib.md5(''.join(str_src)).hexdigest())
								if stry_md5 == str_md5:
									print ''.join(str_src),stry_md5














































































																														

