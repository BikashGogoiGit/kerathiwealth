import mysql.connector

cnx = mysql.connector.connect(user='root', database='e_commerce')
cursor2 = cnx.cursor()
query2 = f"SELECT product_name FROM ecommerce where company_name='oracle'"

#for (unique_id, product_id, product_name, prd_image) in cursor2:
 #   prd_image = prd_image
  #  print(prd_image)
#operation = 'SELECT 1; INSERT INTO t1 VALUES (); SELECT 2'
for result in cursor2.execute(query2, multi=True):
    if result.with_rows:
        #print("Rows produced by statement '{}':".format(
            #result.statement))
        rs = dict(result.fetchall())
        print(rs)

    else:
        print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))