import urllib2
import threading
import time
import pymongo
from loremipsum import generate_paragraphs
import random
import json


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
        conn_cluster = "35.184.62.148:30012"
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
        tenant_start = i * 100
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


# test_insert(50, 100, 300, 'D', None, 1)


def get_url(url_aux, res):
    res.append(urllib2.urlopen(url_aux).read())


def test_4():
    url1 = 'http://35.184.62.148:30002/test/selects/0/25/100/D/1/10/100/lorem'
    url2 = 'http://35.184.62.148:30002/test/selects/25/50/100/D/1/10/100/lorem'
    url3 = 'http://35.184.62.148:30002/test/selects/50/75/100/D/1/10/100/lorem'
    url4 = 'http://35.184.62.148:30002/test/selects/75/100/100/D/1/10/100/lorem'

    urls = [url1, url2, url3, url4]
    threads = []
    res = []
    for url_aux in urls:
        t = threading.Thread(target=get_url, args=(url_aux, res))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    count = 0
    for r in res:
        d = json.loads(r)
        count += d['times'][-1]

    return count/4

print "-------------------------"

total = []
for i in range(0, 20):
    #a = test_4()
    a = 0
    total.append(a)
    #print i
    #print a
    #time.sleep(2)

#print total

print "-------------------------"


def average(aux):
    count = 0
    aux1 = 0
    for i in aux:
        count += i
        aux1 += 1
        if aux1 == 2:
            aux1 = 0
            print count / 2
            count = 0
    return count / len(aux)
array_aux = [
    12.883332014083862,
    13.00239086151123,
    13.655519962310791,
    12.466742992401123,
    12.406434774398804,
    13.834571123123169,
    12.100023031234741,
    11.370167016983032,
    10.380200862884521,
    11.84969687461853,
    12.417817115783691,
    11.903677940368652
]
# average(array_aux)


def get_number_database(replica1, tenant_max1, tenant1):
    number_db1 = -1
    for k in range(0, int(replica1)):
        a1 = (k * int(tenant_max1)) / int(replica1)
        b1 = ((k + 1) * int(tenant_max1)) / int(replica1)
        if tenant1 in range(a1, b1):
            number_db1 = k
    return str(number_db1)


# replica1 = '2'
# tenant_max1 = '100'

#for i in range(75, 100):
#    print get_number_database(replica1, tenant_max1, i)


array_1 = [102.15372800827026, 102.91774952411652, 66.00887221097946, 66.58866518735886, 101.33616900444031, 96.45809072256088, 103.69434177875519, 105.1175382733345, 109.05331528186798, 101.1356914639473, 66.50162398815155, 69.32788419723511, 101.93354624509811, 94.92327105998993, 49.4791305065155, 70.02328723669052, 100.41839575767517, 103.32437199354172, 105.75467419624329, 67.1945281624794]
array_3 = [39.60379981994629, 54.98904997110367, 34.55446094274521, 51.6783812046051, 51.61707329750061, 53.16869682073593, 40.41672742366791, 41.91641443967819, 55.14009255170822, 40.476675271987915, 42.91166293621063, 42.25400447845459, 42.03682678937912, 40.44764560461044, 52.79879504442215, 39.95301675796509, 40.920283794403076, 51.482463002204895, 41.0498029589653, 53.221657276153564]
array_5 = [36.347118973731995, 45.63705575466156, 41.789939165115356, 46.54701393842697, 37.32527631521225, 34.29882496595383, 38.04883474111557, 51.49988454580307, 45.51875078678131, 38.12603259086609, 38.23519974946976, 49.99293142557144, 39.52346521615982, 53.349632263183594, 51.89443999528885, 54.91470628976822, 49.84267175197601, 32.94516295194626, 42.65397256612778, 47.31831103563309]
array_7 = [48.98005950450897, 34.80353718996048, 39.02452528476715, 49.55244982242584, 49.482337474823, 33.492006957530975, 37.74290931224823, 47.80361807346344, 36.692909717559814, 43.422518730163574, 37.242725014686584, 35.83348399400711, 44.51454436779022, 43.8009050488472, 40.0276717543602, 47.636477530002594, 40.55967116355896, 49.32526385784149, 38.91680830717087, 38.809686958789825]
array_9 = [36.71016311645508, 48.455532252788544, 47.448515713214874, 47.068307518959045, 48.975303053855896, 37.67252516746521, 43.68073433637619, 45.90700823068619, 35.454561710357666, 31.191612482070923, 36.652015209198, 44.03967094421387, 35.20111274719238, 43.758993208408356, 45.34801948070526, 44.9112189412117, 37.76628267765045, 33.65753251314163, 47.04243952035904, 50.07303148508072]
array_11 = [49.34795743227005, 37.13432973623276, 37.671592235565186, 43.82886302471161, 45.43622648715973, 45.358451783657074, 37.631931245326996, 37.47312581539154, 43.56478172540665, 43.519086956977844, 34.9056134223938, 42.75364279747009, 44.35640376806259, 35.862518191337585, 35.699737668037415, 36.56950896978378, 44.646196126937866, 44.6958794593811, 36.36375147104263, 32.158917009830475]

