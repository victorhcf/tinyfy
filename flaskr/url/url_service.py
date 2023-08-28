from sqids import Sqids
# GLOBAL_COUNTER_ID = "64ea11192495924af4d39501"
#from flaskr import redis_client


class UrlService:
    '''
        This class is responsible for the main business rule in the application
        Responsible for generating unique short codes for each URL.
        We are using code in the size of 8 chars. This gives us 3.3 trillion unique codes
        In order to generate unique codes in the platform we have a global counter that 
        produces a unique integer input for a hash system that will generate the unique 
        code with length of 8 chars.
    '''
    @staticmethod
    def get_next_counter():
        print('get_next_counter()')
        #counter = Counter.objects.get(pk=GLOBAL_COUNTER_ID)
        #counter = Counter.objects(pk=GLOBAL_COUNTER_ID).update_one(inc__unique_sequential=1)
        #from redis import Redis
        #secret = redis_client.get('unique_sequential')
        #redis = Redis(host='localhost', port=6379)
        from flaskr import redis_client
        secret = redis_client.incr('unique_sequential')
        return secret
        
    @staticmethod
    def generate_code(url):
        url.secret = UrlService.get_next_counter()
        sqids = Sqids(min_length=8)
        url.code = sqids.encode([url.secret])
        return url