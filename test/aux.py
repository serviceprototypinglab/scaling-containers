import urllib2
import threading
import time
import pymongo
from loremipsum import generate_paragraphs
import random
# url1 = 'http://104.198.24.10:30000/documents/search/1/D/lorem'
# print urllib2.urlopen(url1).read()

# conn_cluster = "mongodb://mongo-0.mongo"
# for i in range(1, 2):
#     conn_cluster += ",mongo-" + str(i) + ".mongo"
# conn_cluster += ":27017"
# print conn_cluster

def get_blob():
    res = ''
    for p in generate_paragraphs(10, False):
        res += p[2]
    return res


def create_aux_json(prefix_name, multi_tenant_option, count, user):
    blob = get_blob()
    name = blob[:5]
    path = '/data/blobs/' + prefix_name + '_' + multi_tenant_option + '_' + str(count) + '_' + name + '.txt'
    number_aux = random.randint(1, 100)
    aux_json = {'title': name,
                'tenant': user,
                'user': user,
                'name': name,
                'tenant_option': multi_tenant_option,
                'other_id': count,
                'path': path,
                'blob': blob,
                'number': number_aux}
    return aux_json

def get_connection(user, option, replica):
    conn_cluster = "mongodb://mongo-0.mongo"
    hosts = []
    for i in range(0, replica):
        a = "mongo-" + str(i) + ".mongo:27017"
        hosts.append(a)
        if i != 0:
            conn_cluster += ",mongo-" + str(i) + ".mongo"
    conn_cluster += ":27017/?replicaSet=rs0"
    try:
        # conn = pymongo.MongoClient(conn_cluster, read_preference=ReadPreference.NEAREST)
        conn_cluster = "35.184.62.148:30010"
        conn = pymongo.MongoClient(conn_cluster)
    except Exception, e:
        a2 = {"mongos": e}
        print e
        conn = None
    return conn


def get_database(conn, option, user):
    if user:
        user = str(user)
    if option == 'A':
        return conn['arkis']
    elif option == 'B':
        return conn['arkis']
    elif option == 'C':
        return conn['arkis']
    elif option == 'E':
        return conn['arkis']
    elif option == 'D':
        return conn['arkis' + str(user)]
    else:
        return conn['arkis']


def get_collection(option, db, user, coll):
    if option == 'B':
        return db[str(coll) + str(user)]
    else:
        return db[str(coll)]

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


def test_insert(tenant_start, tenant_end, docs, option, user, replicas):
    if option == 'D':
        counts = []
        conn = get_connection(user, option, int(replicas))
        for i in range(int(tenant_start), int(tenant_end)):
            print i
            db = get_database(conn, 'D', i)
            coll = get_collection(option, db, i, 'documents')
            for j in range(0, int(docs)):
                json_data = create_aux_json('arkis', option, j, int(i))
                coll.insert_one(json_data)
            coll.create_index([('blob', pymongo.TEXT)])
            counts.append(str(coll.count()))
        conn.close()
        return {"counts": counts}

print "-------------------------"

#print test_10()

print "-------------------------"


test_insert(0, 100, 300, 'D', None, 1)
