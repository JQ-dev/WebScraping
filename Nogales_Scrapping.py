from selenium import webdriver

driver = webdriver.Chrome('C:\chromedriver')

'''
driver.get('http://www.nogales.edu.co/autenticacion/padres/')
driver.find_element_by_name("smartUser").send_keys("88284590")
driver.find_element_by_name("smartPassword").send_keys("2664")
driver.find_element_by_class_name("goin").click()
'''

driver.get('http://app.nogales.edu.co/reportes_cln_web/loginP.aspx')
driver.find_element_by_name("txtlogin").send_keys("88284590")
driver.find_element_by_name("txtpassword").send_keys("2664")
driver.find_element_by_name("Button1").click()


year = ["2014-2015","2015-2016","2016-2017","2017-2018","2018-2019"]
bimester = ["1","2","3","4"]
#inform = [driver.find_element_by_id("RadioButtonList2_0"),driver.find_element_by_id("RadioButtonList2_1"),driver.find_element_by_id("RadioButtonList2_2"),driver.find_element_by_id("RadioButtonList2_3")]
inform = [driver.find_element_by_id("RadioButtonList2_1")]
student = [driver.find_element_by_id("RadioButtonList1_0"),driver.find_element_by_id("RadioButtonList1_1")]




for y in year:
    for b in bimester:
        for i in inform:
            for s in student:
                print(driver.find_element_by_name("Drop_Ano").send_keys(y) )
                print(driver.find_element_by_name("Drop_bim").send_keys(b) )
                print(i.click() )
                print(s.click() )
#                driver.find_element_by_id("ImageButton3").click()
                


#driver.find_element_by_name("Drop_Ano").send_keys("2015-2016")
#driver.find_element_by_name("Drop_bim").send_keys("3")

#driver.find_element_by_id("RadioButtonList2_0").click()
#driver.find_element_by_id("RadioButtonList2_1")
#driver.find_element_by_id("RadioButtonList2_2")
#driver.find_element_by_id("RadioButtonList2_3")

#driver.find_element_by_id("RadioButtonList1_0").click()
#driver.find_element_by_id("RadioButtonList1_1")

#driver.find_element_by_id("ImageButton3").click()