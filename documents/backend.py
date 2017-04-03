import bottle
import pymongo
from bottle import response, request
import json
from bson import ObjectId
import os
import time
import requests
import logging

class JSONEncoder1(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    @staticmethod
    def apply(fn, context):
        def _enable_cors(*args, **kwargs):
            # print context
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            response.headers['Content-type'] = 'application/json'
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()
app.install(EnableCors())

print "START"
coll_name = 'documents'


def get_database_host():
    try:
        host = os.environ.get('DATABASE_HOST')
    except Exception, e:
        print e
        host = None
        print "ERROR"
    if host:
        pass
    else:
        host = 'arkismongopersistent'
    return host


def get_database_port():
    try:
        port = int(os.environ.get('DATABASE_PORT'))
    except Exception, e:
        print e
        port = None
        print "ERROR"
    if port:
        pass
    else:
        port = 27017
    return port


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
        conn = pymongo.MongoClient(conn_cluster, readPreference='secondaryPreferred')
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


@app.route('/')
def start():
    a2 = {"mongos": "no"}
    conn = get_connection(None, None, 3)
    a3 = {"conn": str(conn)}
    # host = get_database_host()
    # port = get_database_port()
    conn_cluster = "a"
    a1 = {"conn_cluster": conn_cluster}
    try:
        a2 = {"mongos": conn.is_mongos}
    except Exception, e:
        print e

    res = [a1, a2, a3]
    return JSONEncoder1().encode(res)


@app.route('/check/<replica>')
def check(replica):
    conn = get_connection(None, None, int(replica))
    time.sleep(5)
    try:
        a1 = {"conn1": str(conn.read_preference)}
        print conn.read_preference
    except Exception, e:
        print e
        a1 = {"conn1": str(e)}
    logging.info("trying to config the mongo client")
    try:
        nodes = []
        for n in conn.nodes:
            logging.info(str(n))
            print n
            nodes.append(str(n))
        a2 = {"conn2": nodes}
    except Exception, e:
        print e
        a2 = {"conn2": str(e)}

    try:
        for s in conn.secondaries:
            logging.info(len(s))
            print s
        a3 = {"conn3": str(conn.secondaries)}
    except Exception, e:
        print e
        a3 = {"conn3": str(e)}

    try:
        a4 = {"conn3": len(conn.get_default_database())}
    except Exception, e:
        print e
        a4 = {"conn3": str(e)}

    try:
        a5 = {"conn3": str(conn.read_concern)}
    except Exception, e:
        print e
        a5 = {"conn3": str(e)}

    try:
        a6 = {"conn3": str(conn.server_info())}
        infos = []
        for info in conn.server_info():
            infos.append(str(info))
        a7 = {"conn3": infos}
    except Exception, e:
        print e
        a6 = {"conn3": str(e)}
        a7 = {"conn3": str(e)}

    res = [a1, a2, a3, a4, a5, a6, a7]
    return JSONEncoder1().encode(res)


@app.route('/connection/<user>/<option>/<replica>')
def connection(user, option, replica):
    user = int(user)
    try:
        conn = get_connection(user, option, int(replica))
    except Exception, e:
        collection_names = ["error connection", e]
        return JSONEncoder1().encode({"collections": collection_names})
    try:
        db = get_database(conn, option, user)
    except Exception, e:
        collection_names = ["error database", e]
        return JSONEncoder1().encode({"collections": collection_names})
    collection_names = db.collection_names()
    conn.close()
    return JSONEncoder1().encode({"collections": collection_names})


@app.get('/documents/search/<user>/<option>/<replica>/<pattern>')
def search(user, option, pattern, replica):
    user = int(user)
    try:
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        name = pattern
        example = get_collection(option, db, user, 'documents').find_one(
            {"user": user, "$text": {"$search": name, "$caseSensitive": True}})
        conn.close()
        # TODO CYCLOPS ENDPOINT
        if False:
            try:
                cyclops_endpoint = os.environ.get('CYCLOPS_ENDPOINT')
                if cyclops_endpoint:
                    pass
                else:
                    cyclops_endpoint = '35.160.33.120:4567'
                try:
                    cyclops_time = time.time()
                except Exception, e:
                    print e
                data = {"_class": "ArkisSearchUsage",
                        "account": "ArkisUser",
                        "usage": 1,
                        "unit": "query"}
                # url = 'http://160.85.4.150:4567/data'
                url = 'http://' + cyclops_endpoint + '/data'
                # url = 'http://35.160.33.120:4567/data'
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                rcyclops = requests.post(url, data=json.dumps(data), headers=headers)
                print rcyclops.status_code
                print rcyclops.content
            except Exception, e:
                print "Error with petition post to cyclops"
                print e
        return JSONEncoder1().encode(example)
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])


