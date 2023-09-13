import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def getCategories(category):
    L = []
    for (category, value) in list(category.items()):
        if isinstance(value, dict):
            L += category(value)
        else:
            L.append((category,value))
    return L

def insert2BusinessTable():
    #reading the JSON file
    with open('.//yelp_dataset//yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='BAB0Y!'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            #Generate the INSERT statement for the cussent business
            #TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statment based on your own table schema ans
            # include values for all businessTable attributes
            sql_str = "INSERT INTO business(business_id,name,address,state,city,postal_code,stars,review_count)" \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data['name']) + "','" + cleanStr4SQL(data['address']) + "','" + \
                      data['state'] + "','" + cleanStr4SQL(data['city']) + "','" + data['postal_code'] + \
                      "'," + str(data['stars']) + "," + str(data['review_count']) + ");"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to TABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            categories = data['categories']
            # process business categories
            for category in data['categories']:
                cat_str = "INSERT INTO business_category(business_id,category)" \
                          "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(category) + "');"
                try:
                    cur.execute(cat_str)
                except Exception as e:
                    print("Insert to business_category table failed:", str(e))
                conn.commit()
            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2ReviewsTable():
    #reading the JSON file
    with open('.//yelp_dataset//yelp_review.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='BAB0Y!'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            #Generate the INSERT statement for the cussent business
            #TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statment based on your own table schema ans
            # include values for all businessTable attributes
            sql_str = "INSERT INTO reviews(review_id,business_id,review_stars,review_date)" \
                      "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + cleanStr4SQL(data['business_id']) + "','" + str(data['stars']) + "','" + str(data['date']) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to TABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2CheckinTable():
    #reading the JSON file
    with open('.//yelp_dataset//yelp_checkin.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='BAB0Y!'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            #Generate the INSERT statement for the cussent business
            #TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statment based on your own table schema ans
            # include values for all businessTable attributes
            for(dayofweek, time) in data['time'].items():
                for(hour, count) in time.items():
                    checkin_str = "INSERT INTO checkin(business_id,day,hour,count)" \
                                "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(dayofweek) + "','" + cleanStr4SQL(hour) + "'," + str(count) + ");"
                    try:
                        cur.execute(checkin_str)
                    except:
                        print("Insert to TABLE failed!")
                    conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


# insert2BusinessTable()
# insert2Business_CategoriesTable()
# insert2CheckinTable()
insert2ReviewsTable()