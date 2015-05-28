class APILIB():
    def __init__(self):
        return

    def getHireAd(*args,**kwargs):
        type = kwargs['type']
        if type == 'newest':
            return 'newest'
        if type == 'hotest':
            return 'hotest'
        return None

    def getFlashAd(*args,**kwargs):
        pass

    apilib = {
        'getHireAd':getHireAd,
        'getFlashAd':getFlashAd
        }