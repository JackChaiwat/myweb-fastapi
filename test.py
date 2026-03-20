import easyocr
reader = easyocr.Reader(['th','en'])
result = reader.readtext("pay_slip.jpg")
for r in result:
    print(r[1])

import re
text = " ".join([r[1] for r in result])
amount = re.findall(r"\d+\.\d{2}", text)
print(amount)
