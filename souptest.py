from bs4 import BeautifulSoup


data = open("test.txt", 'r')
orig = data.read()
data.close()

soup = BeautifulSoup(orig)
text = soup.get_text()

print text
#temp = open("test2.txt",'w')
#temp.write(text)
#temp.close()

