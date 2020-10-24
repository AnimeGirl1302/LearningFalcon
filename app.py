import json, falcon
import server

class User:
    
    # Add user to the db
    # pass name, mob, city in the body 

    """
        {
            "name":"abcd",
            "mobile":"9876543210",
            "city":"xyz"
        }
    """

    def on_post(self, req, res):

        data = json.loads(req.stream.read())

        name = str(data['name'])
        mob = str(data['mobile'])
        city = str(data['city'])

        # Inserting the user to the user table
        sql = "INSERT INTO user (name, mobile , city) VALUES (%s, %s, %s)"
        val = (name, mob, city)
        server.mycursor.execute(sql, val)

        server.mydb.commit()

        res.body = "User successfully created"



    # update user city when he moves out
    # pass mobile number in the body

    """
        {
            "mobile":"9876543210",
            "city":"xyz"
        }
    """

    def on_put(self, req, res):
        data = json.loads(req.stream.read())

        mob = str(data['mobile'])
        city = str(data['city'])

        # updating the user city 
        sql = """ UPDATE user SET city = %s WHERE mobile = %s """
        val = (city,mob)
        server.mycursor.execute(sql,val) 
        
        server.mydb.commit()

        # show the updated user details
        sql = "SELECT * FROM user WHERE mobile = %s "
        server.mycursor.execute(sql, (mob,))

        row = server.mycursor.fetchall()
        res.body = json.dumps(row)


            
    # fetch the user details
    # pass mobile num in the body 

    """
        {
            "mobile":"9876543210"
        }
    """

    def on_get(self, req, res):

        data = json.loads(req.stream.read())

        val = (str(data['mobile']),)
        sql = """SELECT * FROM user WHERE mobile = %s"""

        server.mycursor.execute(sql,val) 
        
        rows = server.mycursor.fetchall()
        if len(rows) == 0:
            res.body = "Data Doesn't exist"

        else:
            res.body = json.dumps(rows)





class Admin:

    #fetch all the complaints whose 
    #complaint_status is as mentioned in the body

    """
        {
            "status":"In progress"
        }
    """

    def on_get(self, req, res):

        data = json.loads(req.stream.read())

        comp_status = str(data['status'])

        sql = "SELECT c.comp_id, c.descrip FROM complaint AS c INNER JOIN complaint_status AS s ON s.status = %s AND c.comp_id = s.comp_id"
        server.mycursor.execute(sql, (comp_status,))

        rows = server.mycursor.fetchall()
        res.body = json.dumps(rows)



    # update the status of the complaints
    # pass complaint id
    # in progress, resolved


    """
        {
            "comp_id":"4",
            "status":"Pending"
        }
    """

    def on_put(self, req, res):
        
        data = json.loads(req.stream.read())

        comp_id = str(data['comp_id'])
        status = str(data['status'])

        sql = "UPDATE complaint_status SET status = %s WHERE comp_id = %s"
        val = (status,comp_id)

        server.mycursor.execute(sql,val)
        server.mydb.commit()

        res.body = "Complaint status updated"



class Comp:

    # add complaint to the db
    # pass type of complaint, description, mobile number
    # check whether user exists using mobile
    # only if user exist add complaint

    """
        {
            "type":"Infra",
            "description":"blah blah",
            "mobile":"9876543210"
        }
    """

    def on_post(self, req, res):
        
        data = json.loads(req.stream.read())

        typeOfComp = str(data['type'])
        description = str(data['description'])
        mob = str(data['mobile'])


        # first check if the user exist or not 
        sql = "SELECT * FROM user WHERE mobile = %s"
        server.mycursor.execute(sql,(mob,))
        row = server.mycursor.fetchall()

        if len(row) == 0:
            res.body = "User doesn't exist. Create user first..!!"
        
        else:
            # Add a new complaint to the table
            sql = "INSERT INTO complaint (type, descrip , mobile) VALUES (%s, %s, %s)"
            val = (typeOfComp,description,mob)
            server.mycursor.execute(sql, val)

            id = server.mycursor.lastrowid
            
            defualt_status = "PENDING"
            sql = "INSERT INTO complaint_status (status, comp_id) VALUES (%s, %s)"
            val = (defualt_status,id)
            server.mycursor.execute(sql, val)
            server.mydb.commit()

            res.body = "Complaint successfully registered. Please remember the complaint id:{} for further enquiry or update".format(id)
    
    # modify complaint
    # fetch complaint first and then modify it then update

    """
        {
            "comp_id":"9",
            "description":"blah blah"
        }

    """
    def on_put(self, req, res):
        
        data = json.loads(req.stream.read())

        comp_id = str(data['comp_id'])
        descrip = str(data['description'])

        sql = "UPDATE complaint SET descrip = %s WHERE comp_id = %s"
        val = (descrip, comp_id)

        server.mycursor.execute(sql,val)
        server.mydb.commit()

        res.body = "Complaint description updated."




    #delete complaint
    #get complaint delete it. 

    """
        {
            "comp_id":"9876543210"
        }
    """
    def on_delete(self, req, res):

        data = json.loads(req.stream.read())

        comp_id = str(data['comp_id'])

        sql = "DELETE FROM complaint complaint_status WHERE comp_id = %s" 
        server.mycursor.execute(sql, (comp_id,))

        server.mydb.commit()

        res.body = "Complaint successfully deleted. "
        

    
    
    # get all the complaints registered by a given user
    # pass mobile of user in body
    
    """
        {
            "mobile":"9876543210"
        }
    """
    def on_get(self, req, res):

        data = json.loads(req.stream.read())

        mob = str(data['mobile'])

        sql = "SELECT * FROM complaint WHERE mobile = %s"
        server.mycursor.execute(sql,(mob,))

        rows = server.mycursor.fetchall()
        res.body = json.dumps(rows)


        


api = falcon.API()
api.add_route('/user', User())
api.add_route('/admin', Admin())
api.add_route('/complaint', Comp())

# use ComplaintBox;

# drop table user;
# drop table complaint;
# drop table complaint_status;

# show tables;


# use ComplaintBox;

# select * from user;