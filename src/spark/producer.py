import random
import sys
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer


class wordProducer(object):


    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = SimpleProducer(self.client)


    def random_words(self, source_symbol):
       wordlst = ["books","apple", "car","dog","cat","fish"]
       ln_cnt = 0
       wrd_cnt = 0
       #str_fmt ="{};{}"
       #rndword = random.choice(wordlst) + "," + random.choice(wordlst) + "," + random.choice(wordlst)

       while True:
           rndword = random.choice(wordlst) + "," + random.choice(wordlst) + "," + random.choice(wordlst)
           #msg_info = str_fmt.format(source_symbol,rndword)
           msg_info = rndword
           #print msg_info
           #sys.stdout.flush()
           self.producer.send_messages("random_words", source_symbol, msg_info)
           ln_cnt += 1
           wrd_cnt + = ln_cnt*len(rndword)

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    wrd = wordProducer(ip_addr)
    wrd.random_words(partition_key)
