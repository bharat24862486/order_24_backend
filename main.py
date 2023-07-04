from flask import Flask, render_template, request,jsonify
from flask_cors import CORS
import pickle
app = Flask(__name__)

CORS(app)




def load_data(filename):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def save_data(data, filename):
    with open(filename, "wb") as file:
        pickle.dump(data, file)

arr = load_data("arr.pkl")
order = load_data("order.pkl")

@app.route('/', methods=['GET'])
def read():
    
    return jsonify(arr)

@app.route('/add_dish', methods=['POST'])
def addDish():
    if request.method == 'POST':
        data = request.get_json()


        
        
        for i in arr:
            if i["ID"] == data["ID"]:
                return jsonify("Item has already exists")
            
        
        arr.append(data)
        save_data(arr,"arr.pkl")
    return jsonify("Item added successfully")







@app.route('/new_order', methods=['POST'])
def new_order():
    if request.method == 'POST':
        data = request.get_json()

        quantity = data["Quantity"]
        p = 0

        for i in arr:
            if i["ID"] == data["ID"]:
                if data["Quantity"] > i["Quantity"]:
                    return jsonify("Not enough quantity")
                else :
                    q = i["Quantity"]
                    q1 = q-quantity
                    i["Quantity"] = q1
                    p+=i["Price"]
                    

                    # return jsonify("")
        for i in arr:
            if i["Quantity"] <= 0 :
                    arr.remove(i)

        
        q = data["Quantity"]
        t = q*p
        


        data["Status"] = "Pending"
        data["Total"] = t
        order.append(data)
        save_data(order,"order.pkl")

        return jsonify("Your order is in pending state click on confirm to confirm your order")
    


        
        


        
            
        
    
    return jsonify("Item added successfully")









@app.route('/update/<int:Id>', methods=['PATCH'])
def update_dish(Id):
    if request.method == 'PATCH':
        data = request.get_json()


        
        
        for i in arr:
            if i["ID"] == Id:
                i["Quantity"] = data["Quantity"]
                i["Price"] = data["Price"]
                i["Name"] = data["Name"]
                
                return jsonify("Item Updated successfully")
            
        
        
    return jsonify("Data added succesfully")

@app.route('/delete/<int:Id>', methods=['DELETE'])
def remove_dish(Id):
    if request.method == 'DELETE':
        
        

        
        for i in arr:
            if i["ID"] == Id:
                arr.remove(i)
                return jsonify("Item delete successfully")
                
            
        
       
    return jsonify('Item not found')




if __name__ == '__main__':
    app.run(debug=True)