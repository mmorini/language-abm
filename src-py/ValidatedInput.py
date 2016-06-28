def valInputFloat(prompt):

    while True:
        try:
            var = float(raw_input(prompt))
            print 'OK'
            return var
        except (ValueError):
            print 'Invalid value, reenter.'
            
def valInputInt(prompt):

    while True:
        try:
            var = int(raw_input(prompt))
            print 'OK'
            return var
        except (ValueError):
            print 'Invalid value, reenter.'
            