@app.get('/documents/<user>/<option>/<replica>/lim/<lim>')
def get_all(user, option, lim, replica):
    user = int(user)
    try:
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        if lim == 'nolimit':
            # Change the limit
            r = get_collection(option, db, user, 'documents').find({"user": user}).limit(10000)
        else:
            r = get_collection(option, db, user, 'documents').find({"user": user}).limit(int(lim))
        conn.close()
        res = []
        for a in r:
            res.append(a)
    except Exception, e:
        print e
        error_str = "ERROR LOOKING DOCUMENTS FOR USER " + str(user) + " WITH MT OPTION " + str(option)
        a = {"error": error_str}
        res = [a]
    return JSONEncoder1().encode(res)


@app.get('/documents/<user>/<option>/<replica>/last')
def get_last(user, option, replica):
    user = int(user)
    try:
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        r = get_collection(option, db, user, 'documents').find_one(sort=[("other_id", -1)])
        conn.close()
    except Exception, e:
        print e
        error_str = "ERROR LOOKING DOCUMENTS FOR USER " + str(user) + " WITH MT OPTION " + str(option)
        r = {"error": error_str}
    return JSONEncoder1().encode(r)


@app.get('/documents/<min1>/<max1>/<option>/<replica>/len')
def get_number_documents(min1, max1, option, replica):
    res = []
    try:
        conn = get_connection(None, option, int(replica))
        count = 0
        for i in range(int(min1), int(max1)):
            a = conn['arkis' + str(i)].documents.count()
            count += int(a)
            key_aux = 'documents' + str(i)
            val_aux = str(a)
            aux = {key_aux: val_aux}
            res.append(aux)
        aux = {"total": str(count)}
        res.append(aux)
        conn.close()
    except Exception, e:
        print e
        error_str = "ERROR LOOKING DOCUMENTS FOR USER " + str(max1) + " WITH MT OPTION " + str(option)
        r = {"error": error_str}
    return JSONEncoder1().encode(res)


@app.get('/documents/<user>/<option>/<replica>/<other_id>')
def get_by_id(user, option, other_id, replica):
    try:
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        user = int(user)
        r = get_collection(option, db, user, 'documents').find_one({"other_id": int(other_id), "user": user})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


def get_max_row_id(user, option, replica):
    try:
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        a = int(get_collection(option, db, user, 'documents').find_one(sort=[("other_id", -1)])['other_id'])
        conn.close()
        return a
    except Exception, e:
        print e
        return -2


@app.post('/documents/<user>/<option>/<replica>')
def post(user, option, replica):
    try:
        user = int(user)
        blob = request.forms.get('blob')
        number = int(request.forms.get('number'))
        name = request.forms.get('name')
        title = request.forms.get('title')
        path = '/data/blobs/arkis_' + option + '_' + str(user) + '_' + name + '.txt'
        max_index = get_max_row_id(user, option, replica)
        if max_index == -1:
            return JSONEncoder1().encode([{"error": "no index"}])
        else:
            other_id = max_index + 1
        # print rowident
        aux_blob = {'blob': blob,
                    'number': number,
                    'name': name,
                    'title': title,
                    'other_id': other_id,
                    'user': user,
                    'tenant': user,
                    'tenant_option': option,
                    'path': path}
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        get_collection(option, db, user, 'documents').insert_one(aux_blob)
        conn.close()
    except Exception, e:
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([aux_blob])


