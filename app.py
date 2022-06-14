from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)
@app.route('/', methods = ['GET'])
def retrieveAll():
    holder = list()
    currentCollection = mongo.db.todo
    for i in currentCollection.find():
        holder.append({'task':i['task']})
    return jsonify(holder)

@app.route('/PostTask', methods = ['POST'])
def PostTask():
    holder = list()
    id = ""
    currentCollection = mongo.db.todo
    task = request.json['task']
    currentCollection.insert_one({'task' : task})
    for i in currentCollection.find():
        print(i.get("_id"))
        id = str(i.get("_id"))
        holder.append({'task':i['task'],'taskid': id})
    return jsonify(holder)
@app.route('/deletetask/<id>', methods = ['DELETE'])
def deleteData(id):
    holder = list()
    currentCollection = mongo.db.todo
    currentCollection.delete_one({'_id':ObjectId(id)})
    for i in currentCollection.find():
        print(i.get("_id"))
        id = str(i.get("_id"))
        holder.append({'task':i['task'],'taskid': id})
    return jsonify(holder)
    # return redirect(url_for('retrieveAll'))
@app.route('/update/<id>', methods = ['PUT'])
def updateData(id):
    holder = list()
    task = request.json['updatetask']
    currentCollection = mongo.db.todo
    currentCollection.update_one({'_id': ObjectId(id)},  {'$set': {"task": task}})
    for i in currentCollection.find():
        print(i.get("_id"))
        id = str(i.get("_id"))
        holder.append({'task':i['task'],'taskid': id})
    return jsonify(holder)
    


    
# posts.insert({'a':1})





if __name__ == '__main__':
    app.run(debug=True)