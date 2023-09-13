import sys
import psycopg2
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6 import uic, QtCore, QtGui
from datetime import datetime

qtCreatorFile = "milestone2App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.postalCodeList.itemSelectionChanged.connect(self.postalcodeChanged)
        self.ui.businessSearchButton.clicked.connect(self.searchBusiness)
        self.ui.clearButton.clicked.connect(self.clearSearch)
        self.ui.postalCodeList.itemSelectionChanged.connect(self.numBusinessStat)
        self.ui.postalCodeList.itemSelectionChanged.connect(self.totalPopStat)
        self.ui.postalCodeList.itemSelectionChanged.connect(self.avgIncomeStat)
        self.ui.postalCodeList.itemSelectionChanged.connect(self.categoryStat)
        self.ui.businessSearchButton.clicked.connect(self.popularTableSearch)
        self.ui.businessSearchButton.clicked.connect(self.successfulTableSearch)




    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='BAB0Y!'")
        except:
            print('Unable to connect to the database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM  business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            # print(results)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        self.ui.postalCodeList.clear()
        state = self.ui.stateList.currentText()
        if(self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
                print(results)
            except:
                print("Query failed")

            # for i in reversed(range(self.ui.businessTable.rowCount())):
            #     self.ui.businessTable.removeRow(i)
            # sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name;"
            # try:
            #     results = self.executeQuery(sql_str)
            #     style = "::section {""background-color: #f3f3f3; }"
            #     self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            #     self.ui.businessTable.setColumnCount(len(results[0]))
            #     self.ui.businessTable.setRowCount(len(results))
            #     self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            #     self.ui.businessTable.resizeColumnsToContents()
            #     self.ui.businessTable.setColumnWidth(0, 300)
            #     self.ui.businessTable.setColumnWidth(1, 100)
            #     self.ui.businessTable.setColumnWidth(2, 50)
            #     currentRowCount = 0
            #     for row in results:
            #         for colCount in range(0, len(results[0])):
            #             self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
            #         currentRowCount += 1
            # except:
            #     print("query failed")
    def cityChanged(self):
        if(self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct postal_code FROM business WHERE state ='" + state + "' AND city='" + city + "' ORDER BY postal_code;"
            # print(sql_str)
            results = self.executeQuery(sql_str)
            try:
                self.ui.postalCodeList.clear()
                self.ui.categoryList.clear()
                for row in results:
                    self.ui.postalCodeList.addItem(row[0])
            except:
                print("Query failed")
            # try:
            #     results = self.executeQuery(sql_str)
            #     style = "::section {""background-color: #f3f3f3; }"
            #     self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            #     self.ui.businessTable.setColumnCount(len(results[0]))
            #     self.ui.businessTable.setRowCount(len(results))
            #     self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            #     self.ui.businessTable.resizeColumnsToContents()
            #     self.ui.businessTable.setColumnWidth(0, 300)
            #     self.ui.businessTable.setColumnWidth(1, 100)
            #     self.ui.businessTable.setColumnWidth(2, 50)
            #     currentRowCount = 0
            #     for row in results:
            #         for colCount in range(0, len(results[0])):
            #             self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
            #         currentRowCount += 1
            # except:
            #     print("query failed")

    def postalcodeChanged(self):
        # adds category list
        if(self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.postalCodeList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT category " + \
                      "FROM business_category " + \
                      "JOIN business ON business.business_id = business_category.business_id " + \
                      "WHERE state = '" + state + "' " + \
                      "AND city = '" + city + "' " + \
                      "AND postal_code = '" + postalCode + "' " + \
                      "ORDER BY category;"
            try:
                self.ui.categoryList.clear()
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed")

    def searchBusiness(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            # Clear the existing contents of businessTable
            self.ui.businessTable.clearContents()
            self.ui.businessTable.setRowCount(0)

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()
            category_filter = ""
            if len(self.ui.categoryList.selectedItems()) > 0:
                category = self.ui.categoryList.selectedItems()[0].text()
                category_filter = f"AND business_id IN (SELECT business_id FROM business_category WHERE category = '{category}')"
            try:
                sql_str = f"SELECT name, address, city, stars, review_count, review_rating, num_checkins FROM business WHERE state = '{state}' AND city = '{city}' AND postal_code = '{postalCode}' {category_filter} ORDER BY name;"
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                if results:  # Check if results is not empty
                    self.ui.businessTable.setRowCount(len(results))
                    self.ui.businessTable.setColumnCount(len(results[0]))
                    self.ui.businessTable.setHorizontalHeaderLabels(
                        ['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating',
                         'Number of Checkins'])
                    self.ui.businessTable.resizeColumnsToContents()
                    self.ui.businessTable.setColumnWidth(0, 150)
                    self.ui.businessTable.setColumnWidth(1, 150)
                    self.ui.businessTable.setColumnWidth(2, 100)
                    self.ui.businessTable.setColumnWidth(3, 50)
                    self.ui.businessTable.setColumnWidth(4, 150)
                    self.ui.businessTable.setColumnWidth(5, 150)
                    self.ui.businessTable.setColumnWidth(6, 150)
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            value = row[colCount]
                            if colCount == 3:  # Assuming the 'stars' column is at index 3
                                if value is None or not isinstance(value, (float, int)):
                                    value = "N/A"
                                else:
                                    value = str(value)
                            self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(value)))
                        currentRowCount += 1
                else:
                    print("No results found")
            except:
                print("Query failed")

    def clearSearch(self):
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.cityList.clearSelection()
        self.ui.postalCodeList.clearSelection()

        #Clear the category selection if any
        self.ui.categoryList.clear()

        #Clear the business table
        self.ui.businessTable.clearContents()
        self.ui.businessTable.setRowCount(0)

        self.ui.topCategoryTable.clearContents()
        self.ui.popularTable.clearContents()

    def numBusinessStat(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()
            sql_str = f"SELECT COUNT(*) as num_businesses FROM business WHERE postal_code = '{postalCode}' GROUP BY postal_code;"
            try:
                results = self.executeQuery(sql_str)

                if len(results) > 0:
                    num_businesses = results[0][0]  # Assuming num_businesses is the first column in the result
                    self.ui.numBusinesses.setText(f"{num_businesses}")
                else:
                    self.ui.numBusinesses.setText("N/A")
            except:
                print("Query failed")
        else:
            # Clear the label when city or state is not selected
            self.ui.numBusinesses.clear()

    def totalPopStat(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()
            sql_str = f"SELECT population FROM zipcodedata WHERE zipcode = '{postalCode}';"
            try:
                results = self.executeQuery(sql_str)

                if len(results) > 0:
                    total_pop = results[0][0]  # Assuming num_businesses is the first column in the result
                    self.ui.totalPop.setText(f"{total_pop}")
                else:
                    self.ui.totalPop.setText("N/A")
            except:
                print("Query failed")
        else:
            # Clear the label when city or state is not selected
            self.ui.totalPop.clear()

    def avgIncomeStat(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()
            sql_str = f"SELECT meanincome FROM zipcodedata WHERE zipcode = '{postalCode}';"
            try:
                results = self.executeQuery(sql_str)

                if len(results) > 0:
                    avg_income = results[0][0]  # Assuming num_businesses is the first column in the result
                    self.ui.avgInc.setText(f"{avg_income}")
                else:
                    self.ui.avgInc.setText("N/A")
            except:
                print("Query failed")
        else:
            # Clear the label when city or state is not selected
            self.ui.avgInc.clear()

    def categoryStat(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            # Clear the existing contents of businessTable
            self.ui.topCategoryTable.clearContents()
            self.ui.topCategoryTable.setRowCount(0)

            postalCode = self.ui.postalCodeList.selectedItems()[0].text()
            try:
                sql_str = (
                    "SELECT bc.category, COUNT(*) as num_businesses "
                    "FROM business as b "
                    "JOIN business_category as bc ON b.business_id = bc.business_id "
                    f"WHERE b.postal_code = '{postalCode}' "
                    "GROUP BY bc.category "
                    "ORDER BY COUNT(*) DESC;"
                )
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.topCategoryTable.horizontalHeader().setStyleSheet(style)
                if results:  # Check if results is not empty
                    self.ui.topCategoryTable.setRowCount(len(results))
                    self.ui.topCategoryTable.setColumnCount(2)  # Two columns: # of Businesses and Category
                    self.ui.topCategoryTable.setHorizontalHeaderLabels(['# of Businesses', 'Category'])
                    self.ui.topCategoryTable.resizeColumnsToContents()
                    self.ui.topCategoryTable.setColumnWidth(0, 100)
                    self.ui.topCategoryTable.setColumnWidth(1, 100)
                    currentRowCount = 0
                    for row in results:
                        # Insert the values into the table widget
                        self.ui.topCategoryTable.setItem(currentRowCount, 0,
                                                         QTableWidgetItem(str(row[1])))  # # of Businesses
                        self.ui.topCategoryTable.setItem(currentRowCount, 1, QTableWidgetItem(row[0]))  # Category
                        currentRowCount += 1
                else:
                    print("No results found")
            except:
                print("Query failed")

    def popularTableSearch(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            # Clear the existing contents of popularTable table
            self.ui.popularTable.clearContents()
            self.ui.popularTable.setRowCount(0)

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()

            try:
                # Query to get the popular businesses based on review_count and stars
                popular_business_query = (
                    "SELECT name, stars, review_rating, review_count "
                    "FROM Business "
                    f"WHERE state = '{state}' AND city = '{city}' AND postal_code = '{postalCode}' "
                    "AND review_count > ( "
                    "  SELECT AVG(review_count) "
                    "  FROM Business AS b "
                    f"  WHERE state = '{state}' AND city = '{city}' AND postal_code = '{postalCode}' "
                    ") "
                    "AND stars > 4.0 "
                    "ORDER BY name;"
                )
                popular_business_results = self.executeQuery(popular_business_query)

                if popular_business_results:  # Check if results are not empty
                    self.ui.popularTable.setRowCount(len(popular_business_results))
                    self.ui.popularTable.setColumnCount(4)  # Four columns: Name, Stars, Review Rating, Review Count
                    self.ui.popularTable.setHorizontalHeaderLabels(
                        ['Name', 'Stars', 'Review Rating', 'Review Count'])
                    self.ui.popularTable.resizeColumnsToContents()
                    self.ui.popularTable.setColumnWidth(0, 200)
                    self.ui.popularTable.setColumnWidth(1, 50)
                    self.ui.popularTable.setColumnWidth(2, 150)
                    self.ui.popularTable.setColumnWidth(3, 100)

                    # Iterate through popular business results and insert details into the QTableWidget
                    currentRowCount = 0
                    for business in popular_business_results:
                        name = business[0]
                        stars = str(business[1]) if business[1] is not None else "N/A"
                        review_rating = str(business[2]) if business[2] is not None else "N/A"
                        review_count = str(business[3]) if business[3] is not None else "N/A"

                        # Insert the business details into the QTableWidget
                        self.ui.popularTable.setItem(currentRowCount, 0, QTableWidgetItem(name))
                        self.ui.popularTable.setItem(currentRowCount, 1, QTableWidgetItem(stars))
                        self.ui.popularTable.setItem(currentRowCount, 2, QTableWidgetItem(review_rating))
                        self.ui.popularTable.setItem(currentRowCount, 3, QTableWidgetItem(review_count))

                        currentRowCount += 1
                else:
                    print("No results found")
            except:
                print("Query failed")

    from datetime import datetime

    from datetime import datetime

    # ... (other parts of your code)

    def successfulTableSearch(self):
        if (
                self.ui.stateList.currentIndex() >= 0
                and len(self.ui.cityList.selectedItems()) > 0
                and len(self.ui.postalCodeList.selectedItems()) > 0
        ):
            # Clear the existing contents of successfulTable table
            self.ui.successfulTable.clearContents()
            self.ui.successfulTable.setRowCount(0)

            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            postalCode = self.ui.postalCodeList.selectedItems()[0].text()

            try:
                # Query to get successful businesses based on the number of check-ins
                successful_business_query = (
                    "SELECT name, review_count, num_checkins, MIN(review_date) AS earliest_review_date "
                    "FROM Business "
                    "LEFT JOIN Reviews ON Business.business_id = Reviews.business_id "
                    f"WHERE state = '{state}' AND city = '{city}' AND postal_code = '{postalCode}' "
                    "AND num_checkins > 100 "  # Set a threshold for the minimum number of check-ins to consider a business as successful
                    "GROUP BY Business.business_id "
                    "HAVING EXTRACT(YEAR FROM NOW()) - EXTRACT(YEAR FROM MIN(review_date)) >= 10 "
                    "ORDER BY name;"
                )
                successful_business_results = self.executeQuery(successful_business_query)

                if successful_business_results:  # Check if results are not empty
                    self.ui.successfulTable.setRowCount(len(successful_business_results))
                    self.ui.successfulTable.setColumnCount(
                        5)  # Five columns: Name, # of Reviews, # of Checkins, Longevity (Years), Earliest Review Date
                    self.ui.successfulTable.setHorizontalHeaderLabels(
                        ['Name', '# of Reviews', '# of Checkins', 'Longevity (Years)', 'Earliest Review Date'])
                    self.ui.successfulTable.resizeColumnsToContents()
                    self.ui.successfulTable.setColumnWidth(0, 200)
                    self.ui.successfulTable.setColumnWidth(1, 100)
                    self.ui.successfulTable.setColumnWidth(2, 100)
                    self.ui.successfulTable.setColumnWidth(3, 100)
                    self.ui.successfulTable.setColumnWidth(4, 150)

                    # Iterate through successful business results and insert details into the QTableWidget
                    currentRowCount = 0
                    for business in successful_business_results:
                        name = business[0]
                        num_reviews = str(business[1]) if business[1] is not None else "N/A"
                        num_checkins = str(business[2]) if business[2] is not None else "N/A"

                        earliest_review_date = business[3]
                        longevity = "N/A"
                        if earliest_review_date:
                            earliest_review_date_str = earliest_review_date.strftime('%Y-%m-%d')
                            longevity = str(datetime.now().year - earliest_review_date.year)

                        # Insert the business details and longevity into the QTableWidget
                        self.ui.successfulTable.setItem(currentRowCount, 0, QTableWidgetItem(name))
                        self.ui.successfulTable.setItem(currentRowCount, 1, QTableWidgetItem(num_reviews))
                        self.ui.successfulTable.setItem(currentRowCount, 2, QTableWidgetItem(num_checkins))
                        self.ui.successfulTable.setItem(currentRowCount, 3, QTableWidgetItem(longevity))
                        self.ui.successfulTable.setItem(currentRowCount, 4, QTableWidgetItem(earliest_review_date_str))

                        currentRowCount += 1
                else:
                    print("No results found")
            except:
                print("Query failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec())
