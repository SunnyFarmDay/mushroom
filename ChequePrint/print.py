import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont

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

def cm(list):
    if type(list) == int or type(list) == float:
        return list*28.35
    else:
        output = []
        for x in list:
            output.append(x*28.35)
        return output

Size = {
    'BOC': [17.1, 8.9],
    'HSBC': [15.9, 8.3],
    'Wage Sheet': [19.2, 10.5]
}
pdfmetrics.registerFont(TTFont('TimesNewRoman', '/home/sunny/mushroom/ChequePrint/times.ttf'))



FORMATTING = {
    'BOC':
    {
        'DATE_DAY': (11.6, 7.1),
        'DATE_MONTH': (13.7, 7.1),
        'DATE_YEAR': (15.6, 7.1),
        'NAME': (1.7, 5.6),
        'AMOUNT_0': (13.3, 4.4),
        'AMOUNT_1': (2.8, 4.4),
        'AMOUNT_2': (0.8, 3.2),
        'AMOUNT_OVERFLOW': 48
    },

}



def print_check(cheque_type, name, date, amount):
    # Create a new PDF file
    filename = "cheque_output.pdf"
    if os.path.exists(filename):
        os.remove(filename)
    c = canvas.Canvas(filename)


    # Set the font and font size
    c.setFont('TimesNewRoman', 12)
    c.setPageSize(cm(Size['BOC']))



    # Print the recipient's name, date, and dollar amount on the check
    format = FORMATTING[cheque_type]

    
    c.drawString(cm(format['DATE_DAY'][0]), cm(format['DATE_DAY'][1]), date['day'])
    c.drawString(cm(format['DATE_MONTH'][0]), cm(format['DATE_MONTH'][1]), date['month'])
    c.drawString(cm(format['DATE_YEAR'][0]), cm(format['DATE_YEAR'][1]), date['year'])

    c.drawString(cm(format['NAME'][0]), cm(format['NAME'][1]), name)

    c.drawString(cm(format['AMOUNT_0'][0]), cm(format['AMOUNT_0'][1]), str(amount))
    amount_in_word = [amount_to_en(amount), ]
    if len(amount_in_word[0]) >= 48:
        stop = 0
        for i in range(48, 0, -1):
            if (amount_in_word[0][i]) == ' ':
                stop = i
                break
        print(stop)

    
        amount_in_word = [amount_in_word[0][:stop], amount_in_word[0][stop+1:]]
    c.drawString(cm(format['AMOUNT_1'][0]), cm(format['AMOUNT_1'][1]), amount_in_word[0])
    c.drawString(cm(format['AMOUNT_2'][0]), cm(format['AMOUNT_2'][1]), amount_in_word[1])

    # Save the PDF file
    c.save()
    return filename

# Example usage
recipient_name = "John Doe"
date = {'day': '7', 'month': '4', 'year': '2023'}
dollar_amount = 9999.99

print_check('BOC', recipient_name, date, dollar_amount)
print(len('Nine thousand, nine hundred and ninety-nine doll'))