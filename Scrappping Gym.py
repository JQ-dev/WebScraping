import selenium

from selenium import webdriver

driver = webdriver.Chrome('C:\chromedriver')


driver.get('https://www.myiclubonline.com/iclub/members')


driver.find_element_by_name("j_username").send_keys("ashleycbrandt")
driver.find_element_by_name("j_password").send_keys("")
driver.find_element_by_name("signIn").click()

driver.find_element_by_id("nav-classes").click()
driver.find_element_by_id("classesDayButton").click()
#driver.find_element_by_id("classesDateRangeTitle").click()
driver.find_element_by_id("classesNextButton").click()
driver.find_element_by_class(("classes mico_models_classes_4 listRowDark").("enrollEvent calltoaction")).click()






#driver.find_element_by_name("Drop_Ano").send_keys("2015-2016")
#driver.find_element_by_name("Drop_bim").send_keys("3")

#driver.find_element_by_id("RadioButtonList2_0").click()
#driver.find_element_by_id("RadioButtonList2_1")
#driver.find_element_by_id("RadioButtonList2_2")
#driver.find_element_by_id("RadioButtonList2_3")

#driver.find_element_by_id("RadioButtonList1_0").click()
#driver.find_element_by_id("RadioButtonList1_1")

#driver.find_element_by_id("ImageButton3").click()