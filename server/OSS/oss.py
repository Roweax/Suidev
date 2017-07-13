import oss2
from Config import Config

class AliyunOSS:
    def __init__(self):
        self.auth = oss2.Auth(Config.oss_access_key_id, Config.oss_access_key_secret)
        self.service = oss2.Service(self.auth, Config.oss_backet)

        #print([b.name for b in oss2.BucketIterator(service)])
    def Save(self, source, target):
        bucket = oss2.Bucket(self.auth, Config.oss_backet, 'suidev')
        bucket.put_object_from_file(target, source)
        print("Saved OSS file %s"%target)
        
