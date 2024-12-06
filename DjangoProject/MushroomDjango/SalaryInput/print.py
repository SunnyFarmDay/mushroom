import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
def int_to_en(num):
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + '-' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_en(num % 100)

    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' million'
        else: return int_to_en(num // m) + ' million, ' + int_to_en(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_en(num // b) + ' billion'
        else: return int_to_en(num // b) + ' billion, ' + int_to_en(num % b)

    if (num % t == 0): return int_to_en(num // t) + ' trillion'
    else: return int_to_en(num // t) + ' trillion, ' + int_to_en(num % t)


def amount_to_en(num):
    num = str(num).split('.')
    words = (int_to_en(int(num[0])) + ' dollars').capitalize()
    if len(num) == 1:
        return words + ' only'
    dec = num[1]
    if len(dec) == 1:
        dec = dec*10
    dec = int(dec)
    words = words + ' and ' + int_to_en(dec)+ ' cents only'
    return words


pdfmetrics.registerFont(TTFont('TimesNewRoman', 'staticfiles/fonts/MINGLIU.TTC'))
pdfmetrics.registerFont(TTFont('MingLiu', 'staticfiles/fonts/MINGLIU.TTC'))


FORMATTING = {
    'BOC':
    {
        'SIZE_W': 17.1,
        'SIZE_H': 8.9,
        'DATE_DAY': (12.1, 7.3),
        'DATE_MONTH': (14.1, 7.3),
        'DATE_YEAR': (15.6, 7.3),
        'NAME': (1.7, 5.6),
        'AMOUNT_0': (13.3, 4.4),
        'AMOUNT_1': (3.0, 4.4),
        'AMOUNT_2': (1.0, 3.2),
        'AMOUNT_OVERFLOW': 48
    },
    'HSBC':
    {
        'SIZE_W': 15.3,
        'SIZE_H': 8.3,
        'DATE_DAY': (11.6, 6.3),
        'DATE_MONTH': (12.6, 6.3),
        'DATE_YEAR': (13.8, 6.3),
        'NAME': (1.6, 5.5),
        'AMOUNT_0': (11.3, 4.5),
        'AMOUNT_1': (2.4, 4.6),
        'AMOUNT_2': (0.9, 3.8),
        'AMOUNT_OVERFLOW': 37
    },
    'WAGE':
    {
        'SIZE_W': 19.2,
        'SIZE_H': 10.5,
        'DATE_MONTH': (3.6, 9.0),
        'DATE_YEAR': (1.8, 9.0),
        'SID': (14.3, 8.9),
        'NAME': (3.4, 7.6),
        'AMOUNT': (9.4, 4.6),
        'CHEQUE_NUM': (3.5, 2.5),
        'SIGN_HERE': (10.0, 2.5)
    }
}




def print_record(date, data):
    # Create a new PDF file
    filename = "cheque_output.pdf"
    if os.path.exists(filename):
        os.remove(filename)
    c = canvas.Canvas(filename)
    for thisdata in data:
        name = thisdata['name']
        amount = thisdata['amount']



        # Print the recipient's name, date, and dollar amount on the check
        format = FORMATTING[thisdata['layout']]

        # Set the font and font size
        c.setFont('TimesNewRoman', 16)
        c.setPageSize((format['SIZE_W'] * cm, format['SIZE_H'] * cm))

        
        c.drawString(format['DATE_DAY'][0] * cm, format['DATE_DAY'][1] * cm, date['day'])
        c.drawString(format['DATE_MONTH'][0] * cm, format['DATE_MONTH'][1] * cm, date['month'])
        c.drawString(format['DATE_YEAR'][0] * cm, format['DATE_YEAR'][1] * cm, date['year'])
        if (len(name) <= 4):
            c.setFont('MingLiu', 16)
            c.drawString(format['NAME'][0] * cm, format['NAME'][1] * cm, name)
            c.setFont('TimesNewRoman', 16)
        else:
            c.drawString(format['NAME'][0] * cm, format['NAME'][1] * cm, name)

        c.drawString(format['AMOUNT_0'][0] * cm, format['AMOUNT_0'][1] * cm, str(amount))

        
        c.setFont('TimesNewRoman', 10)

        amount_in_word = [amount_to_en(amount), '']
        overflow = format['AMOUNT_OVERFLOW']
        if len(amount_in_word[0]) > overflow :
            stop = 0
            for i in range(overflow, 0, -1):
                if (amount_in_word[0][i]) == ' ':
                    stop = i
                    amount_in_word = [amount_in_word[0][:stop], amount_in_word[0][stop+1:]]
                    break
                elif (amount_in_word[0][i]) == '-':
                    stop = i
                    amount_in_word = [amount_in_word[0][:stop+1], amount_in_word[0][stop+1:]]
                    break

        
            
        c.drawString(format['AMOUNT_1'][0] * cm, format['AMOUNT_1'][1] * cm, amount_in_word[0])
        c.drawString(format['AMOUNT_2'][0] * cm, format['AMOUNT_2'][1] * cm, amount_in_word[1])

        c.showPage()

        format = FORMATTING['WAGE']
        c.setFont('TimesNewRoman', 16)
        c.setPageSize((format['SIZE_W'] * cm, format['SIZE_H'] * cm))
        c.drawString(format['DATE_YEAR'][0] * cm, format['DATE_YEAR'][1] * cm, date['year'])
        c.drawString(format['DATE_MONTH'][0] * cm, format['DATE_MONTH'][1] * cm, date['month'])

        c.drawString(format['SID'][0] * cm, format['SID'][1] * cm, thisdata['SID'])
        
        if (len(name) <= 4):
            c.setFont('MingLiu', 16)
            c.drawString(format['NAME'][0] * cm, format['NAME'][1] * cm, name)
            c.setFont('TimesNewRoman', 16)
        else:
            c.drawString(format['NAME'][0] * cm, format['NAME'][1] * cm, name)
        
        c.setFont('MingLiu', 16)
        c.drawString(format['AMOUNT'][0] * cm, format['AMOUNT'][1] * cm, f"合共: {thisdata['amount']}")
        
        c.drawString(format['CHEQUE_NUM'][0] * cm, format['CHEQUE_NUM'][1] * cm, f"支票號碼 #{thisdata['layout']}-{thisdata['cheque_number']}")

        c.drawString(format['SIGN_HERE'][0] * cm, format['SIGN_HERE'][1] * cm, "簽名:")

        c.showPage()
        
    # Save the PDF file
    c.save()

    return filename
