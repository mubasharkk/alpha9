# -*- coding: utf-8 -*-
import SocketServer
import alpha9
import memory_usage
import sys


#print 'müller'.decode('utf8').encode("ascii")


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        _handlers = {'common': self.common_cmd,
            'search': self.search_cmd}
        data = self.rfile.readline().strip()
        l = data.split()        
        
        
        self.engine = alpha9.SearchEngine();
        
        if len(l) >= 2:
            command, args = l[0], l[1:]
            f = _handlers.get(command, None)
            if f:
                ans = f(*args)
            else:
                ans = 'Invalid command'
        else:
            ans = 'Invalid Usage'
        self.request.sendall(ans + '\r\n')
        
        
    def mem_stats(self, mem_start):
        print 'Memory on Start: ' + str(mem_start) + ' bytes'
        print 'Memory on Completion: ' + str(memory_usage.memory()) + ' bytes'
        print 'Memory Usage: ' + str(memory_usage.memory(mem_start) / memory_usage._scale['MB']) + ' MB'
        
    def common_cmd(self, * args):
        """Add your code here for the common command
        This function should return a string with the
        most n most common words in the books
        """
        mem_start = memory_usage.memory()

        # Default result count
        count = 10
        if args[0]:
            count = int(args[0])
            
        ans = self.engine.getCommonWords(count);
        
        list = []
        for key, value in ans:
            list.append(key)
            
        self.mem_stats(mem_start);
    
        return '\n'.join(list)
    
    def transform_word(self, word):
        table = {
            ord(u'ä'): u'ae',
            ord(u'ö'): u'oe',
            ord(u'ü'): u'ue',
            ord(u'ß'): u'ss',
        }
        print str(word.decode('utf8').translate(table))

    def search_cmd(self, * args):
        """Add your code here for the search command
        Should return a a string with the documents the
        word appears into"""
        
        mem_start = memory_usage.memory()
        
        if args[0] is None:
            return 'Nothing to find!'
        
        """ Needs to transform the UTF8 'keyword' value to ASCII
        to be able to search into the files"""        
#        keyword = self.transform_word(args[0].lower())

        keyword = args[0].lower()
        
        ans = self.engine.searchKeyword(keyword);
                
        list = []
        for key, value in ans:
            list.append(str(key) + ":" + str(value))
            
        if len(args)  > 1:
            list = list[:int(args[1])]
            
        self.mem_stats(mem_start);

        return '\n'.join(list)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

