from retrying import retry
import datetime
@retry()
def make_trouble():
    '''Retry until succeed'''
    print ('retrying...')
    raise
if __name__ == '__main__':
    print(datetime.datetime.now().strftime("%M"))
    #make_trouble()
