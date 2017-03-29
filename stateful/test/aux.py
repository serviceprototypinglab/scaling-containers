import urllib2
import threading
import time
# url1 = 'http://104.198.24.10:30000/documents/search/1/D/lorem'
# print urllib2.urlopen(url1).read()

# conn_cluster = "mongodb://mongo-0.mongo"
# for i in range(1, 2):
#     conn_cluster += ",mongo-" + str(i) + ".mongo"
# conn_cluster += ":27017"
# print conn_cluster


def test_1(url1, res1):
    print "start"
    print url1
    a = urllib2.urlopen(url1).read()
    print a
    print "end"
    print len(res1)
    res1.append(a)


def test_10():
    threads = []
    res = []
    for i in range(0, 10):
        tenant_start = i*100
        tenant_end = tenant_start + 100
        url_aux = 'http://104.154.53.217:30002/test/selects/thread/' + str(tenant_start) + '/' + str(tenant_end) \
                  + '/10/D/3/2/1000/lorem'
        t = threading.Thread(target=test_1, args=(url_aux, res))
        threads.append(t)
    count = 0
    for t in threads:
        print "start_" + str(count)
        count += 1
        t.start()
        time.sleep(0.5)

    if count == len(threads):
        for t in threads:
            print "join_" + str(count)
            count += 1
            t.join()

    print "out join"

    return res


print "-------------------------"

print test_10()

print "-------------------------"