#array_1 = [85.88882946968079, 60.19962501525879, 57.776523768901825, 45.71059602499008, 60.51870000362396, 44.06839233636856, 88.17350697517395, 55.661609053611755, 56.896120965480804, 57.41839677095413, 86.8252580165863, 57.99726277589798, 88.26190948486328, 88.41167002916336, 57.65348041057587, 88.72080606222153, 89.25412100553513, 56.3027982711792, 86.59606170654297, 90.95850276947021, 89.156434237957, 61.59624207019806, 119.54049998521805, 90.12099194526672, 39.558609783649445, 90.29724526405334, 59.831831991672516, 92.47132498025894, 59.109006524086, 61.59549343585968, 97.79373401403427, 96.03218072652817, 60.96557241678238, 61.40053403377533, 61.054949939250946, 86.76825648546219, 59.93363827466965, 88.12760698795319, 60.38487005233765, 88.74005597829819, 58.0229514837265, 59.07639122009277, 86.9239975810051, 57.70862191915512, 57.930763244628906, 85.57016730308533, 56.447540283203125, 57.22526174783707, 56.46382665634155, 91.70191895961761, 91.28605431318283, 83.33145731687546, 61.356404185295105, 91.8106763958931, 63.02370822429657, 95.36253023147583, 91.64799571037292, 63.88240307569504, 61.67236524820328, 61.772271275520325, 60.32924348115921, 92.74684804677963, 92.22812974452972, 93.00098705291748, 63.19939750432968, 49.18063950538635, 94.94590699672699, 94.99184226989746, 62.456608176231384, 89.70782351493835, 93.77161145210266, 90.0748839378357, 59.603945195674896, 94.52382725477219, 63.84709393978119, 48.207448065280914, 98.11914402246475, 61.73067682981491, 48.944686591625214, 39.162271440029144, 59.19102507829666, 59.82235699892044, 86.9736835360527, 59.573485255241394, 88.2960079908371, 47.59750485420227, 30.81118279695511, 57.90204793214798, 57.904603481292725, 58.449951231479645, 71.95989042520523, 62.69485902786255, 96.56918966770172, 62.9812912940979, 93.07037371397018, 60.24299216270447, 93.17080694437027, 59.8114692568779, 61.81933444738388, 50.326679050922394]
#array_3 = [54.15760999917984, 44.00885081291199, 43.27223718166351, 42.44336646795273, 58.0515713095665, 43.938934683799744, 45.13986998796463, 57.77275449037552, 47.598250448703766, 45.527646005153656, 53.93853169679642, 54.61852329969406, 34.29718774557114, 42.84283173084259, 53.18711298704147, 54.86210948228836, 43.514974653720856, 55.29099017381668, 42.69734454154968, 43.82157075405121, 41.3281232714653, 45.50312775373459, 58.96451151371002, 55.38988423347473, 52.12595075368881, 56.24729698896408, 56.88093703985214, 42.663110852241516, 53.97117060422897, 42.51482003927231, 55.241972506046295, 53.9595822095871, 60.69012826681137, 57.12484794855118, 60.11887449026108, 44.554346680641174, 54.69048500061035, 42.77042144536972, 55.872290194034576, 41.64425766468048, 42.47366225719452, 58.59762740135193, 42.06734323501587, 45.58279222249985, 44.59841471910477, 42.389098048210144, 55.89468175172806, 42.94187378883362, 56.34219425916672, 54.417109072208405, 44.60336285829544, 42.086806774139404, 57.18942868709564, 46.55669057369232, 43.017946660518646, 41.731919050216675, 44.930506467819214, 55.17815524339676, 42.9409185051918, 53.66359156370163, 38.62673717737198, 53.052875995635986, 33.85369324684143, 55.65179491043091, 54.329469323158264, 40.99675250053406, 42.50801545381546, 54.02140522003174, 54.98190802335739, 55.131142258644104, 39.448656260967255, 44.907636761665344, 57.14677274227142, 46.007204711437225, 35.053348541259766, 39.501079976558685, 39.69558125734329, 50.560808300971985, 40.174002051353455, 54.594351053237915, 53.750940918922424, 55.8685462474823, 36.38118493556976, 53.69787776470184, 52.60556226968765, 39.7807337641716, 38.50509798526764, 52.113871335983276, 52.06048929691315, 41.14173012971878, 38.7908952832222, 40.56919324398041, 60.17403268814087, 40.84804731607437, 39.14775723218918, 39.78291267156601, 52.84528797864914, 40.364080250263214, 51.46972191333771, 50.643509805202484]
#array_5 = [42.705968499183655, 44.35145777463913, 47.57757079601288, 36.40841722488403, 34.596025466918945, 44.53066968917847, 44.65918904542923, 44.29424875974655, 45.18775075674057, 29.636745750904083, 33.51935803890228, 34.72343593835831, 44.277914345264435, 35.64161628484726, 35.92888468503952, 44.4164457321167, 43.99824595451355, 36.0804483294487, 36.153524518013, 42.78504580259323]
#array_7 = [40.38057625293732, 42.99327725172043, 43.9639750123024, 39.65859705209732, 34.9242781996727, 33.87644302845001, 28.534021973609924, 33.403913259506226, 41.0175017118454, 39.22861850261688, 34.582730531692505, 33.73218822479248, 32.585772812366486, 31.281027853488922, 34.090036511421204, 32.56112778186798, 38.49561369419098, 33.314079225063324, 37.41931802034378, 32.26621222496033]
#array_9 = [32.930805802345276, 38.28164106607437, 32.256771087646484, 29.414470613002777, 32.65046948194504, 38.60061049461365, 32.775099992752075, 37.64577054977417, 32.91072177886963, 31.80351811647415, 31.33476024866104, 37.92484772205353, 39.49885529279709, 33.62131977081299, 38.82429826259613, 41.59911268949509, 39.687918305397034, 32.49359601736069, 44.27207100391388, 42.37888216972351]
#array_11 = [37.751176714897156, 34.95412027835846, 40.562461733818054, 31.221032977104187, 30.342949748039246, 33.953069508075714, 39.21348565816879, 32.382420778274536, 41.62026005983353, 39.774462938308716, 33.810929000377655, 36.79510223865509, 35.087788224220276, 34.12022548913956, 35.582268834114075, 34.303137719631195, 33.09962898492813, 41.028846740722656, 40.391187965869904, 41.095329999923706]

count = 0
for i in array_1:
    count += i

print count/len(array_1)

count = 0
for i in array_3:
    count += i

print count/len(array_3)

count = 0
for i in array_5:
    count += i

print count/len(array_5)

count = 0
for i in array_7:
    count += i

print count/len(array_7)

count = 0
for i in array_9:
    count += i

print count/len(array_9)

count = 0
for i in array_11:
    count += i

print count/len(array_11)