@app.put('/documents/<user>/<option>/<replica>/<other_id>')
def put(user, option, other_id, replica):
    r = None
    try:
        try:
            user = int(user)
            conn = get_connection(user, option, int(replica))
            db = get_database(conn, option, user)
            r = get_collection(option, db, user, 'documents').find_one({"other_id": int(other_id), "user": user})
        except Exception, e:
            return JSONEncoder1().encode([{"error": str(e)}])
        aux_blob = request.forms.get('blob')
        aux_number = request.forms.get('number')
        aux_name = request.forms.get('name')
        aux_title = request.forms.get('title')
        aux_path = None
        if aux_title:
            r['title'] = aux_title
        if aux_name:
            aux_path = '/data/blobs/arkis_' + option + '_' + str(user) + '_' + aux_name + '.txt'
            r['name'] = aux_name
        if aux_path:
            r['path'] = aux_path
        if aux_number:
            aux_number = int(aux_number)
            r['number'] = aux_number
        if aux_blob:
            r['blob'] = aux_blob
        get_collection(option, db, user, 'documents').update({"other_id": int(other_id)}, r)
        conn.close()
    except Exception, e:
        if r:
            return JSONEncoder1().encode([{"error": str(e)}, r])
        else:
            return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


@app.post('/put/documents/<user>/<option>/<replica>/<other_id>')
def put1(user, option, other_id, replica):
    r = None
    try:
        try:
            user = int(user)
            conn = get_connection(user, option, int(replica))
            db = get_database(conn, option, user)
            r = get_collection(option, db, user, 'documents').find_one({"other_id": int(other_id), "user": user})
        except Exception, e:
            return JSONEncoder1().encode([{"error": str(e)}])
        aux_blob = request.forms.get('blob')
        aux_number = request.forms.get('number')
        aux_name = request.forms.get('name')
        aux_title = request.forms.get('title')
        aux_path = None
        if aux_title:
            r['title'] = aux_title
        if aux_name:
            aux_path = '/data/blobs/arkis_' + option + '_' + str(user) + '_' + aux_name + '.txt'
            r['name'] = aux_name
        if aux_path:
            r['path'] = aux_path
        if aux_number:
            aux_number = int(aux_number)
            r['number'] = aux_number
        if aux_blob:
            r['blob'] = aux_blob
        get_collection(option, db, user, 'documents').update({"other_id": int(other_id)}, r)
        conn.close()
    except Exception, e:
        if r:
            return JSONEncoder1().encode([{"error": str(e)}, r])
        else:
            return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode(r)


@app.delete('/documents/<user>/<option>/<replica>/<other_id>')
def delete(user, option, other_id, replica):
    try:
        user = int(user)
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        get_collection(option, db, user, 'documents').delete_one({"other_id": int(other_id), "user": user})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([{"res": "Deleted"}])


@app.get('/delete/documents/<user>/<option>/<replica>/<other_id>')
def delete1(user, option, other_id, replica):
    try:
        user = int(user)
        conn = get_connection(user, option, int(replica))
        db = get_database(conn, option, user)
        get_collection(option, db, user, 'documents').delete_one({"other_id": int(other_id), "user": user})
        conn.close()
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    return JSONEncoder1().encode([{"res": "Deleted"}])


@app.get('/blobs/host/<host1>')
def change_host(host1):
    try:
        os.environ["DATABASE_HOST"] = host1
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    res = os.environ["DATABASE_HOST"]
    return JSONEncoder1().encode([{"host": res}])


@app.get('/blobs/port/<port1>')
def change_port(port1):
    try:
        os.environ["DATABASE_PORT"] = port1
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    res = os.environ["DATABASE_PORT"]
    return JSONEncoder1().encode([{"port": res}])


@app.get('/blobs/rcb/<rcb1>')
def change_rcb(rcb1):
    try:
        os.environ["CYCLOPS_ENDPOINT"] = rcb1
    except Exception, e:
        print e
        return JSONEncoder1().encode([{"error": str(e)}])
    res = os.environ["CYCLOPS_ENDPOINT"]
    return JSONEncoder1().encode([{"localhost": res}])


app.run(host='0.0.0.0', port=55555, debug=True)
