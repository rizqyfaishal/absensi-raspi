
csv = open('data_univ_id.csv')
wr = open('s.sh', 'w')
data = csv.readlines()

count = 0
for row in data:
	if count > 0:
		wr.write('curl http://159.89.200.51/schedule.json -d project=forlapdikti -d spider=forlap_daftar_dosen -d univ_id=' + row + '\n')
	count = count + 1

csv.close()
wr.close()