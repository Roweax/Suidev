import oss2
from itertools import islice
from Config import Config

class AliyunOSS:
    def __init__(self):
        self.auth = oss2.Auth(Config.oss_access_key_id, Config.oss_access_key_secret)
        self.service = oss2.Service(self.auth, Config.oss_backet)
        #print([b.name for b in oss2.BucketIterator(service)])


    def List(self, file_path) :
        bucket = oss2.Bucket(self.auth, Config.oss_backet, 'suidev')
        iterator = oss2.ObjectIterator(bucket, prefix=file_path)
        file_list = [];
        for i in iterator: 
            if not i.key.endswith("/") :
                file_list.append(i.key)

        return file_list;

    def Save(self, source, target):
        success = False
        while not success:
            try :
                self.CoreSave(source, target)
            except Exception, e:
                print(e)
            else :
                success = True

    def Load(self, source, target):
        success = False
        while not success:
            try :
                self.CoreLoad(source, target)
            except Exception, e:
                print(e)
            else :
                success = True


    def CoreSave(self, source, target) :
        bucket = oss2.Bucket(self.auth, Config.oss_backet, 'suidev')
        bucket.put_object_from_file(target, source)
        print("Saved OSS file %s"%target)


    def CoreLoad(self, source, target) :
        bucket = oss2.Bucket(self.auth, Config.oss_backet, 'suidev')
        bucket.get_object_to_file(source, target)
        print("Loaded OSS file %s"%target)

        
