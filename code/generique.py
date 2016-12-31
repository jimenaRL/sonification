import os
import time

explanation = [
    'Gender data was collected and processed in order to reveal gender inequalities.',
    'For example, we use the absolute value of the difference of boys and girls scores in educational tests.',
    'The data is then encoding in distinctive elements of a musical piece, such as distorted instruments or random patterns.',
    'Bigger inequalities are then perceived as strongly altered audio.',
    'Data points are presented in the screen as they are used in the musical piece.',
]

os.system('clear')

time.sleep(2)
print '\n'*2
print  ' '*20+'--------------------------'
print  ' '*20+' Gender Data Sonification '
print  ' '*20+'--------------------------'

print '\n'*4
time.sleep(4)
for e in explanation:
    time.sleep(6)
    print ' '*30+e

time.sleep(4)
print '\n'*4
print ' '*30+'Music & Programming:'
print '\n'*2
print ' '*40+' '*10+'Alice  Guerlot-Kourouklis'
print ' '*40+' '*10+'Jimena Royo-Letelier'

time.sleep(4)
print '\n'*4
print ' '*30+'Data source:'
print '\n'*2
print ' '*40+' '*10+'http://www.oecd.org/gender/data/'
print '\n'*2












